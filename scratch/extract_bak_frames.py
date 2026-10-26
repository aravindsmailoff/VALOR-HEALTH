import re
import base64
from pathlib import Path

out_dir = Path("folio-app/public/frames")
out_dir.mkdir(parents=True, exist_ok=True)

with open("Folio Insurance_ single hero preview.bak.html", "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r'const FR\s*=\s*\[(.*?)\];', content, re.DOTALL)
frames = [s.strip().strip('"').strip("'") for s in m.group(1).split(",")]

print(f"Extracting {len(frames)} original still-photo frames into {out_dir}...")
for i, f_b64 in enumerate(frames):
    img_data = base64.b64decode(f_b64)
    file_path = out_dir / f"frame_{i:03d}.webp"
    with open(file_path, "wb") as img_file:
        img_file.write(img_data)

print("Original still-photo frame restoration complete!")
