import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino/file',
    options: { destination: 1 }, // stdout
  },
});

// Logger silencioso para Baileys (muy verboso por defecto).
export const waLogger = pino({ level: 'silent' });
