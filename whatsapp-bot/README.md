# 🤖 Bot WhatsApp B2B — IPTV LATAM (Resellers)

Bot de WhatsApp para captar y dar seguimiento a revendedores de la plataforma de
Televisión Digital. Construido con **Baileys** (WhatsApp Web, gratis) + **SQLite**
+ **Notion**, pensado para correr en un VPS de 4GB con **PM2**.

## ✨ Funciones

1. **Respuesta automática** con menú de bienvenida (opción 1: desde cero / opción 2: ya vende).
2. **Seguimiento automático**: 24h (suave), 48h (urgencia/promo), 72h (marca lead frío).
3. **Conversión de moneda** cuando el lead pregunta el precio en su moneda local
   (CLP, MXN, COP, PEN, BS; Ecuador y El Salvador en USD).
4. **Registro automático en Notion** (nombre, país, fecha, estado, plan, monto, pago, notas).
5. **Alerta al dueño** por WhatsApp cuando un lead da señales de cierre
   ("sí quiero", "cuándo empezamos", "cómo pago", etc.).

El país se detecta por el código telefónico del número: 🇲🇽 52 · 🇨🇱 56 · 🇪🇨 593 ·
🇸🇻 503 · 🇧🇴 591 · 🇵🇪 51 · 🇨🇴 57.

## 🏗️ Arquitectura

```
WhatsApp ──Baileys──▶ flow.js (motor) ──▶ SQLite (estado/seguimientos)
                          │                    │
                          ├──▶ intents.js (moneda/opciones/cierre)
                          ├──▶ messages.js (plantillas + conversión)
                          ├──▶ notion.js  (CRM)
                          └──▶ alerta al dueño
node-cron (cada hora) ──▶ followup.js ──▶ seguimientos 24/48/72h
```

| Archivo | Rol |
|---|---|
| `src/index.js` | Arranque: conecta WhatsApp + programa seguimientos |
| `src/whatsapp.js` | Transporte Baileys (QR, reconexión, envío con escritura simulada) |
| `src/flow.js` | Motor de conversación |
| `src/intents.js` | Detección de opción / moneda / cierre |
| `src/messages.js` | Plantillas y conversión de moneda |
| `src/config.js` | Planes, precios, tasas de cambio, países, pagos |
| `src/db.js` | SQLite |
| `src/notion.js` | Sincronización con Notion (opcional) |
| `src/followup.js` | Cron de seguimiento |

## 🚀 Instalación en el VPS (Ubuntu/Debian)

```bash
# 1. Node.js 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs build-essential   # build-essential para better-sqlite3

# 2. Dependencias del bot
cd whatsapp-bot
npm install

# 3. Configuración
cp .env.example .env
nano .env        # pon tu OWNER_JID y, opcional, las claves de Notion

# 4. Primer arranque (escanea el QR con WhatsApp Business)
npm start
#   WhatsApp Business → Dispositivos vinculados → Vincular dispositivo → escanea el QR
#   La sesión queda guardada en auth_info/ (no se vuelve a pedir QR)

# 5. Producción con PM2 (auto-reinicio y arranque con el sistema)
sudo npm install -g pm2
pm2 start ecosystem.config.cjs
pm2 save
pm2 startup        # ejecuta el comando que imprime
```

Ver logs: `pm2 logs iptv-bot` · Reiniciar: `pm2 restart iptv-bot`

## ⚙️ Variables de entorno (`.env`)

| Variable | Obligatoria | Descripción |
|---|---|---|
| `OWNER_JID` | Sí (para alertas) | Tu número en formato `569XXXXXXXX@s.whatsapp.net` |
| `NOTION_TOKEN` | No | Token de integración interna de Notion |
| `NOTION_DATABASE_ID` | No | ID de la base de datos de leads |
| `TZ` | No | Zona horaria del cron (def. `America/Santiago`) |
| `MIN_TYPING_MS` / `MAX_TYPING_MS` | No | Rango de "escritura humana" antes de enviar |

## 🗂️ Base de datos de Notion

Crea una base de datos con **exactamente** estas propiedades (nombre y tipo):

| Propiedad | Tipo |
|---|---|
| `Nombre` | Title |
| `Número` | Text |
| `País` | Select |
| `Primer contacto` | Date |
| `Estado` | Select (opciones: `Nuevo`, `Demo`, `Interesado`, `Cerrado`, `Frío`) |
| `Plan` | Text |
| `Monto USD` | Number |
| `Método de pago` | Text |
| `Notas` | Text |

Luego comparte la base con tu integración (botón **···** → *Connections*) y copia el
ID de la base (parte de la URL) en `NOTION_DATABASE_ID`. Si dejas las claves de Notion
vacías, el bot funciona igual pero sin registrar en Notion.

## 💰 Actualizar precios o tasas de cambio

Todo está en `src/config.js` (`PLANS` y `COUNTRIES`). Las tasas son de referencia
y se editan a mano; si más adelante quieres tasas en vivo, se puede conectar una API
de tipo de cambio.

## ⚠️ Nota sobre Baileys (anti-ban)

Baileys usa WhatsApp Web de forma no oficial. Para reducir el riesgo de bloqueo:
- El bot simula escritura antes de responder y no hace spam.
- Respeta el corte a 72h (no insiste con leads fríos).
- Usa un número de WhatsApp Business dedicado y mantenlo "calentado".

Si el volumen crece, considera migrar a la **WhatsApp Cloud API oficial** de Meta.
