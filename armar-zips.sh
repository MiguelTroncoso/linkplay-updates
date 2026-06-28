#!/usr/bin/env bash
# ============================================================
# armar-zips.sh — Empaqueta los 3 productos de Academia Venta
# Digital en ZIPs listos para subir a Hotmart.
# Cada ZIP contiene SOLO los archivos del comprador (no el
# material interno de venta ni los archivos fuente).
#
# Uso:  bash armar-zips.sh
# Salida:  ./entregas/<Producto>.zip
# ============================================================
set -euo pipefail
cd "$(dirname "$0")"

OUT="entregas"
rm -rf "$OUT"
mkdir -p "$OUT"

# Empaqueta una carpeta-producto: nombre + lista de archivos
armar() {
  local nombre="$1"; shift
  local stage="$OUT/$nombre"
  echo "→ $nombre"
  rm -rf "$stage"; mkdir -p "$stage"
  for f in "$@"; do
    if [[ ! -f "$f" ]]; then
      echo "   ⚠️  FALTA: $f" >&2; exit 1
    fi
    cp "$f" "$stage/"
    echo "   + $(basename "$f")"
  done
  ( cd "$OUT" && zip -r -X -q "$nombre.zip" "$nombre" )
  rm -rf "$stage"
}

# ---- 1) Producto principal: WhatsApp Ventas Pro (USD 9,99) ----
armar "WhatsApp-Ventas-Pro" \
  "whatsapp-ventas-pro/LEEME-PRIMERO.txt" \
  "whatsapp-ventas-pro/ebook-WhatsApp-Ventas-Pro.pdf" \
  "whatsapp-ventas-pro/recursos/plantilla-CRM-WhatsApp-Ventas-Pro.csv" \
  "whatsapp-ventas-pro/recursos/checklist-imprimible.pdf" \
  "whatsapp-ventas-pro/recursos/frases-copiables.txt" \
  "whatsapp-ventas-pro/recursos/prompts-IA.txt"

# ---- 2) Order bump: Pack 100 Respuestas (USD 7) ----
armar "Pack-100-Respuestas-para-WhatsApp" \
  "pack-100-respuestas/LEEME-PRIMERO.txt" \
  "pack-100-respuestas/pack-100-respuestas.pdf" \
  "pack-100-respuestas/pack-100-respuestas-EDITABLE.md" \
  "pack-100-respuestas/pack-100-respuestas.csv"

# ---- 3) Upsell: Meta Ads Express (USD 27) ----
armar "Meta-Ads-Express-para-WhatsApp" \
  "meta-ads-express/LEEME-PRIMERO.txt" \
  "meta-ads-express/ebook-Meta-Ads-Express.pdf" \
  "meta-ads-express/recursos/checklist-lanzamiento.pdf" \
  "meta-ads-express/recursos/banco-textos-anuncios.txt" \
  "meta-ads-express/recursos/planilla-seguimiento-resultados.csv" \
  "meta-ads-express/recursos/10-ideas-creativos-canva.txt" \
  "meta-ads-express/recursos/5-guiones-reels-anuncios.txt"

echo ""
echo "✅ Listo. ZIPs generados en ./$OUT/"
ls -lh "$OUT"/*.zip
