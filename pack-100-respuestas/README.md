# Pack 100 Respuestas para WhatsApp — Academia Venta Digital

Producto complementario (**Order Bump**) de *WhatsApp Ventas Pro*.

**Subtítulo:** Mensajes listos para responder, hacer seguimiento y cerrar ventas sin quedarte en blanco.

## 📦 Entregables

| Archivo | Descripción |
|---|---|
| `pack-100-respuestas.pdf` | Producto final maquetado (51 páginas) — listo para entregar |
| `pack-100-respuestas-EDITABLE.md` | **Plantilla editable** — copia, pega y reemplaza los [corchetes] |
| `pack-100-respuestas.csv` | Los 100 mensajes en columnas — ideal para importar/ordenar o pegar como respuestas rápidas |
| `pack-100-respuestas.html` | Fuente del PDF (editable con estilos) |
| `build.py` | Generador: fuente única de datos → HTML + MD + CSV |

## 💬 Contenido: 100 mensajes en 9 categorías

| # | Categoría | Mensajes |
|---|---|---|
| 1 | Mensajes de bienvenida | 15 |
| 2 | Respuestas a consultas iniciales | 15 |
| 3 | Mensajes para explicar precios | 15 |
| 4 | Mensajes para hacer seguimiento | 15 |
| 5 | Clientes que dejaron de responder | 10 |
| 6 | Respuestas a objeciones comunes | 10 |
| 7 | Mensajes de cierre de venta | 10 |
| 8 | Mensajes para pedir datos de compra | 5 |
| 9 | Mensajes para reactivar clientes antiguos | 5 |

Cada mensaje incluye: **título del caso de uso**, **mensaje listo para copiar**, **variante más corta** y **recomendación de cuándo enviarlo**.

## 📋 Material adicional incluido

- Introducción breve e instrucciones de uso (7 pasos)
- Checklist de seguimiento diario
- 10 prompts de IA para adaptar los mensajes a cualquier negocio
- Descripción corta y larga para Hotmart (con disclaimer de marcas para pegar en la ficha)
- Texto de venta para Order Bump (checkout)
- 3 ideas de diseño en Canva + portada y contraportada sugeridas
- Página de **Avisos legales** (marcas WhatsApp/Meta + resultados + herramientas de IA), coherente con el ebook principal

## 🎨 Identidad visual

Mismo sistema de marca que *WhatsApp Ventas Pro*: Azul `#0B3D6B` / `#1573C6`, Verde WhatsApp `#25D366`, Amarillo acento `#FFC53D`. Estilo moderno, limpio, digital y confiable.

## 🔧 Regenerar los archivos

```bash
python3 build.py   # genera HTML, MD y CSV desde la fuente única
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=pack-100-respuestas.pdf --print-to-pdf-no-header pack-100-respuestas.html
```

> Nota honesta: material educativo. No promete ventas garantizadas ni usa frases engañosas. El enfoque es ordenar y mejorar la comunicación comercial.
