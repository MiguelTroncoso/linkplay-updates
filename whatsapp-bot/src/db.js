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

// Tabla clave/valor para ajustes editables en caliente (demo del día, apps...).
db.exec(`CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);`);

// Contactos a ignorar: números ya guardados en tu agenda + ignorados manualmente.
// Si ignored = 1, el bot NO responde a ese número (no es un lead de la campaña).
db.exec(`CREATE TABLE IF NOT EXISTS contacts (jid TEXT PRIMARY KEY, name TEXT, ignored INTEGER DEFAULT 1);`);

// Migración suave: agrega columnas nuevas si la tabla ya existía.
for (const col of ['fallback_count INTEGER DEFAULT 0', 'credentials TEXT']) {
  try {
    db.exec(`ALTER TABLE leads ADD COLUMN ${col};`);
  } catch {
    /* la columna ya existe */
  }
}

export function getSetting(key, fallback = null) {
  const row = db.prepare('SELECT value FROM settings WHERE key = ?').get(key);
  return row ? row.value : fallback;
}

export function setSetting(key, value) {
  db.prepare(
    'INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value'
  ).run(key, value);
}

// Marca un contacto guardado de la agenda (no flipea un ajuste manual previo).
export function rememberSavedContact(jid, name = null) {
  db.prepare(
    `INSERT INTO contacts (jid, name, ignored) VALUES (?, ?, 1)
     ON CONFLICT(jid) DO UPDATE SET name = COALESCE(excluded.name, contacts.name)`
  ).run(jid, name);
}

// Ignora/activa manualmente un número (comandos /ignore y /unignore).
export function setIgnored(jid, ignored, name = null) {
  db.prepare(
    `INSERT INTO contacts (jid, name, ignored) VALUES (?, ?, ?)
     ON CONFLICT(jid) DO UPDATE SET ignored = excluded.ignored`
  ).run(jid, name, ignored ? 1 : 0);
}

export function isIgnored(jid) {
  const row = db.prepare('SELECT ignored FROM contacts WHERE jid = ?').get(jid);
  return row ? row.ignored === 1 : false;
}

export function countIgnored() {
  return db.prepare('SELECT COUNT(*) AS n FROM contacts WHERE ignored = 1').get().n;
}

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
