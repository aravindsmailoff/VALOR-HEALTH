import re

with open("Folio Insurance_ single hero preview.bak.html", "r", encoding="utf-8") as f:
    c_bak = f.read()

with open("Folio Insurance_ single hero preview.html", "r", encoding="utf-8") as f:
    c_cur = f.read()

m_bak = re.search(r'const FR\s*=\s*\[(.*?)\];', c_bak, re.DOTALL)
m_cur = re.search(r'const FR\s*=\s*\[(.*?)\];', c_cur, re.DOTALL)

f_bak = [s.strip().strip('"').strip("'") for s in m_bak.group(1).split(",")]
f_cur = [s.strip().strip('"').strip("'") for s in m_cur.group(1).split(",")]

diffs = [i for i in range(160) if f_bak[i] != f_cur[i]]
print(f"Total diffs: {len(diffs)}")
if diffs:
    print(f"Diffs start at frame {diffs[0]} and end at frame {diffs[-1]}")
