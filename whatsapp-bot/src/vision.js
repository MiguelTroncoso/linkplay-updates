// OCR de comprobantes de pago con Claude (visión). Es opcional: si no hay
// ANTHROPIC_API_KEY, las funciones devuelven null y el bot sigue funcionando.
import Anthropic from '@anthropic-ai/sdk';
import { toUsd } from './config.js';
import { logger } from './logger.js';

const enabled = Boolean(process.env.ANTHROPIC_API_KEY);
const client = enabled ? new Anthropic() : null;

if (!enabled) {
  logger.warn('OCR de comprobantes deshabilitado (falta ANTHROPIC_API_KEY).');
}

// Normaliza el mimetype al formato que acepta la API de imágenes.
function mediaType(mimetype = '') {
  if (mimetype.includes('png')) return 'image/png';
  if (mimetype.includes('webp')) return 'image/webp';
  if (mimetype.includes('gif')) return 'image/gif';
  return 'image/jpeg';
}

const PROMPT =
  'Eres un asistente que lee comprobantes de pago/transferencias bancarias de LATAM. ' +
  'Analiza la imagen y responde SOLO con un objeto JSON válido, sin texto extra, con esta forma:\n' +
  '{"is_receipt": boolean, "amount": number|null, "currency": "CLP"|"MXN"|"COP"|"PEN"|"BS"|"USD"|null, "method": string|null}\n' +
  '- is_receipt: true solo si la imagen es un comprobante/recibo de pago o transferencia.\n' +
  '- amount: el monto total pagado (solo el número, sin símbolos ni separadores de miles).\n' +
  '- currency: la moneda detectada (códigos de arriba) o null si no es claro.\n' +
  '- method: banco o método (ej. "Yape", "Nequi", "SPEI", "Transferencia") o null.';

// Recibe { buffer, mimetype } y el país del lead. Devuelve datos del comprobante o null.
export async function extractPaymentInfo(media, country) {
  if (!enabled || !media?.buffer) return null;
  try {
    const resp = await client.messages.create({
      model: 'claude-haiku-4-5',
      max_tokens: 300,
      messages: [
        {
          role: 'user',
          content: [
            { type: 'image', source: { type: 'base64', media_type: mediaType(media.mimetype), data: media.buffer.toString('base64') } },
            { type: 'text', text: PROMPT },
          ],
        },
      ],
    });
    const text = resp.content.find((b) => b.type === 'text')?.text || '';
    const json = JSON.parse(text.replace(/```json|```/g, '').trim());
    if (!json.is_receipt) return { isReceipt: false };

    // Si no detectó moneda, usa la del país del lead.
    const currency = json.currency || country?.currency || null;
    const amountUsd = toUsd(json.amount, currency);
    return {
      isReceipt: true,
      amount: json.amount ?? null,
      currency,
      amountUsd,
      method: json.method || null,
    };
  } catch (err) {
    logger.error({ err: err.message }, 'Error leyendo el comprobante con OCR');
    return null;
  }
}
