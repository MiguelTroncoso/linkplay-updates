# 🤖 Bot WhatsApp B2B — IPTV LATAM (Resellers)

Bot de WhatsApp para captar, atender y dar seguimiento a revendedores de la
plataforma de Televisión Digital. Construido con **Baileys** (WhatsApp Web, gratis)
+ **SQLite** + **Notion**, pensado para correr en un VPS de 4GB con **PM2**.

---

## ✨ Funciones

1. **Respuesta automática** con menú de bienvenida (opción 1: desde cero / opción 2: ya vende).
2. **Demo del día**: el dueño la cambia cada mañana con un comando y el bot la reenvía
   igual todo el día, junto con las **apps recomendadas**.
3. **Seguimiento automático**: 24h (suave), 48h (urgencia/promo), 72h (marca lead frío).
4. **Conversión de moneda** local cuando el lead la pide (CLP, MXN, COP, PEN, BS; EC y SV en USD).
5. **Datos bancarios por país**: el bot los envía automáticamente cuando el lead va a pagar.
6. **Flujo de pago → entrega**: cuando el lead dice "ya pagué", el bot le pide el
   *usuario y contraseña* que desea y **te alerta** para que crees el panel manualmente.
7. **Hablar con una persona**: si el lead lo pide (o el bot no entiende tras varios intentos),
   se hace **handoff humano**: te avisa y **pausa el bot** para ese lead para no interferir.
8. **Registro automático en Notion** (nombre, país, fecha, estado, plan, monto, pago, notas).
9. **Alertas al dueño** por WhatsApp ante cierres, pagos, credenciales y solicitudes de asesor.

El país se detecta por el código telefónico: 🇲🇽 52 · 🇨🇱 56 · 🇪🇨 593 · 🇸🇻 503 · 🇧🇴 591 · 🇵🇪 51 · 🇨🇴 57.

---

## 🧭 Cómo conversa el bot (flujo)

```
Lead escribe ──▶ ¿es el dueño? ──▶ ejecuta comando (/demo, /apps, /pause, ...)
                       │ no
                       ▼
        ¿bot en pausa (handoff)? ──▶ solo registra, no responde
                       │ no
                       ▼
  Prioridad: credenciales > "hablar con persona" > "ya pagué" > cierre >
             primer contacto (bienvenida) > opción 1/2 > demo > bancos >
             moneda local > fallback (2 intentos → ofrece asesor)
```

| Situación del lead | Qué hace el bot |
|---|---|
| Primer mensaje (número nuevo) | Envía bienvenida con menú 1/2 |
| Vuelve a saludar (ya habló antes) | Menú de re-enganche: *"¿Ya te decidiste? 1️⃣ Sí, ver precios · 2️⃣ Hablar con una persona"* |
| Envía una **imagen** (comprobante) | **Lee el monto con IA (OCR)**, lo guarda en Notion y pide usuario/clave. Sin OCR: pide escribir *"pago realizado"* |
| Responde "1" | Explicación + precios + **demo del día** + apps |
| Responde "2" | Precios + pregunta cuántos clientes maneja |
| "quiero la demo" | Envía la demo del día + apps |
| "¿cuánto en pesos?" | Convierte precios a su moneda local |
| "a dónde transfiero" | Envía datos bancarios de su país + USDT/PayPal/WU |
| "sí quiero / cómo pago" | Datos de pago + **alerta al dueño** |
| "ya pagué" | Pide usuario/clave deseados + **alerta al dueño** |
| Envía usuario/clave | Confirma + **alerta al dueño con las credenciales** para crear el panel |
| "hablar con una persona" | Avisa que un asesor sigue + **pausa el bot** + te alerta |

---

## 🛠️ Comandos del dueño (envíalos por WhatsApp al número del bot)

> Solo funcionan desde el número configurado en `OWNER_JID`.

| Comando | Acción |
|---|---|
| `/demo` | Muestra la demo actual |
| `/demo <texto>` | **Actualiza la demo del día** (links, credenciales de prueba…) |
| `/apps` | Muestra las apps recomendadas |
| `/apps <texto>` | Actualiza las apps recomendadas |
| `/pause <número>` | Pausa el bot para ese lead (lo atiendes tú) |
| `/resume <número>` | Reactiva el bot para ese lead |
| `/ignore <número>` | El bot **nunca** responde a ese número |
| `/unignore <número>` | Permite que el bot vuelva a responder a ese número |
| `/stats` | Resumen de leads e ignorados |
| `/help` | Lista de comandos |

