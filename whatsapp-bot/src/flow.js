// Motor de conversación: decide qué responder a cada mensaje entrante.
import { sendText } from './whatsapp.js';
import { getLead, upsertLead, getSetting, isIgnored } from './db.js';
import { detectCountry, config, DEFAULT_DEMO, DEFAULT_APPS } from './config.js';
import {
  detectOption,
  isCurrencyRequest,
  isClosing,
  isPaymentDone,
  isHumanRequest,
  isDemoRequest,
  isBankRequest,
  isGreeting,
} from './intents.js';
import * as msg from './messages.js';
import { handleOwnerCommand } from './commands.js';
import { syncLead } from './notion.js';
import { extractPaymentInfo } from './vision.js';
import { logger } from './logger.js';

const jidToPhone = (jid) => jid.split('@')[0];

// Envía un mensaje y registra la salida + estado actualizado.
async function reply(jid, text, fields = {}) {
  const lead = upsertLead(jid, { last_outbound: Date.now(), ...fields });
  await sendText(jid, text);
  await syncLead(lead);
  return lead;
}

async function alertOwner(text) {
  if (!config.ownerJid) {
    logger.warn('OWNER_JID no configurado: no se envió alerta.');
    return;
  }
  await sendText(config.ownerJid, text);
}

const currentDemo = () => msg.demoMessage(getSetting('demo', DEFAULT_DEMO), getSetting('apps', DEFAULT_APPS));

