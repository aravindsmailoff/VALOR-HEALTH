import re

with open(r'd:\VALOR\Folio Insurance_ single hero preview.html', 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'const FR\s*=\s*\[(.*?)\];', c, re.DOTALL)
if m:
    items = re.findall(r'"([^"]+)"', m.group(1))
    print(f"Frames in Folio Insurance_ single hero preview.html: {len(items)}")
else:
    print("No FR found")
