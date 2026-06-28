# WhatsApp Ventas Pro — Academia Venta Digital

Producto digital completo: ebook + kit de materiales de venta para Hotmart.

**Subtítulo:** Sistema simple para ordenar clientes, responder mejor y vender más usando WhatsApp + IA.

## 📦 Entregables

### 🛒 Para el comprador (subir a Hotmart)

| Archivo | Descripción | Páginas |
|---|---|---|
| `LEEME-PRIMERO.txt` | Guía de bienvenida: qué incluye y orden sugerido de uso | — |
| `ebook-WhatsApp-Ventas-Pro.pdf` | Ebook completo (15 secciones + bonus + recursos + aviso legal) | 45 |
| `recursos/plantilla-CRM-WhatsApp-Ventas-Pro.csv` | Plantilla CRM editable para Google Sheets / Excel | — |
| `recursos/checklist-imprimible.pdf` | Checklist diario imprimible (1 página, con diseño de marca) | 1 |
| `recursos/checklist-imprimible.md` | Checklist en texto (fuente editable del PDF) | — |
| `recursos/frases-copiables.txt` | Muestra inicial de frases listas para copiar | — |
| `recursos/prompts-IA.txt` | Prompts de IA para mejorar y adaptar mensajes | — |

### 🔒 Uso interno (NO entregar al comprador)

| Archivo | Descripción |
|---|---|
| `materiales-de-venta.pdf` | Material interno para configurar Hotmart, anuncios y página de venta (descripciones, beneficios, bullets, portadas, paleta, guía de estilo, títulos A/B) |

Archivos fuente editables (HTML con estilos embebidos): `ebook.html` y `materiales-de-venta.html`.

## 📘 Estructura del ebook

1. Portada
2. Presentación de Academia Venta Digital
3. Introducción: por qué se pierden ventas en WhatsApp
4. Cap. 1 — El error de vender solo respondiendo mensajes
5. Cap. 2 — Cómo ordenar tus clientes por etapas
6. Cap. 3 — Cómo usar una plantilla CRM simple
7. Cap. 4 — Cómo responder rápido sin sonar robótico
8. Cap. 5 — Cómo usar IA para crear mejores respuestas
9. Cap. 6 — Cómo hacer seguimiento sin parecer insistente
10. Cap. 7 — Cómo responder objeciones comunes
11. Cap. 8 — Cómo cerrar ventas con mensajes claros
12. Cap. 9 — Rutina diaria de 20 minutos
13. Cap. 10 — Plan de acción de 7 días
14. Bonus: 10 errores frecuentes · Banco de frases · Plantilla CRM imprimible
15. Checklist final
16. Recursos descargables (con enlaces/QR a editar)
17. Invitación al siguiente paso: Meta Ads Express para WhatsApp
18. Avisos legales (marcas + resultados + IA)

Incluye: ejemplos reales de conversaciones, tablas de clasificación de clientes, checklist diario, ejercicios prácticos, frases para copiar y pegar, y recomendaciones de uso de IA.

> **Índice con páginas reales:** los números del índice se calculan automáticamente con `fix_toc.py` (renderiza cada sección, cuenta sus páginas y reescribe el índice). Ejecútalo después de editar contenido y antes de regenerar el PDF.

## 🎨 Identidad visual

- **Estilo:** moderno, limpio, digital, confiable.
- **Paleta:** Azul profundo `#0B3D6B`, Azul digital `#1573C6`, Verde WhatsApp `#25D366`, Verde oscuro `#0E7A4A`, Amarillo acento `#FFC53D`, Gris claro `#EAF0F5`.

## 🔧 Regenerar los PDF

```bash
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=ebook-WhatsApp-Ventas-Pro.pdf --print-to-pdf-no-header ebook.html
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=materiales-de-venta.pdf --print-to-pdf-no-header materiales-de-venta.html
```

> Nota honesta: material educativo. No promete riqueza ni garantiza resultados.
