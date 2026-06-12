// Sincronización de leads con Notion. Es opcional: si no hay token configurado,
// las funciones no hacen nada y el bot sigue operando normal.
import { Client } from '@notionhq/client';
import { config } from './config.js';
import { logger } from './logger.js';
import db from './db.js';

const enabled = Boolean(config.notionToken && config.notionDatabaseId);
const notion = enabled ? new Client({ auth: config.notionToken }) : null;

if (!enabled) {
  logger.warn('Notion deshabilitado (faltan NOTION_TOKEN o NOTION_DATABASE_ID). El bot funcionará sin registrar en Notion.');
}

const txt = (v) => (v ? [{ text: { content: String(v).slice(0, 1900) } }] : []);

function buildProperties(lead) {
  const props = {
    Nombre: { title: txt(lead.name || lead.phone) },
    Número: { rich_text: txt(lead.phone) },
    Estado: { select: { name: lead.state || 'Nuevo' } },
  };
  if (lead.country) props.País = { select: { name: lead.country } };
  if (lead.first_contact) props['Primer contacto'] = { date: { start: new Date(lead.first_contact).toISOString() } };
  if (lead.plan) props.Plan = { rich_text: txt(lead.plan) };
  if (lead.amount_usd != null) props['Monto USD'] = { number: lead.amount_usd };
  if (lead.payment_method) props['Método de pago'] = { rich_text: txt(lead.payment_method) };
  if (lead.notes) props.Notas = { rich_text: txt(lead.notes) };
  return props;
}

// Crea o actualiza la página del lead en Notion y guarda el page_id localmente.
export async function syncLead(lead) {
  if (!enabled) return;
  try {
    const properties = buildProperties(lead);
    if (lead.notion_page_id) {
      await notion.pages.update({ page_id: lead.notion_page_id, properties });
    } else {
      const page = await notion.pages.create({
        parent: { database_id: config.notionDatabaseId },
        properties,
      });
      db.prepare('UPDATE leads SET notion_page_id = ? WHERE jid = ?').run(page.id, lead.jid);
    }
  } catch (err) {
    logger.error({ err: err.message, jid: lead.jid }, 'Error sincronizando con Notion');
  }
}
