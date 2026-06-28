# WhatsApp Ventas Pro — Academia Venta Digital

Producto digital completo: ebook + kit de materiales de venta para Hotmart.

**Subtítulo:** Sistema simple para ordenar clientes, responder mejor y vender más usando WhatsApp + IA.

## 📦 Entregables (listos en PDF)

| Archivo | Descripción | Páginas |
|---|---|---|
| `ebook-WhatsApp-Ventas-Pro.pdf` | Ebook completo (15 secciones + bonus) | 41 |
| `materiales-de-venta.pdf` | Contraportada, descripciones Hotmart, beneficios, bullets, portadas, paleta, guía de estilo y títulos A/B | 14 |

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
16. Invitación al siguiente paso: Meta Ads Express para WhatsApp

Incluye: ejemplos reales de conversaciones, tablas de clasificación de clientes, checklist diario, ejercicios prácticos, frases para copiar y pegar, y recomendaciones de uso de IA.

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