### 🚫 El bot NO responde a tus contactos guardados

Para que el bot atienda **solo a leads nuevos** de la campaña (y no a tus conocidos),
ignora automáticamente a cualquier número que ya tengas **guardado en la agenda** del
WhatsApp donde corre el bot. Tu lista de contactos se sincroniza sola al conectar.

Para los que te escribieron **antes** de activar el bot (y aún no tienes guardados),
agrégalos a `IGNORE_NUMBERS` en `.env` o usa `/ignore <número>` sobre la marcha.

**Ejemplo de tu rutina de la mañana** (un solo mensaje, admite varias líneas):

```
/demo Usuario de prueba del día:
🔗 http://tu-servidor.com:8080
👤 usuario: demo1206
🔑 clave: prueba2026
⏳ Válido solo por hoy
```

---

## 🏗️ Arquitectura

| Archivo | Rol |
|---|---|
| `src/index.js` | Arranque: conecta WhatsApp + programa seguimientos |
| `src/whatsapp.js` | Transporte Baileys (QR, reconexión, escritura simulada anti-ban) |
| `src/flow.js` | Motor de conversación |
| `src/commands.js` | Comandos del dueño (`/demo`, `/apps`, `/pause`…) |
| `src/intents.js` | Detección de opción / moneda / cierre / pago / humano / demo / banco |
| `src/messages.js` | Plantillas y conversión de moneda |
| `src/config.js` | **Planes, precios, tasas, países, bancos, demo y apps por defecto** |
| `src/db.js` | SQLite (leads + ajustes) |
| `src/notion.js` | Sincronización con Notion (opcional) |
| `src/followup.js` | Cron de seguimiento (cada hora) |

---

## 🚀 Paso a paso: instalación en el VPS (Ubuntu/Debian, 4GB RAM)

```bash
# 1. Node.js 20 LTS + herramientas de compilación (better-sqlite3 las necesita)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs build-essential

# 2. Clonar el repo y entrar a la carpeta del bot
git clone https://github.com/MiguelTroncoso/linkplay-updates.git
cd linkplay-updates/whatsapp-bot

# 3. Instalar dependencias
npm install

# 4. Configurar variables de entorno
cp .env.example .env
nano .env
#    OWNER_JID = tu número en formato 569XXXXXXXX@s.whatsapp.net (obligatorio para alertas)
#    NOTION_TOKEN y NOTION_DATABASE_ID (opcionales)

# 5. Completar tus datos reales en src/config.js
nano src/config.js
#    → BANK_DETAILS  (cuentas bancarias por país)
#    → CRYPTO_PAYMENTS (USDT/PayPal/Western Union)
#    → PLANS y COUNTRIES (precios y tasas, si cambian)

# 6. Primer arranque: vincular WhatsApp escaneando el QR
npm start
#    En WhatsApp Business: Ajustes → Dispositivos vinculados → Vincular dispositivo
#    Escanea el QR que aparece en la terminal.
#    La sesión queda guardada en auth_info/ (no se vuelve a pedir QR).

# 7. Producción con PM2 (auto-reinicio + arranque con el sistema)
sudo npm install -g pm2
pm2 start ecosystem.config.cjs
pm2 save
pm2 startup        # ejecuta el comando que imprime para que arranque al reiniciar el VPS
```

**Operación diaria:**

```bash
pm2 logs iptv-bot       # ver actividad en vivo
pm2 restart iptv-bot    # reiniciar
pm2 stop iptv-bot       # detener
```

Cada mañana solo envías `/demo ...` al bot por WhatsApp. Nada más.

---

## ⚙️ Variables de entorno (`.env`)

| Variable | Obligatoria | Descripción |
|---|---|---|
| `OWNER_JID` | Sí (para alertas/comandos) | Tu número: `569XXXXXXXX@s.whatsapp.net` |
| `NOTION_TOKEN` | No | Token de integración interna de Notion |
| `NOTION_DATABASE_ID` | No | ID de la base de datos de leads |
| `IGNORE_NUMBERS` | No | Números que el bot nunca responde (coma-separados, sin `+`) |
| `ANTHROPIC_API_KEY` | No | Clave de Claude para leer el monto de los comprobantes con OCR |
| `TZ` | No | Zona horaria del cron (def. `America/Santiago`) |
| `MIN_TYPING_MS` / `MAX_TYPING_MS` | No | Rango de "escritura humana" antes de enviar |

