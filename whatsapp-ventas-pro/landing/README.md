# Landing page — WhatsApp Ventas Pro

Página de ventas autónoma (1 solo archivo) para Hotmart u hosting propio.

- **Archivo:** `index.html` (HTML + CSS + JS embebidos, sin dependencias salvo Google Fonts)
- **Responsive:** mobile-first, con barra CTA fija en celular.
- **Carga rápida:** sin frameworks ni imágenes pesadas.

## ✏️ Qué reemplazar antes de publicar

| Placeholder | Dónde | Reemplazar por |
|---|---|---|
| `[PEGAR_LINK_DE_COMPRA_HOTMART]` | 5 botones (header, hero, oferta, CTA final, barra fija) | Tu link de checkout de Hotmart |
| `[ MOCKUP_EBOOK ]` | Hero (caja azul) | Imagen/render real del ebook (reemplaza el `<div class="mockup">`) |
| `[IMAGEN_CRM]` / `[ICONOS_RECURSOS]` | — | Opcional: ya se usan íconos SVG propios; cámbialos si quieres fotos reales |

> Tip: busca y reemplaza `[PEGAR_LINK_DE_COMPRA_HOTMART]` (5 apariciones) de una sola vez.

## 🎨 Características incluidas
- 15 secciones: hero, problema (5 fugas), solución, qué incluye, beneficios, para quién sí/no, cómo funciona, oferta, seguridad/confianza, order bump + upsell, FAQ (acordeón), CTA final, footer.
- Paleta de marca (azul profundo, azul digital, verde WhatsApp, amarillo).
- Tipografías Poppins (títulos) + Inter (texto) vía Google Fonts.
- CTAs repetidos (hero, oferta, cierre) + barra fija en móvil.
- FAQ acordeón con `<details>` (funciona incluso sin JS).
- Animaciones de aparición solo si hay JS (sin JS, todo se ve normal).
- Avisos legales y de independencia de marcas; sin testimonios falsos; sin logos oficiales de terceros.

## 🚀 Publicar
1. Reemplaza los placeholders.
2. (Opcional) Inserta tu imagen real del ebook en el hero.
3. Sube `index.html` a tu hosting, o pega el contenido en un editor compatible con HTML.
4. Verifica en celular y escritorio.
