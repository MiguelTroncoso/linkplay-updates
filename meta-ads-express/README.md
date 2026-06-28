# Meta Ads Express para WhatsApp — Academia Venta Digital

Producto **upsell** (USD 27) de la familia *WhatsApp Ventas Pro*.

**Subtítulo:** La guía rápida para crear anuncios simples en Facebook e Instagram y llevar personas interesadas directo a tu WhatsApp.

## 📦 Entregables

### 🛒 Para el comprador (subir a Hotmart)

| Archivo | Descripción | Páginas |
|---|---|---|
| `LEEME-PRIMERO.txt` | Guía de bienvenida: qué incluye y orden de uso | — |
| `ebook-Meta-Ads-Express.pdf` | Ebook completo (10 capítulos + bonus + plan + recursos + aviso legal) | 35 |
| `recursos/banco-textos-anuncios.txt` | Plantillas de texto para anuncios | — |
| `recursos/checklist-lanzamiento.pdf` | Checklist de lanzamiento imprimible (1 página) | 1 |
| `recursos/planilla-seguimiento-resultados.csv` | Planilla de resultados (fecha, campaña, gasto, conversaciones, costo, ventas, ingresos, ganancia) | — |
| `recursos/10-ideas-creativos-canva.txt` | 10 conceptos de imagen para anuncios en Canva | — |
| `recursos/5-guiones-reels-anuncios.txt` | 5 guiones para grabar videos cortos / reels | — |

### 🔒 Uso interno (NO entregar al comprador)

| Archivo | Descripción |
|---|---|
| `materiales-de-venta.pdf` | Descripciones Hotmart, beneficios, bullets, **texto de upsell para el checkout**, ideas de portada, paleta, guía de estilo y títulos A/B |

Fuentes editables (HTML): `ebook.html`, `materiales-de-venta.html`, `recursos/checklist-lanzamiento.html`.

## 📘 Estructura del ebook (34 págs)

Presentación · Introducción · Cap. 1 Cómo funciona la publicidad a WhatsApp · Cap. 2 Lo que necesitas · Cap. 3 Define tu oferta y público · Cap. 4 Crea tu primer anuncio paso a paso · Cap. 5 Qué escribir y qué imagen · Cap. 6 Cuánto invertir · Cap. 7 Segmentación simple · Cap. 8 Prepara tu WhatsApp · Cap. 9 Cómo medir resultados · Cap. 10 Optimizar y crecer · Bonus 8 errores · Plan de 5 días · Checklist de lanzamiento · Banco de textos · Recursos descargables · Cierre (sistema completo) · Avisos legales.

Incluye: mockups de anuncios, pasos numerados, ejemplos de textos, tablas, ejercicios y plan de acción.

## 🔧 Regenerar

```bash
python3 fix_toc.py   # recalcula el índice con páginas reales
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=ebook-Meta-Ads-Express.pdf --print-to-pdf-no-header ebook.html
```

## 🎨 Identidad visual

Misma familia de marca + acento **azul Meta `#0866FF`** para identificar el producto de publicidad. Verde WhatsApp `#25D366`, azul profundo `#0B3D6B`, amarillo `#FFC53D`.

> Nota honesta: material educativo. La publicidad implica inversión que el usuario controla; no garantiza ventas ni resultados. Producto independiente, no afiliado a Meta/WhatsApp/Facebook/Instagram.
