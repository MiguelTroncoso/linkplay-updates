// Detección de intenciones a partir del texto del lead.
const normalize = (t) =>
  t
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '') // quita acentos
    .trim();

// Opción del menú de bienvenida (1 o 2).
export function detectOption(text) {
  const t = normalize(text);
  const first = t.replace(/[^0-9a-z]/g, ' ').trim().split(/\s+/)[0];
  if (first === '1' || first === 'uno' || /iniciar desde cero|empezar de cero|desde cero/.test(t)) {
    return 1;
  }
  if (first === '2' || first === 'dos' || /ya vendo|mas clientes|quiero mas clientes/.test(t)) {
    return 2;
  }
  return null;
}

// El lead pide precios en su moneda local / pregunta cuánto cuesta.
export function isCurrencyRequest(text, country) {
  const t = normalize(text);
  const localMoney = /(peso|pesos|clp|mxn|cop|sol|soles|pen|boliviano|bolivianos|\bbs\b|moneda local|en mi moneda|cuanto en|cuanto sale en)/;
  if (localMoney.test(t)) return true;
  // Si pregunta por precio y el país no usa USD, respondemos en su moneda.
  const priceIntent = /(precio|precios|cuanto cuesta|cuanto vale|cuanto sale|cuanto es|cuanto cobran|valor)/;
  if (priceIntent.test(t) && country && country.currency !== 'USD') return true;
  return false;
}

// Señales de cierre que disparan alerta al dueño.
const CLOSING_PATTERNS = [
  /\bsi quiero\b/, /\bsi,? quiero\b/, /\blo quiero\b/, /\bquiero comprar\b/, /\bquiero empezar\b/,
  /cuando empezamos/, /cuando comenzamos/, /\bempecemos\b/, /\bdame acceso\b/, /\bquiero el panel\b/,
  /como pago/, /donde pago/, /como compro/, /listo para pagar/, /quiero pagar/, /como lo adquiero/,
];
export function isClosing(text) {
  const t = normalize(text);
  return CLOSING_PATTERNS.some((re) => re.test(t));
}
