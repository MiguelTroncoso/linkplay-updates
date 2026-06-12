// Configuración central del negocio: planes, precios, monedas y métodos de pago.
// Edita este archivo para actualizar precios o tasas de cambio sin tocar la lógica.

export const config = {
  ownerJid: process.env.OWNER_JID || '',
  notionToken: process.env.NOTION_TOKEN || '',
  notionDatabaseId: process.env.NOTION_DATABASE_ID || '',
  minTypingMs: Number(process.env.MIN_TYPING_MS || 1200),
  maxTypingMs: Number(process.env.MAX_TYPING_MS || 3000),
};

// Números a ignorar manualmente desde el arranque (además de tus contactos guardados).
// Útil para los que ya te escribieron antes de activar el bot. Coma-separados, sin '+'.
export const IGNORE_NUMBERS = (process.env.IGNORE_NUMBERS || '')
  .split(',')
  .map((s) => s.replace(/\D/g, ''))
  .filter(Boolean)
  .map((n) => `${n}@s.whatsapp.net`);

// --- Planes y precios en USD ---
export const PLANS = {
  resellers: [
    { name: '10+2 Créditos', usd: 20 },
    { name: '20+4 Créditos', usd: 35.2 },
    { name: '45+5 Créditos', usd: 49.5 },
    { name: '100+10 Créditos', usd: 77 },
  ],
  superResellers: [
    { name: '1500 Créditos', usd: 165 },
    { name: '2000 Créditos', usd: 198 },
    { name: '2500 Créditos', usd: 220 },
    { name: '5000 Créditos', usd: 350 },
  ],
  ilimitados: [
    { name: 'Panel Ilimitado (mensual)', usd: 200 },
    { name: 'Panel Ilimitado Admin (mensual)', usd: 400 },
  ],
};

// --- Países soportados (detectados por código telefónico) ---
// El orden importa: los códigos más largos van primero para evitar colisiones.
export const COUNTRIES = {
  '593': { code: 'EC', name: 'Ecuador', currency: 'USD', rate: 1, symbol: '$' },
  '591': { code: 'BO', name: 'Bolivia', currency: 'BS', rate: 6.96, symbol: 'Bs' },
  '503': { code: 'SV', name: 'El Salvador', currency: 'USD', rate: 1, symbol: '$' },
  '57': { code: 'CO', name: 'Colombia', currency: 'COP', rate: 4000, symbol: '$' },
  '56': { code: 'CL', name: 'Chile', currency: 'CLP', rate: 810, symbol: '$' },
  '52': { code: 'MX', name: 'México', currency: 'MXN', rate: 16.8, symbol: '$' },
  '51': { code: 'PE', name: 'Perú', currency: 'PEN', rate: 3.7, symbol: 'S/' },
};

// --- Métodos de pago por país (además de los globales) ---
export const GLOBAL_PAYMENTS = 'USDT (Binance), PayPal o Western Union';
export const LOCAL_PAYMENTS = {
  CL: 'Transferencia bancaria CLP',
  MX: 'SPEI / transferencia MXN',
  CO: 'Nequi o Bancolombia (COP)',
  EC: 'Transferencia en USD',
  BO: 'Transferencia en BS',
  PE: 'Yape / Plin / transferencia PEN',
  SV: 'Transferencia en USD',
};

// --- Datos bancarios / de pago por país ---
// ✏️ EDITA estos textos con tus datos reales. Soporta varias líneas.
// El bot los envía cuando el lead va a pagar (según su país).
export const BANK_DETAILS = {
  CL: `🏦 *Chile (CLP)*
Banco: [TU BANCO]
Tipo de cuenta: [Cuenta Corriente/Vista]
N° de cuenta: [NÚMERO]
RUT: [TU RUT]
Nombre: [TITULAR]
Correo: [CORREO]`,
  MX: `🏦 *México (MXN — SPEI)*
Banco: [TU BANCO]
CLABE: [18 DÍGITOS]
N° de tarjeta: [OPCIONAL]
Titular: [NOMBRE]`,
  CO: `🏦 *Colombia (COP)*
Nequi: [NÚMERO]
Bancolombia — Ahorros N°: [NÚMERO]
Titular: [NOMBRE]
Cédula: [NÚMERO]`,
  PE: `🏦 *Perú (PEN)*
Yape / Plin: [NÚMERO]
Banco (BCP/Interbank): [CUENTA]
CCI: [NÚMERO]
Titular: [NOMBRE]`,
  BO: `🏦 *Bolivia (BS)*
Banco: [TU BANCO]
N° de cuenta: [NÚMERO]
Titular: [NOMBRE]
CI: [NÚMERO]`,
  EC: `🏦 *Ecuador (USD)*
Banco: [TU BANCO]
Tipo de cuenta: [Ahorros/Corriente]
N° de cuenta: [NÚMERO]
Titular: [NOMBRE]
Cédula: [NÚMERO]`,
  SV: `🏦 *El Salvador (USD)*
Banco: [TU BANCO]
N° de cuenta: [NÚMERO]
Titular: [NOMBRE]
DUI: [NÚMERO]`,
};

// Pagos globales (USDT/PayPal/WU). ✏️ Completa con tus datos reales.
export const CRYPTO_PAYMENTS = `🌎 *Pagos internacionales*
💰 USDT (red TRC20/Binance): [TU WALLET o BinancePay ID]
💳 PayPal: [TU CORREO PAYPAL]
🏧 Western Union: a nombre de [NOMBRE] — [CIUDAD, PAÍS]`;

// --- Demo y apps por defecto (se sobreescriben con /demo y /apps) ---
// El dueño cambia la demo cada mañana enviando "/demo ..." al bot.
export const DEFAULT_DEMO =
  '⚠️ La demo del día aún no está configurada. Escríbeme y te la activo en minutos.';
export const DEFAULT_APPS = `📲 *Apps recomendadas*
• Android / TV Box / Fire Stick: *IPTV Smarters Pro* o *XCIPTV*
• Smart TV Samsung/LG: *Smart STB* o *SS IPTV*
• iPhone / iPad: *Smarters Player Lite*
• PC/Windows: *VLC* o *MyIPTV Player*`;

// Convierte un monto en moneda local a USD usando las tasas de COUNTRIES.
export function toUsd(amount, currency) {
  if (!amount || !currency) return null;
  if (currency === 'USD') return Math.round(amount * 100) / 100;
  for (const c of Object.values(COUNTRIES)) {
    if (c.currency === currency) return Math.round((amount / c.rate) * 100) / 100;
  }
  return null;
}

// Detecta el país a partir del número (JID o E.164 sin '+').
export function detectCountry(numberOrJid) {
  const digits = String(numberOrJid).replace(/\D/g, '');
  // México móvil suele venir como 521XXXXXXXXXX -> normalizamos a 52
  const normalized = digits.startsWith('521') ? '52' + digits.slice(3) : digits;
  for (const codeKey of ['593', '591', '503', '57', '56', '52', '51']) {
    if (normalized.startsWith(codeKey)) return COUNTRIES[codeKey];
  }
  return null;
}
