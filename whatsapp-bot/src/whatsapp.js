// Capa de transporte WhatsApp usando Baileys (WhatsApp Web, no oficial).
import makeWASocket, {
  useMultiFileAuthState,
  DisconnectReason,
  fetchLatestBaileysVersion,
} from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { config } from './config.js';
import { logger, waLogger } from './logger.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const AUTH_DIR = join(__dirname, '..', 'auth_info');

let sock = null;

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
    await sock.sendMessage(jid, { text });
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

  sock.ev.on('messages.upsert', async ({ messages, type }) => {
    if (type !== 'notify') return;
    for (const msg of messages) {
      const jid = msg.key.remoteJid;
      // Ignora mensajes propios, grupos y estados.
      if (msg.key.fromMe || !jid || jid.endsWith('@g.us') || jid === 'status@broadcast') continue;
      const text =
        msg.message?.conversation ||
        msg.message?.extendedTextMessage?.text ||
        msg.message?.imageMessage?.caption ||
        '';
      if (!text.trim()) continue;
      try {
        await onMessage(jid, text.trim(), msg.pushName || null);
      } catch (err) {
        logger.error({ err: err.message, jid }, 'Error procesando mensaje entrante');
      }
    }
  });

  return sock;
}
