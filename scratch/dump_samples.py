import base64
import re
import cv2
import numpy as np
import os

with open(r'd:\VALOR\Folio Insurance_ single hero preview.html', 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'const FR\s*=\s*\[(.*?)\];', c, re.DOTALL)
items = re.findall(r'"([^"]+)"', m.group(1))

os.makedirs(r'd:\VALOR\scratch\preview_inspect', exist_ok=True)

# Save every 10th frame as jpg to inspect
for i in range(0, len(items), 8):
    data = base64.b64decode(items[i])
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite(rf'd:\VALOR\scratch\preview_inspect\frame_{i:03d}.jpg', img)

print(f"Saved {len(range(0, len(items), 8))} sample frames to d:\\VALOR\\scratch\\preview_inspect")
