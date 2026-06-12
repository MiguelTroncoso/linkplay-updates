// Comandos que SOLO el dueño (OWNER_JID) puede enviar al bot por WhatsApp.
import { sendText } from './whatsapp.js';
import { getSetting, setSetting, getLead, upsertLead, allLeads } from './db.js';
import { DEFAULT_DEMO, DEFAULT_APPS } from './config.js';
import { logger } from './logger.js';

const phoneToJid = (num) => `${String(num).replace(/\D/g, '')}@s.whatsapp.net`;

const HELP = `🛠️ *Comandos del dueño*

/demo            → muestra la demo actual
/demo <texto>    → actualiza la demo del día (links/credenciales)
/apps            → muestra las apps recomendadas
/apps <texto>    → actualiza las apps recomendadas
/pause <número>  → pausa el bot para ese lead (lo atiendes tú)
/resume <número> → reactiva el bot para ese lead
/stats           → resumen de leads por estado
/help            → muestra esta ayuda`;

// Devuelve true si el mensaje era un comando del dueño (y ya fue atendido).
export async function handleOwnerCommand(jid, text) {
  if (!text.startsWith('/')) return false;

  const [cmd, ...rest] = text.trim().split(/\s+/);
  const arg = text.slice(text.indexOf(cmd) + cmd.length).trim(); // conserva saltos de línea

  switch (cmd.toLowerCase()) {
    case '/help':
      await sendText(jid, HELP);
      break;

    case '/demo':
      if (!arg) {
        await sendText(jid, `🎬 *Demo actual:*\n\n${getSetting('demo', DEFAULT_DEMO)}`);
      } else {
        setSetting('demo', arg);
        await sendText(jid, '✅ Demo del día actualizada. Se enviará a los leads que la pidan.');
        logger.info('Demo actualizada por el dueño');
      }
      break;

    case '/apps':
      if (!arg) {
        await sendText(jid, `📲 *Apps actuales:*\n\n${getSetting('apps', DEFAULT_APPS)}`);
      } else {
        setSetting('apps', arg);
        await sendText(jid, '✅ Apps recomendadas actualizadas.');
      }
      break;

    case '/pause': {
      if (!rest[0]) return await sendText(jid, 'Uso: /pause <número con código de país>'), true;
      const target = phoneToJid(rest[0]);
      upsertLead(target, { stage: 'human' });
      await sendText(jid, `⏸️ Bot pausado para ${rest[0]}. Atiéndelo tú.`);
      break;
    }

    case '/resume': {
      if (!rest[0]) return await sendText(jid, 'Uso: /resume <número con código de país>'), true;
      const target = phoneToJid(rest[0]);
      const lead = getLead(target);
      if (!lead) return await sendText(jid, 'No encuentro ese lead.'), true;
      upsertLead(target, { stage: 'welcomed' });
      await sendText(jid, `▶️ Bot reactivado para ${rest[0]}.`);
      break;
    }

    case '/stats': {
      const leads = allLeads();
      const by = leads.reduce((acc, l) => ((acc[l.state] = (acc[l.state] || 0) + 1), acc), {});
      const lines = Object.entries(by).map(([s, n]) => `• ${s}: ${n}`).join('\n') || 'Sin leads aún.';
      await sendText(jid, `📊 *Leads (${leads.length} total)*\n${lines}`);
      break;
    }

    default:
      await sendText(jid, `❓ Comando no reconocido.\n\n${HELP}`);
  }
  return true;
}
