with open(r'd:\VALOR\Folio Insurance_ single hero preview.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace titles, nav, footer
html = html.replace('<title>Folio Insurance: every policy, every stage of life</title>', '<title>VALOR Health: Continuous Coverage & Predictive Digital Twin</title>')
html = html.replace('<nav><a href="#top">Folio</a>', '<nav><a href="#top">VALOR</a>')
html = html.replace('<footer>© 2026 Folio Insurance. Sample website.</footer>', '<footer>© 2026 VALOR Health Insurance. All rights reserved.</footer>')

with open(r'd:\VALOR\Folio Insurance_ single hero preview.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated Folio Insurance_ single hero preview.html with VALOR branding!")
