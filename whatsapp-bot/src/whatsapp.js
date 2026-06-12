// Capa de transporte WhatsApp usando Baileys (WhatsApp Web, no oficial).
import makeWASocket, {
  useMultiFileAuthState,
  DisconnectReason,
  fetchLatestBaileysVersion,
  downloadMediaMessage,
} from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { config } from './config.js';
import { logger, waLogger } from './logger.js';
import { rememberSavedContact, setIgnored } from './db.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const AUTH_DIR = join(__dirname, '..', 'auth_info');

let sock = null;

// IDs de mensajes que envió el propio bot (para distinguirlos de los que el
// dueño escribe a mano desde su teléfono).
const botSentIds = new Set();
const rememberBotSent = (id) => {
  if (!id) return;
  botSentIds.add(id);
  if (botSentIds.size > 3000) botSentIds.clear();
};

// Inyección de un socket falso para pruebas automatizadas.
export function _setSockForTest(fake) {
  sock = fake;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

// Envía texto simulando escritura humana (reduce riesgo de baneo).
export async function sendText(jid, text) {
  if (!sock) throw new Error('Socket de WhatsApp no inicializado');
  try {
    await sock.presenceSubscribe(jid);
    await sock.sendPresenceUpdate('composing', jid);
    await sleep(rand(config.minTypingMs, config.maxTypingMs));
    await sock.sendPresenceUpdate('paused', jid);
    const sent = await sock.sendMessage(jid, { text });
    rememberBotSent(sent?.key?.id);
  } catch (err) {
    logger.error({ err: err.message, jid }, 'Error enviando mensaje');
  }
}

// Inicia la conexión. onMessage(jid, text, pushName) se llama por cada mensaje entrante.
export async function startWhatsApp(onMessage) {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const { version } = await fetchLatestBaileysVersion();

  sock = makeWASocket({
    version,
    auth: state,
    logger: waLogger,
    printQRInTerminal: false,
    markOnlineOnConnect: false,
    syncFullHistory: false,
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', (update) => {
    const { connection, lastDisconnect, qr } = update;
    if (qr) {
      logger.info('Escanea este código QR con WhatsApp Business (Dispositivos vinculados):');
      qrcode.generate(qr, { small: true });
    }
    if (connection === 'open') {
      logger.info('✅ Conectado a WhatsApp');
    }
    if (connection === 'close') {
      const code = lastDisconnect?.error?.output?.statusCode;
      const loggedOut = code === DisconnectReason.loggedOut;
      logger.warn({ code }, loggedOut ? 'Sesión cerrada. Borra auth_info y reescanea el QR.' : 'Conexión cerrada, reintentando...');
      if (!loggedOut) startWhatsApp(onMessage);
    }
  });

  // Sincroniza tu agenda: los contactos con nombre guardado se marcan para ignorar.
  const remember = (list = []) => {
    let n = 0;
    for (const c of list) {
      if (c?.id?.endsWith('@s.whatsapp.net') && c.name) {
        rememberSavedContact(c.id, c.name);
        n++;
      }
    }
    if (n) logger.info({ n }, 'Contactos guardados sincronizados (el bot no les responderá)');
  };
  sock.ev.on('contacts.set', ({ contacts }) => remember(contacts));
  sock.ev.on('contacts.upsert', (contacts) => remember(contacts));
  sock.ev.on('contacts.update', (contacts) => remember(contacts));
  sock.ev.on('messaging-history.set', ({ contacts }) => remember(contacts));

  sock.ev.on('messages.upsert', async ({ messages, type }) => {
    for (const msg of messages) {
      const jid = msg.key.remoteJid;
      if (!jid || jid.endsWith('@g.us') || jid === 'status@broadcast') continue;

      // Mensajes salientes de la cuenta del bot.
      if (msg.key.fromMe) {
        // ¿lo envió el propio bot? -> es solo el eco, ignorar.
        if (botSentIds.has(msg.key.id)) {
          botSentIds.delete(msg.key.id);
          continue;
        }
        // Lo escribió el DUEÑO a mano desde su teléfono -> el humano atiende ese
        // chat: el bot deja de responderle a ese contacto (socios, amigos, etc.).
        if (config.ownerJid && jid === config.ownerJid) continue; // chat consigo mismo, no marcar
        setIgnored(jid, true);
        logger.info({ jid }, '✍️ Respondiste a mano: el bot ya no intervendrá en ese chat');
        continue;
      }

      if (type !== 'notify') continue; // solo procesamos mensajes entrantes nuevos
      const imageMessage = msg.message?.imageMessage;
      const hasImage = Boolean(imageMessage || msg.message?.documentMessage);
      const text =
        msg.message?.conversation ||
        msg.message?.extendedTextMessage?.text ||
        imageMessage?.caption ||
        msg.message?.documentMessage?.caption ||
        '';
      if (!text.trim() && !hasImage) continue; // ignora audios/stickers/etc. sin texto

      // Descarga la imagen (comprobante) para el OCR; los documentos no se procesan.
      let media = null;
      if (imageMessage) {
        try {
          const buffer = await downloadMediaMessage(msg, 'buffer', {}, { logger, reuploadRequest: sock.updateMediaMessage });
          media = { buffer, mimetype: imageMessage.mimetype || 'image/jpeg' };
        } catch (err) {
          logger.warn({ err: err.message }, 'No se pudo descargar la imagen');
        }
      }

      try {
        await onMessage(jid, text.trim(), msg.pushName || null, hasImage, media);
      } catch (err) {
        logger.error({ err: err.message, jid }, 'Error procesando mensaje entrante');
      }
    }
  });

  return sock;
}
