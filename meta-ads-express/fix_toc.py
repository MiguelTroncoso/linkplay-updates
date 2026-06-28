# -*- coding: utf-8 -*-
"""Calcula los números de página reales de cada sección y reescribe el índice."""
import re, os, subprocess, tempfile

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
SRC = "ebook.html"
html = open(SRC, encoding="utf-8").read()
head = html[:html.index("</head>") + len("</head>")]
body = html[html.index("<body>"):]
sections = re.findall(r"<section\b.*?</section>", body, re.DOTALL)
print("Secciones:", len(sections))

def page_count(s):
    full = (head + "<body><style>section,.cover{page-break-after:auto !important;"
            "min-height:auto !important;}</style>" + s + "</body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(full); path = f.name
    pdf = path + ".pdf"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "--print-to-pdf-no-header", path],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    n = len(re.findall(rb"/Type\s*/Page[^s]", open(pdf, "rb").read()))
    os.remove(path); os.remove(pdf)
    return max(n, 1)

starts, cur = [], 1
for s in sections:
    starts.append(cur); cur += page_count(s)
print("Total:", cur - 1)

idx_section = next(i for i, s in enumerate(sections) if 'class="toc-item"' in s)
def start(sub):
    for i, s in enumerate(sections):
        if i != idx_section and sub in s:
            return starts[i]
    raise ValueError(sub)

TOC = [
 ("Presentación", False, "Ya ordenaste. Ahora toca atraer"),
 ("Introducción: por qué los anuncios a WhatsApp funcionan", False, "Por qué los anuncios a WhatsApp funcionan"),
 ("Capítulo 1 · Cómo funciona la publicidad que lleva a WhatsApp", True, "Cómo funciona la publicidad que lleva a WhatsApp"),
 ("Capítulo 2 · Lo que necesitas antes de empezar", True, "Lo que necesitas antes de empezar"),
 ("Capítulo 3 · Define tu oferta y a quién le hablas", True, "Define tu oferta y a quién le hablas"),
 ("Capítulo 4 · Crea tu primer anuncio paso a paso", True, "Crea tu primer anuncio paso a paso"),
 ("Capítulo 5 · Qué escribir y qué imagen usar", True, "Qué escribir y qué imagen usar"),
 ("Capítulo 6 · Cuánto invertir para empezar", True, "Cuánto invertir para empezar"),
 ("Capítulo 7 · A quién mostrarle tu anuncio", True, "A quién mostrarle tu anuncio"),
 ("Capítulo 8 · Prepara tu WhatsApp para los anuncios", True, "Prepara tu WhatsApp para recibir los anuncios"),
 ("Capítulo 9 · Cómo saber si tu anuncio funciona", True, "Cómo saber si tu anuncio funciona"),
 ("Capítulo 10 · Optimizar y crecer con calma", True, "Optimizar y crecer con calma"),
 ("Bonus: 8 errores comunes al hacer anuncios", False, "8 errores comunes al hacer anuncios"),
 ("Plan de acción: lanza tu primer anuncio en 5 días", False, "Lanza tu primer anuncio en 5 días"),
 ("Checklist de lanzamiento", False, "Checklist de lanzamiento</h2>"),
 ("Banco de textos para tus anuncios", False, "Banco de textos para tus anuncios"),
 ("Recursos descargables", False, "Recursos descargables</h2>"),
 ("Tu sistema completo", False, "Ya tienes la máquina completa"),
 ("Avisos legales", False, "Avisos legales</h2>"),
]
rows = []
for label, cap, sub in TOC:
    p = start(sub)
    cls = ' class="toc-cap"' if cap else ""
    rows.append(f'  <div class="toc-item"><span{cls}>{label}</span><span class="n">{p:02d}</span></div>')
new = "\n".join(rows)

old = re.search(r'  <!-- TOC_AUTO -->.*?</section>', html, re.DOTALL).group(0)
html = html.replace(old, "  <!-- TOC_AUTO -->\n" + new + "\n</section>")
open(SRC, "w", encoding="utf-8").write(html)
print("Índice actualizado:")
for label, _, sub in TOC:
    print(f"  {start(sub):02d}  {label}")
