// Plantillas de mensajes y formateo de precios/monedas.
import { PLANS, GLOBAL_PAYMENTS, LOCAL_PAYMENTS } from './config.js';

const fmtUsd = (n) => `$${Number.isInteger(n) ? n : n.toFixed(2)} USD`;

function plansBlock() {
  const r = PLANS.resellers.map((p) => `• ${p.name} — ${fmtUsd(p.usd)}`).join('\n');
  const sr = PLANS.superResellers.map((p) => `• ${p.name} — ${fmtUsd(p.usd)}`).join('\n');
  const il = PLANS.ilimitados.map((p) => `• ${p.name} — ${fmtUsd(p.usd)}`).join('\n');
  return (
    `📦 *Panel Resellers*\n${r}\n\n` +
    `🚀 *Panel Super Resellers*\n${sr}\n\n` +
    `♾️ *Paneles Ilimitados Mensuales*\n${il}`
  );
}

// Mensaje 1 — Bienvenida automática
export const welcome = () =>
  `👋 ¡Hola! Gracias por contactarnos.\n` +
  `Somos una plataforma de Televisión Digital con contenido para toda LATAM.\n\n` +
  `📺 Más de 3.000 canales\n` +
  `🎬 Más de 15.000 películas y series\n` +
  `⚽ Deportes internacionales en vivo\n\n` +
  `💼 Tú compras créditos mayoristas y los revendes a $4-8 USD/mes.\n\n` +
  `¿Con cuál opción te identificas?\n` +
  `1️⃣ Quiero iniciar desde cero\n` +
  `2️⃣ Ya vendo y quiero más clientes`;

// Opción 1 — explicación + precios + demo
export const option1 = () =>
  `🙌 ¡Excelente! Empezar es muy fácil, no necesitas experiencia previa.\n\n` +
  `Funciona así:\n` +
  `1. Compras un panel de créditos mayoristas.\n` +
  `2. Cada crédito = 1 cuenta de 1 mes para un cliente.\n` +
  `3. Tú revendes cada cuenta a $4-8 USD/mes y te quedas la diferencia.\n\n` +
  `Estos son nuestros planes:\n\n${plansBlock()}\n\n` +
  `🎁 Te puedo activar una *demo gratis* para que pruebes el servicio en tu pantalla. ` +
  `¿Te la genero? Dime en qué dispositivo la verías (TV, celular, TV Box).`;

// Opción 2 — precios directos + pregunta de volumen
export const option2 = () =>
  `💪 ¡Perfecto! Si ya vendes, lo que te conviene es escalar con más créditos a mejor costo.\n\n` +
  `Estos son nuestros planes mayoristas:\n\n${plansBlock()}\n\n` +
  `Para recomendarte el panel ideal: *¿cuántos clientes manejas actualmente?* 👇`;

// Seguimiento 24h — suave
export const followup24 = () =>
  `👋 ¡Hola de nuevo! Vi que quedaste interesado en nuestros paneles IPTV.\n` +
  `¿Te quedó alguna duda? Estoy aquí para ayudarte a empezar a vender. 📺`;

// Seguimiento 48h — urgencia / promoción
export const followup48 = () =>
  `⏳ Última oportunidad: esta semana tenemos *créditos de regalo* en los paneles de reseller.\n` +
  `Si activas hoy, te ayudo a configurar todo y arrancas vendiendo de inmediato. 🚀\n` +
  `¿Lo activamos?`;

// Conversión a moneda local
export function currencyConversion(country) {
  if (!country || country.currency === 'USD') {
    return (
      `💵 En tu país los precios se manejan directamente en *USD*.\n\n${plansBlock()}\n\n` +
      `Puedes pagar con ${GLOBAL_PAYMENTS}.`
    );
  }
  const { name, currency, rate, symbol } = country;
  const conv = (usd) => {
    const local = usd * rate;
    const rounded = currency === 'PEN' || currency === 'BS' ? local.toFixed(2) : Math.round(local).toLocaleString('es');
    return `${symbol}${rounded} ${currency}`;
  };
  const lines = PLANS.resellers
    .map((p) => `• ${p.name} — ${fmtUsd(p.usd)} ≈ ${conv(p.usd)}`)
    .join('\n');
  const pay = LOCAL_PAYMENTS[country.code] || GLOBAL_PAYMENTS;
  return (
    `💱 Tasa de referencia: 1 USD ≈ ${symbol}${rate.toLocaleString('es')} ${currency} (${name}).\n\n` +
    `*Panel Resellers en tu moneda:*\n${lines}\n\n` +
    `💳 Puedes pagar con: ${pay}, o también ${GLOBAL_PAYMENTS}.`
  );
}

// Respuesta cuando el lead da señales de cierre
export function closingReply(country) {
  const pay = country ? LOCAL_PAYMENTS[country.code] || GLOBAL_PAYMENTS : GLOBAL_PAYMENTS;
  return (
    `🎉 ¡Genial! Vamos a activarte el acceso ahora mismo.\n\n` +
    `Métodos de pago disponibles para ti: ${pay}, o también ${GLOBAL_PAYMENTS}.\n\n` +
    `En un momento un asesor te confirma los datos y te entrega tu panel. 🙌`
  );
}

// Alerta interna al dueño
export function ownerAlert(lead, text) {
  return (
    `🔔 *LEAD CALIENTE — posible cierre*\n\n` +
    `👤 ${lead.name || 'Sin nombre'}\n` +
    `📞 ${lead.phone}\n` +
    `🌎 ${lead.country || 'País desconocido'}\n` +
    `📌 Estado: ${lead.state}\n` +
    `💬 Dijo: "${text}"\n\n` +
    `➡️ Contáctalo para cerrar la venta.`
  );
}

// Fallback cuando no entendemos el mensaje
export const fallback = () =>
  `🤔 No estoy seguro de haber entendido. Para ayudarte mejor, responde:\n` +
  `1️⃣ Quiero iniciar desde cero\n` +
  `2️⃣ Ya vendo y quiero más clientes\n\n` +
  `O escríbeme tu pregunta sobre *precios* o *formas de pago*.`;
