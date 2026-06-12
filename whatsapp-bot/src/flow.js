// Motor de conversación: decide qué responder a cada mensaje entrante.
import { sendText } from './whatsapp.js';
import { getLead, upsertLead } from './db.js';
import { detectCountry, config } from './config.js';
import { detectOption, isCurrencyRequest, isClosing } from './intents.js';
import * as msg from './messages.js';
import { syncLead } from './notion.js';
import { logger } from './logger.js';

const jidToPhone = (jid) => jid.split('@')[0];

// Envía un mensaje y registra la salida + estado actualizado.
async function reply(jid, text, fields = {}) {
  const lead = upsertLead(jid, { last_outbound: Date.now(), ...fields });
  await sendText(jid, text);
  await syncLead(lead);
  return lead;
}

async function alertOwner(lead, text) {
  if (!config.ownerJid) {
    logger.warn('OWNER_JID no configurado: no se envió alerta de cierre.');
    return;
  }
  await sendText(config.ownerJid, msg.ownerAlert(lead, text));
}

export async function handleMessage(jid, text, pushName) {
  const existing = getLead(jid);
  const isFirstContact = !existing;
  const country = detectCountry(jid);

  // Registra el mensaje entrante y reinicia los relojes de seguimiento.
  const inboundFields = {
    phone: jidToPhone(jid),
    name: pushName || existing?.name || null,
    country: country?.name || existing?.country || null,
    last_inbound: Date.now(),
    notes: text.slice(0, 500),
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
  upsertLead(jid, inboundFields);

  // 1) Señal de cierre: máxima prioridad, alerta al dueño.
  if (isClosing(text)) {
    const lead = await reply(jid, msg.closingReply(country), { state: 'Interesado', stage: 'closing' });
    await alertOwner(lead, text);
    logger.info({ jid, phone: lead.phone }, '🔔 Lead caliente: alerta enviada al dueño');
    return;
  }

  // 2) Primer contacto: mensaje de bienvenida.
  if (isFirstContact) {
    await reply(jid, msg.welcome(), { stage: 'welcomed' });
    logger.info({ jid, country: country?.name }, 'Nuevo lead: bienvenida enviada');
    return;
  }

  // 3) Selección del menú (1 / 2).
  const option = detectOption(text);
  if (option === 1) {
    await reply(jid, msg.option1(), { stage: 'opt1', state: 'Demo' });
    return;
  }
  if (option === 2) {
    await reply(jid, msg.option2(), { stage: 'opt2', state: 'Interesado' });
    return;
  }

  // 4) Pregunta por precio en moneda local.
  if (isCurrencyRequest(text, country)) {
    await reply(jid, msg.currencyConversion(country));
    return;
  }

  // 5) No entendido: reofrece el menú.
  await reply(jid, msg.fallback());
}