export async function handleMessage(jid, text, pushName, hasImage = false, media = null) {
  // 0) Mensajes del dueño: comandos de administración, nunca flujo de lead.
  if (config.ownerJid && jid === config.ownerJid) {
    await handleOwnerCommand(jid, text);
    return;
  }

  // 0.1) Contacto ya guardado en tu agenda (no es un lead): el bot NO responde.
  if (isIgnored(jid)) {
    logger.debug({ jid }, 'Contacto guardado/ignorado: el bot no responde');
    return;
  }

  const existing = getLead(jid);
  const isFirstContact = !existing;
  const country = detectCountry(jid);

  // Bot en pausa para este lead (handoff humano): solo registramos, no respondemos.
  if (existing?.stage === 'human') {
    upsertLead(jid, { last_inbound: Date.now(), name: pushName || existing.name, notes: text.slice(0, 500) });
    return;
  }

  // Registra el mensaje entrante y reinicia los relojes de seguimiento.
  const inboundFields = {
    phone: jidToPhone(jid),
    name: pushName || existing?.name || null,
    country: country?.name || existing?.country || null,
    last_inbound: Date.now(),
    notes: text.slice(0, 500) || (hasImage ? '[imagen recibida]' : ''),
    fu24_sent: 0,
    fu48_sent: 0,
    fu72_done: 0,
  };
  if (isFirstContact) {
    inboundFields.first_contact = Date.now();
    inboundFields.state = 'Nuevo';
    inboundFields.stage = 'new';
  } else if (existing.state === 'Frío') {
    inboundFields.state = 'Interesado'; // re-enganchó, deja de estar frío
  }
  const lead = upsertLead(jid, inboundFields);

  // 1) Esperando usuario/contraseña tras un pago confirmado.
  if (lead.stage === 'awaiting_credentials') {
    if (!text) {
      // Mandó una imagen u otro adjunto: insistimos en que envíe los datos por texto.
      await reply(jid, msg.askCredentials());
      return;
    }
    const updated = await reply(jid, msg.credentialsReceived(), {
      credentials: text.slice(0, 500),
      stage: 'credentials_received',
      state: 'Cerrado',
    });
    await alertOwner(msg.ownerCredentialsAlert(updated, text));
    logger.info({ phone: updated.phone }, '🔐 Credenciales recibidas: alerta para crear panel');
    return;
  }

  // 2) Pide hablar con una persona → handoff y pausa del bot.
  if (isHumanRequest(text)) {
    const updated = await reply(jid, msg.humanReply(), { stage: 'human' });
    await alertOwner(msg.ownerHumanAlert(updated, text));
    logger.info({ phone: updated.phone }, '🙋 Handoff humano solicitado');
    return;
  }

  // 3) Avisa que ya pagó → pedir credenciales + alertar al dueño.
  if (isPaymentDone(text)) {
    const updated = await reply(jid, msg.askCredentials(), {
      stage: 'awaiting_credentials',
      state: 'Cerrado',
      fallback_count: 0,
    });
    await alertOwner(msg.ownerPaymentAlert(updated, text));
    logger.info({ phone: updated.phone }, '💸 Pago reportado');
    return;
  }

  // 4) Señal de cierre: respuesta + datos bancarios + alerta al dueño.
  if (isClosing(text)) {
    const updated = await reply(jid, `${msg.closingReply(country)}\n\n${msg.bankMessage(country)}`, {
      state: 'Interesado',
      stage: 'closing',
      fallback_count: 0,
    });
    await alertOwner(msg.ownerAlert(updated, text));
    logger.info({ phone: updated.phone }, '🔔 Lead caliente: alerta enviada');
    return;
  }

  // 5) Primer contacto: bienvenida.
  if (isFirstContact) {
    await reply(jid, msg.welcome(), { stage: 'welcomed' });
    logger.info({ jid, country: country?.name }, 'Nuevo lead: bienvenida enviada');
    return;
  }

  // 5.1) Respuesta al menú de re-enganche (1 = precios, 2 = hablar con persona).
  if (lead.stage === 'returning_menu') {
    const opt = detectOption(text);
    if (opt === 1) {
      await reply(jid, msg.pricesMessage(), { stage: 'opt2', state: 'Interesado', fallback_count: 0 });
      return;
    }
    if (opt === 2) {
      const updated = await reply(jid, msg.humanReply(), { stage: 'human', fallback_count: 0 });
      await alertOwner(msg.ownerHumanAlert(updated, text));
      return;
    }
    // Si no respondió 1/2, sigue con el resto de intenciones normales.
  }

  // 5.2) Ya había hablado antes y solo saluda: menú de re-enganche.
  if (text && isGreeting(text)) {
    await reply(jid, msg.welcomeBack(lead), { stage: 'returning_menu', fallback_count: 0 });
    logger.info({ jid }, 'Lead recurrente: menú de re-enganche');
    return;
  }

  // 6) Menú: opción 1 (desde cero) → explicación + precios + demo.
  const option = detectOption(text);
  if (option === 1) {
    await reply(jid, msg.option1(), { stage: 'opt1', state: 'Demo', fallback_count: 0 });
    if (getSetting('demo')) await sendText(jid, currentDemo());
    return;
  }
  if (option === 2) {
    await reply(jid, msg.option2(), { stage: 'opt2', state: 'Interesado', fallback_count: 0 });
    return;
  }

  // 7) Pide la demo.
  if (isDemoRequest(text)) {
    await reply(jid, currentDemo(), { state: 'Demo', fallback_count: 0 });
    if (!getSetting('demo')) await alertOwner(`⚠️ Un lead (${lead.phone}) pidió la demo y aún no la configuras con /demo.`);
    return;
  }

  // 8) Pide datos bancarios / a dónde pagar.
  if (isBankRequest(text)) {
    await reply(jid, msg.bankMessage(country), { state: 'Interesado', fallback_count: 0 });
    return;
  }

  // 9) Pregunta por precio en moneda local.
  if (isCurrencyRequest(text, country)) {
    await reply(jid, msg.currencyConversion(country), { fallback_count: 0 });
    return;
  }

  // 9.5) Envió una imagen: intenta leer el comprobante con OCR.
  if (hasImage) {
    const info = media ? await extractPaymentInfo(media, country) : null;
    if (info?.isReceipt && info.amountUsd != null) {
      // Comprobante con monto legible → registra monto y pide credenciales.
      const updated = await reply(jid, msg.paymentReceiptReply(info), {
        stage: 'awaiting_credentials',
        state: 'Cerrado',
        amount_usd: info.amountUsd,
        payment_method: info.method || (info.currency ? `Comprobante ${info.currency}` : 'Comprobante'),
        fallback_count: 0,
      });
      await alertOwner(msg.ownerReceiptAlert(updated, info));
      logger.info({ phone: updated.phone, usd: info.amountUsd }, '📸 Comprobante leído con OCR');
      return;
    }
    // Sin OCR o no se pudo leer el monto → pide escribir "pago realizado".
    const updated = await reply(jid, msg.paymentProofPrompt(), { state: 'Interesado', fallback_count: 0 });
    await alertOwner(msg.ownerImageAlert(updated));
    logger.info({ phone: updated.phone }, '📸 Imagen recibida: posible comprobante');
    return;
  }

  // 10) No entendido: reofrece el menú; tras varios intentos, ofrece un asesor.
  const count = (lead.fallback_count || 0) + 1;
  if (count >= 2) {
    const updated = await reply(jid, msg.humanReply(), { stage: 'human', fallback_count: 0 });
    await alertOwner(msg.ownerHumanAlert(updated, text));
    logger.info({ phone: updated.phone }, '🙋 Escalado a humano tras varios mensajes sin entender');
    return;
  }
  await reply(jid, msg.fallback(), { fallback_count: count });
}
