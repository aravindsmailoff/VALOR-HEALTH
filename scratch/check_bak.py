import re
import json

with open("Folio Insurance_ single hero preview.bak.html", "r", encoding="utf-8") as f:
    c_bak = f.read()

m = re.search(r'const FR\s*=\s*\[(.*?)\];', c_bak, re.DOTALL)
if m:
    raw = m.group(1).strip()
    # It might be comma-separated strings
    frames = [s.strip().strip('"').strip("'") for s in raw.split(",")]
    print("Found frames in bak:", len(frames))
    print("First frame length:", len(frames[0]))
    print("Frame 80 length:", len(frames[80]))
    print("Last frame length:", len(frames[-1]))
else:
    print("No FR array found in bak")
