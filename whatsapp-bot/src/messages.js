// Plantillas de mensajes y formateo de precios/monedas.
import { PLANS, GLOBAL_PAYMENTS, LOCAL_PAYMENTS, BANK_DETAILS, getCrypto } from './config.js';

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

// Pregunta qué plan/monto va a comprar.
export const askPlan = () =>
  `🎉 ¡Genial! Vamos a activarte.\n\n` +
  `¿Qué plan vas a tomar? Escríbeme el *monto en USD* (ej: $20, $35.20) ` +
  `o el plan (ej: *45+5 créditos*, *Panel Ilimitado*).`;

export const askPlanAgain = () =>
  `🤔 No capté el plan. Escríbeme el *monto en USD* (ej: $20) ` +
  `o el plan exacto (ej: *100+10 créditos*).`;

// Confirma el plan elegido y entrega los datos de pago.
export function planSelected(plan, country) {
  return (
    `✅ ¡Perfecto! Tomaste *${plan.name}* ($${plan.usd} USD).\n\n` +
    `${bankMessage(country)}\n\n` +
    `📸 Cuando hagas el pago, escríbeme *pago realizado* y te activo tu panel. 🚀`
  );
}

export function ownerPlanAlert(lead, plan) {
  return (
    `🛒 *LEAD ELIGIÓ PLAN*\n\n👤 ${lead.name || 'Sin nombre'}\n📞 ${lead.phone}\n` +
    `🌎 ${lead.country || 'Desconocido'}\n📦 Plan: ${plan.name}\n💰 Monto: $${plan.usd} USD\n\n` +
    `➡️ Está por pagar. Te avisaré cuando confirme el pago.`
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

// Demo del día + apps recomendadas
export function demoMessage(demoText, appsText) {
  return (
    `🎬 *Demo de prueba (válida hoy)*\n\n${demoText}\n\n${appsText}\n\n` +
    `Pruébalo y me cuentas qué te pareció. Cuando quieras, te activo tu panel para revender. 🚀`
  );
}

// Saludo + menú de re-enganche para un lead que ya había hablado antes.
export const welcomeBack = (lead) =>
  `👋 ¡Hola de nuevo${lead?.name ? `, ${lead.name}` : ''}! Qué gusto verte por aquí otra vez.\n\n` +
  `¿Ya te decidiste y quieres empezar con nosotros?\n` +
  `1️⃣ Sí, quiero empezar (te muestro los precios)\n` +
  `2️⃣ Quiero hablar con una persona`;

// Precios completos (para el "1" del menú de re-enganche).
export const pricesMessage = () =>
  `📋 *Nuestros planes:*\n\n${plansBlock()}\n\n` +
  `¿Con cuál quieres empezar? Dime y te paso los datos de pago. 🚀`;

// Respuesta cuando el lead envía una imagen (posible comprobante de pago).
export const paymentProofPrompt = () =>
  `📸 ¡Gracias! Recibí tu imagen. Si es tu *comprobante de pago*, escríbeme las palabras ` +
  `*pago realizado* y enseguida te pido los datos para activar tu panel. 🙌`;

// El OCR detectó un comprobante con monto: confirma y pide credenciales.
export function paymentReceiptReply(info) {
  const local = info.amount != null && info.currency ? ` por *${info.amount} ${info.currency}*` : '';
  const usd = info.amountUsd != null ? ` (≈ $${info.amountUsd} USD)` : '';
  return (
    `📸 ¡Recibí tu comprobante${local}${usd}! 🙌 Gracias.\n\n` +
    `Para activar tu panel, envíame en *un solo mensaje* el *usuario* y la *contraseña* que deseas.\n` +
    `Ejemplo:\n_usuario: juan123_\n_clave: miClave2025_`
  );
}

export function ownerReceiptAlert(lead, info) {
  const local = info.amount != null && info.currency ? `${info.amount} ${info.currency}` : 'monto no detectado';
  const usd = info.amountUsd != null ? ` ≈ $${info.amountUsd} USD` : '';
  return (
    `💸 *COMPROBANTE LEÍDO (OCR)*\n\n👤 ${lead.name || 'Sin nombre'}\n📞 ${lead.phone}\n` +
    `🌎 ${lead.country || 'Desconocido'}\n💰 Monto: ${local}${usd}\n` +
    `🏦 Método: ${info.method || 'no detectado'}\n\n` +
    `➡️ Verifica el comprobante. El bot ya le pidió usuario y contraseña para crear el panel.`
  );
}

export function ownerImageAlert(lead) {
  return (
    `📸 *POSIBLE COMPROBANTE DE PAGO*\n\n👤 ${lead.name || 'Sin nombre'}\n📞 ${lead.phone}\n` +
    `🌎 ${lead.country || 'Desconocido'}\n\n➡️ Revisa la imagen en el chat de WhatsApp.`
  );
}

// Datos bancarios según país (+ pagos internacionales).
export function bankMessage(country) {
  const local = country && BANK_DETAILS[country.code];
  const header = `💳 *Datos para tu pago*\n`;
  if (local) {
    return `${header}\n${local}\n\n${getCrypto()}\n\n📸 Cuando transfieras, envíame el comprobante por aquí.`;
  }
  return `${header}\n${getCrypto()}\n\n📸 Cuando pagues, envíame el comprobante por aquí.`;
}

// Conexión con un asesor humano.
export const humanReply = () =>
  `👨‍💼 ¡Claro que sí! Te conecto con uno de nuestros asesores.\n` +
  `En unos minutos una persona del equipo continúa contigo por aquí. 🙌\n` +
  `Mientras tanto, puedes dejarme tu consulta y la verá el asesor.`;

// Tras confirmar pago: pedir usuario/contraseña deseados.
export const askCredentials = () =>
  `🙌 *¡Pago recibido, gracias!* Ya casi tienes tu panel.\n\n` +
  `Para crearlo, envíame en *un solo mensaje* el *usuario* y la *contraseña* que deseas.\n` +
  `Ejemplo:\n_usuario: juan123_\n_clave: miClave2025_`;

// Confirmación tras recibir las credenciales.
export const credentialsReceived = () =>
  `✅ ¡Listo! Recibí tus datos. Estoy creando tu panel y en unos minutos te entrego el acceso. 🚀`;

// --- Alertas internas al dueño ---
export function ownerPaymentAlert(lead, text) {
  return (
    `💸 *PAGO REPORTADO*\n\n👤 ${lead.name || 'Sin nombre'}\n📞 ${lead.phone}\n` +
    `🌎 ${lead.country || 'Desconocido'}\n💬 "${text}"\n\n` +
    `➡️ Verifica el comprobante. El bot ya le pidió usuario y contraseña.`
  );
}

export function ownerCredentialsAlert(lead, creds) {
  return (
    `🔐 *CREAR PANEL — credenciales recibidas*\n\n👤 ${lead.name || 'Sin nombre'}\n📞 ${lead.phone}\n` +
    `🌎 ${lead.country || 'Desconocido'}\n\n📝 Datos que pidió el cliente:\n${creds}\n\n` +
    `➡️ Crea el panel manualmente y entrégale el acceso.`
  );
}

export function ownerHumanAlert(lead, text) {
  return (
    `🙋 *LEAD PIDE HABLAR CON UNA PERSONA*\n\n👤 ${lead.name || 'Sin nombre'}\n📞 ${lead.phone}\n` +
    `🌎 ${lead.country || 'Desconocido'}\n💬 "${text}"\n\n` +
    `➡️ El bot quedó *en pausa* para este lead. Responde tú directamente.\n` +
    `Para reactivar el bot con él: \`/resume ${lead.phone}\``
  );
}

// Fallback cuando no entendemos el mensaje
export const fallback = () =>
  `🤔 No estoy seguro de haber entendido. Para ayudarte mejor, responde:\n` +
  `1️⃣ Quiero iniciar desde cero\n` +
  `2️⃣ Ya vendo y quiero más clientes\n\n` +
  `O escríbeme tu pregunta sobre *precios* o *formas de pago*.`;
