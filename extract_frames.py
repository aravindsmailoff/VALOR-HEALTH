import re
import base64
import os

with open(r'd:\VALOR\Folio Insurance_ single hero preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'const FR\s*=\s*\[(.*?)\];', content, re.DOTALL)
if not m:
    print("Could not find FR array")
    exit(1)

raw_items = m.group(1)
items = re.findall(r'"([^"]+)"', raw_items)
print(f"Found {len(items)} frames in Folio Insurance_ single hero preview.html")

out_dir = r'd:\VALOR\folio-app\public\folio_frames'
os.makedirs(out_dir, exist_ok=True)

for i, b64_str in enumerate(items):
    data = base64.b64decode(b64_str)
    filepath = os.path.join(out_dir, f"frame_{i:03d}.webp")
    with open(filepath, 'wb') as img_f:
        img_f.write(data)

print(f"Successfully saved {len(items)} webp frames to {out_dir}")
