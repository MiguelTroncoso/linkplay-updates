// Seguimiento automático de leads inactivos: 24h (suave), 48h (urgencia), 72h (frío).
import cron from 'node-cron';
import { sendText } from './whatsapp.js';
import { leadsForFollowup, upsertLead } from './db.js';
import { config } from './config.js';
import * as msg from './messages.js';
import { syncLead } from './notion.js';
import { logger } from './logger.js';

const HOUR = 3600 * 1000;

export async function runFollowups() {
  const now = Date.now();
  let sent24 = 0, sent48 = 0, frozen = 0;

  for (const lead of leadsForFollowup()) {
    if (lead.jid === config.ownerJid) continue;
    const hours = (now - lead.last_inbound) / HOUR;

    if (hours >= 72 && !lead.fu72_done) {
      const updated = upsertLead(lead.jid, { state: 'Frío', fu72_done: 1 });
      await syncLead(updated);
      frozen++;
    } else if (hours >= 48 && !lead.fu48_sent) {
      await sendText(lead.jid, msg.followup48());
      const updated = upsertLead(lead.jid, { fu48_sent: 1, last_outbound: now });
      await syncLead(updated);
      sent48++;
    } else if (hours >= 24 && !lead.fu24_sent) {
      await sendText(lead.jid, msg.followup24());
      const updated = upsertLead(lead.jid, { fu24_sent: 1, last_outbound: now });
      await syncLead(updated);
      sent24++;
    }
  }

  if (sent24 || sent48 || frozen) {
    logger.info({ sent24, sent48, frozen }, 'Ciclo de seguimiento completado');
  }
}

// Programa el chequeo cada hora (minuto 0).
export function scheduleFollowups() {
  cron.schedule('0 * * * *', () => {
    runFollowups().catch((err) => logger.error({ err: err.message }, 'Error en seguimiento'));
  }, { timezone: process.env.TZ || 'America/Santiago' });
  logger.info('⏰ Seguimiento automático programado (cada hora)');
}
