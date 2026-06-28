# -*- coding: utf-8 -*-
"""Calcula los números de página REALES de cada sección del ebook
renderizando cada una por separado, y reescribe el índice con precisión."""
import re, os, subprocess, tempfile

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
SRC = "ebook.html"

html = open(SRC, encoding="utf-8").read()
head = html[:html.index("</head>") + len("</head>")]
body = html[html.index("<body>"):]

# Extraer secciones (no anidadas)
sections = re.findall(r"<section\b.*?</section>", body, re.DOTALL)
print(f"Secciones encontradas: {len(sections)}")

def page_count(section_html):
    full = (head + "<body><style>section,.cover{page-break-after:auto !important;"
            "min-height:auto !important;}</style>" + section_html + "</body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(full); path = f.name
    pdf = path + ".pdf"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    "--print-to-pdf-no-header", path],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    data = open(pdf, "rb").read()
    n = len(re.findall(rb"/Type\s*/Page[^s]", data))
    os.remove(path); os.remove(pdf)
    return max(n, 1)

# Página de inicio de cada sección (1-indexed)
starts, cur = [], 1
counts = []
for s in sections:
    starts.append(cur)
    c = page_count(s)
    counts.append(c)
    cur += c
total = cur - 1
print("Páginas por sección:", counts)
print("Total:", total)

# Identificar la sección índice (la que tiene los toc-item) para excluirla
idx_section = next(i for i, s in enumerate(sections) if 'class="toc-item"' in s)

def find_start(substr):
    for i, s in enumerate(sections):
        if i == idx_section:
            continue
        if substr in s:
            return starts[i]
    raise ValueError(f"No encontrado: {substr}")

# (etiqueta visible, es_capitulo, substring para localizar la sección)
TOC = [
 ("Presentación de Academia Venta Digital", False, "Quiénes somos"),
 ("Introducción: por qué se pierden ventas en WhatsApp", False, "Por qué muchos emprendedores pierden"),
 ("Capítulo 1 · El error de vender solo respondiendo mensajes", True, "El error de vender solo respondiendo"),
 ("Capítulo 2 · Cómo ordenar tus clientes por etapas", True, "Cómo ordenar tus clientes por etapas"),
 ("Capítulo 3 · Cómo usar una plantilla CRM simple", True, "Cómo usar una plantilla CRM simple"),
 ("Capítulo 4 · Cómo responder rápido sin sonar robótico", True, "Cómo responder rápido sin sonar"),
 ("Capítulo 5 · Cómo usar IA para crear mejores respuestas", True, "Cómo usar IA para crear mejores"),
 ("Capítulo 6 · Cómo hacer seguimiento sin parecer insistente", True, "Cómo hacer seguimiento sin parecer"),
 ("Capítulo 7 · Cómo responder objeciones comunes", True, "Cómo responder objeciones comunes"),
 ("Capítulo 8 · Cómo cerrar ventas con mensajes claros", True, "Cómo cerrar ventas con mensajes"),
 ("Capítulo 9 · Rutina diaria de 20 minutos", True, "Rutina diaria de 20 minutos"),
 ("Capítulo 10 · Plan de acción de 7 días", True, "Plan de acción de 7 días"),
 ("Bonus: errores, banco de frases y plantilla CRM", False, "10 errores que matan tus ventas"),
 ("Checklist final", False, "Checklist final"),
 ("Recursos descargables", False, "Recursos descargables"),
 ("Siguiente paso: Meta Ads Express para WhatsApp", False, "Meta Ads Express para WhatsApp"),
]

rows = []
for label, is_cap, sub in TOC:
    p = find_start(sub)
    cls = ' class="toc-cap"' if is_cap else ""
    rows.append(f'  <div class="toc-item"><span{cls}>{label}</span>'
                f'<span class="n">{p:02d}</span></div>')
new_toc = "\n".join(rows)

# Reemplazar el bloque de toc-items existente
old_block = re.search(r'(  <div class="toc-item">.*?</div>)\s*\n</section>',
                      html, re.DOTALL).group(1)
html = html.replace(old_block, new_toc)
open(SRC, "w", encoding="utf-8").write(html)
print("\nÍndice actualizado:")
for label, _, sub in TOC:
    print(f"  {find_start(sub):02d}  {label}")
