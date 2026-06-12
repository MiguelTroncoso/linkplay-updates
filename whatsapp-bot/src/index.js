// Punto de entrada del bot: conecta WhatsApp y arranca el seguimiento automático.
import { startWhatsApp } from './whatsapp.js';
import { handleMessage } from './flow.js';
import { scheduleFollowups, runFollowups } from './followup.js';
import { setIgnored } from './db.js';
import { IGNORE_NUMBERS } from './config.js';
import { logger } from './logger.js';

async function main() {
  logger.info('🤖 Iniciando bot IPTV LATAM...');

  // Carga la lista manual de números a ignorar (de IGNORE_NUMBERS en .env).
  for (const jid of IGNORE_NUMBERS) setIgnored(jid, true);
  if (IGNORE_NUMBERS.length) logger.info({ n: IGNORE_NUMBERS.length }, 'Números en lista de ignorados (.env)');

  await startWhatsApp(handleMessage);
  scheduleFollowups();

  // Chequeo inicial de seguimientos al arrancar (por si el bot estuvo caído).
  setTimeout(() => runFollowups().catch((e) => logger.error({ err: e.message })), 15000);
}

process.on('uncaughtException', (err) => logger.error({ err: err.message }, 'uncaughtException'));
process.on('unhandledRejection', (err) => logger.error({ err: String(err) }, 'unhandledRejection'));

main().catch((err) => {
  logger.error({ err: err.message }, 'Fallo al iniciar');
  process.exit(1);
});