> 💡 Para obtener tu `OWNER_JID`: es tu número completo con código de país, sin `+`,
> seguido de `@s.whatsapp.net`. Ej. Chile `+56 9 1234 5678` → `56912345678@s.whatsapp.net`.

---

## 🗂️ Notion: crear la base de datos (BD)

### Opción A — Prompt listo para pegar en Notion AI

> En una página de Notion, escribe `/AI` (o usa Notion AI) y pega esto:

```
Crea una base de datos (database) tipo tabla llamada "Leads IPTV LATAM" con estas
propiedades exactas, respetando nombres y tipos:

1. "Nombre"           → Title
2. "Número"           → Text
3. "País"             → Select con opciones: México, Chile, Ecuador, El Salvador, Bolivia, Perú, Colombia
4. "Primer contacto"  → Date
5. "Estado"           → Select con opciones: Nuevo, Demo, Interesado, Cerrado, Frío
6. "Plan"             → Text
7. "Monto USD"        → Number (formato dólar)
8. "Método de pago"   → Text
9. "Notas"            → Text

Crea también 3 vistas: una tabla "Todos", un tablero (Board) agrupado por "Estado",
y una vista de calendario por "Primer contacto".
```

### Opción B — Manual

Crea una base de datos con **exactamente** estas propiedades (los nombres deben coincidir):

| Propiedad | Tipo | Notas |
|---|---|---|
| `Nombre` | Title | |
| `Número` | Text | |
| `País` | Select | México, Chile, Ecuador, El Salvador, Bolivia, Perú, Colombia |
| `Primer contacto` | Date | |
| `Estado` | Select | `Nuevo`, `Demo`, `Interesado`, `Cerrado`, `Frío` |
| `Plan` | Text | |
| `Monto USD` | Number | |
| `Método de pago` | Text | |
| `Notas` | Text | |

### Conectar la integración

1. Ve a <https://www.notion.so/my-integrations> → **New integration** → copia el *Internal Integration Secret* → pégalo en `NOTION_TOKEN`.
2. Abre tu base de datos → botón **···** (arriba a la derecha) → **Connections** → añade tu integración.
3. Copia el **ID de la base** desde la URL y pégalo en `NOTION_DATABASE_ID`:
   `https://notion.so/tuworkspace/`**`ESTE_ES_EL_ID`**`?v=...` (los 32 caracteres antes de `?v=`).

> Si dejas `NOTION_TOKEN`/`NOTION_DATABASE_ID` vacíos, el bot funciona igual, solo no registra en Notion.

---

## 💰 Actualizar precios, tasas, bancos, demo

| Qué | Dónde |
|---|---|
| Precios de planes | `src/config.js` → `PLANS` |
| Tasas de cambio | `src/config.js` → `COUNTRIES` (campo `rate`) |
| Datos bancarios por país | `src/config.js` → `BANK_DETAILS` |
| USDT / PayPal / Western Union | `src/config.js` → `CRYPTO_PAYMENTS` |
| Demo del día | comando `/demo` por WhatsApp (no requiere reiniciar) |
| Apps recomendadas | comando `/apps` por WhatsApp |

Tras editar `config.js`: `pm2 restart iptv-bot`.

---

## 📸 OCR de comprobantes (lectura del monto con IA)

Cuando un lead envía la **foto de su comprobante**, el bot la lee con **Claude Haiku 4.5**
(visión) y extrae el **monto, la moneda y el método de pago**. Convierte el monto a USD
con tus tasas (`src/config.js`), lo **guarda en Notion** (campo *Monto USD*) y le pide al
cliente el usuario/clave para su panel — todo automático. Tú recibes la alerta con el monto.

Para activarlo, pon tu `ANTHROPIC_API_KEY` (de <https://console.anthropic.com>) en `.env`.
Es muy económico: Haiku cuesta ~$1 por millón de tokens, y cada comprobante usa muy pocos.
Si dejas la clave vacía, el bot sigue funcionando: solo le pide al cliente que escriba
*"pago realizado"* en vez de leer el monto.

## ⚠️ Nota sobre Baileys (anti-ban)

Baileys usa WhatsApp Web de forma no oficial. Para reducir el riesgo de bloqueo el bot
simula escritura antes de responder, no hace spam y respeta el corte a 72h. Recomendado:
usa un número de WhatsApp Business **dedicado** y "calentado". Si el volumen crece mucho,
considera migrar a la **WhatsApp Cloud API oficial** de Meta.
