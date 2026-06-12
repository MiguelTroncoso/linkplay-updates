// Persistencia local en SQLite. Guarda el estado de cada lead para programar
// seguimientos, evitar duplicados y sincronizar con Notion.
import Database from 'better-sqlite3';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const db = new Database(join(__dirname, '..', 'leads.db'));
db.pragma('journal_mode = WAL');

db.exec(`
  CREATE TABLE IF NOT EXISTS leads (
    jid            TEXT PRIMARY KEY,
    phone          TEXT,
    name           TEXT,
    country        TEXT,
    first_contact  INTEGER,
    last_inbound   INTEGER,
    last_outbound  INTEGER,
    state          TEXT DEFAULT 'Nuevo',
    stage          TEXT DEFAULT 'new',
    plan           TEXT,
    amount_usd     REAL,
    payment_method TEXT,
    notes          TEXT,
    fu24_sent      INTEGER DEFAULT 0,
    fu48_sent      INTEGER DEFAULT 0,
    fu72_done      INTEGER DEFAULT 0,
    notion_page_id TEXT
  );
`);

export function getLead(jid) {
  return db.prepare('SELECT * FROM leads WHERE jid = ?').get(jid);
}

export function upsertLead(jid, fields) {
  const existing = getLead(jid);
  if (!existing) {
    const cols = ['jid', ...Object.keys(fields)];
    const placeholders = cols.map(() => '?').join(', ');
    db.prepare(`INSERT INTO leads (${cols.join(', ')}) VALUES (${placeholders})`).run(
      jid,
      ...Object.values(fields)
    );
    return getLead(jid);
  }
  const sets = Object.keys(fields).map((k) => `${k} = ?`).join(', ');
  db.prepare(`UPDATE leads SET ${sets} WHERE jid = ?`).run(...Object.values(fields), jid);
  return getLead(jid);
}

// Leads candidatos a seguimiento: no cerrados, no fríos, con contacto previo.
export function leadsForFollowup() {
  return db
    .prepare(
      `SELECT * FROM leads
       WHERE state NOT IN ('Cerrado', 'Frío')
         AND last_inbound IS NOT NULL`
    )
    .all();
}

export function allLeads() {
  return db.prepare('SELECT * FROM leads ORDER BY first_contact DESC').all();
}

export default db;
