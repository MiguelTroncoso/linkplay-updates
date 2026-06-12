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

// El lead avisa que ya realizó el pago.
const PAYMENT_DONE = [
  /\bya pague\b/, /\bya pague\b/, /ya hice el pago/, /ya realice el pago/, /ya transfer/,
  /\btransferi\b/, /hice la transferencia/, /pago realizado/, /pago hecho/, /\blisto pague\b/,
  /envie el comprobante/, /aqui el comprobante/, /adjunto comprobante/, /ya deposite/, /\bya envie el pago\b/,
];
export function isPaymentDone(text) {
  const t = normalize(text);
  return PAYMENT_DONE.some((re) => re.test(t));
}

// El lead quiere hablar con una persona real.
const HUMAN_PATTERNS = [
  /hablar con (una |alguien|un )?(persona|humano|asesor|agente|alguien|vendedor|ejecutivo)/,
  /atencion (humana|personal|de una persona)/, /\bun asesor\b/, /\bpersona real\b/,
  /me pueden? llamar/, /quiero hablar con/, /\bagente\b/, /\bsoporte\b/, /\bayuda humana\b/,
];
export function isHumanRequest(text) {
  const t = normalize(text);
  return HUMAN_PATTERNS.some((re) => re.test(t));
}

// El lead pide la demo / quiere probar.
const DEMO_PATTERNS = [
  /\bdemo\b/, /quiero probar/, /puedo probar/, /una prueba/, /probar el servicio/,
  /probarlo/, /pruebame/, /quiero ver/, /me lo muestras/, /tienen prueba/,
];
export function isDemoRequest(text) {
  const t = normalize(text);
  return DEMO_PATTERNS.some((re) => re.test(t));
}

// El lead pide datos bancarios / a dónde transferir.
const BANK_PATTERNS = [
  /datos bancarios/, /datos de pago/, /numero de cuenta/, /\bcuenta bancaria\b/,
  /a donde (transfiero|pago|deposito|envio)/, /donde (transfiero|deposito|consigno)/,
  /\bnequi\b/, /\byape\b/, /\bplin\b/, /\bclabe\b/, /\bspei\b/, /\bcci\b/,
  /a que cuenta/, /pasame (la cuenta|los datos)/, /tus datos para pagar/,
];
export function isBankRequest(text) {
  const t = normalize(text);
  return BANK_PATTERNS.some((re) => re.test(t));
}
