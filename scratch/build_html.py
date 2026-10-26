import json
import base64
import glob
import os

# 1. Read original desk frames from backup
with open('Folio Insurance_ single hero preview.bak.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_fr = text.find('const FR=[') + len('const FR=')
end_fr = text.find('];const COUNT=', start_fr) + 1
original_frames = json.loads(text[start_fr:end_fr])
desk_frames = original_frames[:80]
print(f'Desk frames: {len(desk_frames)}')

# 2. Read new 80 video frames from scratch/test_q88
video_frames = []
files = sorted(glob.glob('scratch/test_q88/frame_*.webp'))
for f in files:
    with open(f, 'rb') as fp:
        video_frames.append(base64.b64encode(fp.read()).decode('ascii'))
print(f'Video frames: {len(video_frames)}')

all_frames = desk_frames + video_frames
fr_json = json.dumps(all_frames)
print(f'Total frames: {len(all_frames)}, JSON length: {len(fr_json)}')

head_part = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Folio Insurance: every policy, every stage of life</title>
<meta name="description" content="Health, home, auto and life insurance in one place.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap" rel="stylesheet">
<style>:root{--ink:#16202b;--paper:#f6f3ec;--oak:#b98a52;--mist:#dfe6ea;--line:rgba(22,32,43,.16);--white:#fff}
*{box-sizing:border-box}html{scroll-padding-top:70px}
body{margin:0;background:var(--paper);color:var(--ink);font:400 18px/1.55 "Newsreader",Georgia,serif}
h1,h2,h3{font-family:"Bricolage Grotesque",system-ui,sans-serif}
nav{position:fixed;top:0;left:0;right:0;z-index:20;display:flex;justify-content:space-between;align-items:center;padding:calc(18px + env(safe-area-inset-top,0px)) 5vw 18px;color:var(--white);font:600 17px "Bricolage Grotesque",sans-serif}
nav a{color:inherit;text-decoration:none}nav .links{display:flex;gap:28px;font-weight:400;font-size:15px}
nav .cta{background:var(--white);color:var(--ink);padding:9px 18px;border-radius:999px;font-weight:600}
a:focus-visible{outline:3px solid var(--oak);outline-offset:3px}
#hero{height:1100vh;position:relative}
.stage{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;background:#222}
canvas{position:absolute;inset:0;width:100%;height:100%;display:block}
.scrim{position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,22,31,.78) 0%,rgba(14,22,31,.42) 38%,rgba(14,22,31,0) 70%);transition:background .5s ease,opacity .5s ease;pointer-events:none}
.scrim.film-mode{background:linear-gradient(90deg,rgba(14,22,31,.65) 0%,rgba(14,22,31,.25) 36%,rgba(14,22,31,0) 65%),linear-gradient(0deg,rgba(14,22,31,.55) 0%,rgba(14,22,31,0) 35%)}
.beat{position:absolute;left:5vw;bottom:14vh;max-width:560px;color:var(--white);opacity:0;transform:translateY(24px);transition:opacity .45s,transform .45s;pointer-events:none}
.beat.on{opacity:1;transform:none;pointer-events:auto}
.beat h1,.beat h2{font-size:clamp(38px,6.2vw,84px);line-height:.98;letter-spacing:-.03em;margin:0 0 18px;font-weight:700}
.beat p{margin:0;font-size:clamp(18px,1.7vw,23px);max-width:34em;color:rgba(255,255,255,.88)}
.btn{display:inline-block;margin-top:26px;background:var(--oak);color:var(--ink);padding:14px 26px;border-radius:999px;text-decoration:none;font:600 16px "Bricolage Grotesque",sans-serif}
.tabs{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
.tabs span{font:600 14px "Bricolage Grotesque",sans-serif;padding:8px 14px;border:1px solid rgba(255,255,255,.55);border-radius:6px;background:rgba(255,255,255,.12)}
.bar{position:absolute;left:5vw;right:5vw;bottom:5vh;height:2px;background:rgba(255,255,255,.28)}
.bar i{display:block;height:100%;width:0;background:var(--oak)}
.hint{position:absolute;right:5vw;bottom:calc(5vh + 14px);color:rgba(255,255,255,.8);font:400 14px "Bricolage Grotesque",sans-serif;transition:opacity .3s}
.load{position:absolute;inset:0;display:grid;place-items:center;background:var(--ink);color:var(--white);font:400 16px "Bricolage Grotesque",sans-serif;z-index:5;transition:opacity .5s}
section.page{padding:12vh 5vw;max-width:1180px;margin:0 auto}
section.page h2{font-size:clamp(32px,4.4vw,56px);line-height:1.02;letter-spacing:-.025em;margin:0 0 40px;max-width:14em}
.lead{max-width:34em}
.cov{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));border-top:2px solid var(--ink)}
.cov div{padding:26px 24px 30px 0;border-bottom:1px solid var(--line)}
.cov h3{margin:0 0 8px;font-size:24px}.cov p{margin:0;max-width:26em}
footer{background:var(--ink);color:var(--mist);padding:8vh 5vw;font:400 15px "Bricolage Grotesque",sans-serif}
@media (max-width:640px){nav .links{display:none}.beat{bottom:12vh;right:5vw}.scrim{background:linear-gradient(0deg,rgba(14,22,31,.85) 0%,rgba(14,22,31,.4) 60%,rgba(14,22,31,.1) 100%)}.scrim.film-mode{background:linear-gradient(0deg,rgba(14,22,31,.8) 0%,rgba(14,22,31,.3) 50%,rgba(14,22,31,0) 100%)}}
</style></head><body>
<nav><a href="#top">Folio</a><div class="links"><a href="#cover">Cover</a><a href="#claims">Claims</a></div><a class="cta" href="#cover">Get a quote</a></nav>

<header id="hero"><div class="stage">
<div class="load" id="load">Opening the folders…</div>
<canvas id="cv" role="img" aria-label="Scroll-driven film: insurance folders on a desk, then scenes of health and peace of mind"></canvas>
<div class="scrim" id="scrim"></div>

<div class="beat on" data-s="0" data-e=".1"><h1>Every policy, one desk.</h1><p>Health, home, auto and life cover, filed together and ready when you need them.</p></div>
<div class="beat" data-s=".11" data-e=".23"><h2>Stop searching for paperwork.</h2><p>Your documents sit in one place, so renewals and claims never start with a hunt through drawers.</p></div>
<div class="beat" data-s=".24" data-e=".37"><h2>Four folders. Nothing missing.</h2><p>Each policy keeps its own cover details, dates and contacts.</p><div class="tabs"><span>Health</span><span>Home</span><span>Auto</span><span>Life</span></div></div>
<div class="beat" data-s=".38" data-e=".5"><h2>Behind every folder, a life.</h2><p>Keep scrolling to see where your health cover shows up.</p></div>
<div class="beat" data-s=".51" data-e=".72"><h2>It starts with a check-up.</h2><p>Health cover turns doctor visits into routine care, keeping little milestones healthy and happy.</p></div>
<div class="beat" data-s=".73" data-e=".83"><h2>Care that grows with you.</h2><p>From routine diagnostics to specialist consultations, trusted guidance for every stage of life.</p></div>
<div class="beat" data-s=".84" data-e=".91"><h2>Prescriptions without friction.</h2><p>Cashless approvals and hassle-free pharmacy coverage when you need medication most.</p></div>
<div class="beat" data-s=".92" data-e="1.01"><h2>Peace of mind.</h2><p>Live each day with confidence, knowing you and your loved ones are protected wherever life takes you.</p><a class="btn" href="#cover">Get covered today</a></div>

<div class="hint" id="hint">Scroll to move in</div>
<div class="bar"><i id="prog"></i></div>
</div></header>

<section class="page" id="cover"><h2>Cover that fits on a single page.</h2>
<div class="cov"><div><h3>Health</h3><p>Hospital stays, day care and check-ups with cashless hospitals nearby.</p></div><div><h3>Home</h3><p>Structure and contents, covered against fire, flood and theft.</p></div><div><h3>Auto</h3><p>Own damage and third-party cover, renewed in a few taps.</p></div><div><h3>Life</h3><p>A fixed payout for the people who depend on you.</p></div></div></section>
<section class="page" id="claims"><h2>Claims that start with the right folder.</h2><p class="lead">Upload photos, pick the policy, and track each step until the settlement reaches your account.</p></section>
<footer>© 2026 Folio Insurance. Sample website.</footer>
"""

script_part = f"""<script>const FR={fr_json};const COUNT=160,SPLIT=.5;
const cv=document.getElementById('cv'),ctx=cv.getContext('2d'),hero=document.getElementById('hero'),
load=document.getElementById('load'),prog=document.getElementById('prog'),hint=document.getElementById('hint'),
beats=[...document.querySelectorAll('.beat')],scrimEl=document.getElementById('scrim'),
reduce=matchMedia('(prefers-reduced-motion:reduce)').matches,imgs=[];
let cur=0,target=0,ready=0,vis=true;
function size(){{
  const d=Math.min(devicePixelRatio||1,2);
  cv.width=innerWidth*d;
  cv.height=innerHeight*d;
  ctx.imageSmoothingEnabled=true;
  ctx.imageSmoothingQuality='high';
  draw(Math.round(cur));
}}
function draw(i){{
  const im=imgs[Math.max(0,Math.min(COUNT-1,i))];
  if(!im||!im.complete)return;
  const cw=cv.width,ch=cv.height,s=Math.max(cw/im.width,ch/im.height),w=im.width*s,h=im.height*s;
  ctx.imageSmoothingEnabled=true;
  ctx.imageSmoothingQuality='high';
  ctx.drawImage(im,(cw-w)/2,(ch-h)/2,w,h);
}}
function update(){{
  const r=hero.getBoundingClientRect();
  vis=r.bottom>0&&r.top<innerHeight;
  const p=Math.max(0,Math.min(1,-r.top/(hero.offsetHeight-innerHeight)));
  target=p*(COUNT-1);
  prog.style.width=p*100+'%';
  hint.style.opacity=p>.02?0:1;
  if(scrimEl)scrimEl.classList.toggle('film-mode',p>=SPLIT);
  beats.forEach(b=>b.classList.toggle('on',p>=+b.dataset.s&&p<+b.dataset.e));
}}
function loop(){{
  if(vis){{
    cur+=(target-cur)*(reduce?1:.14);
    if(Math.abs(target-cur)<.01)cur=target;
    draw(Math.round(cur));
  }}
  requestAnimationFrame(loop);
}}
for(let i=0;i<COUNT;i++){{
  const im=new Image();
  im.onload=im.onerror=()=>{{
    if(++ready===COUNT){{
      load.style.opacity=0;
      setTimeout(()=>load.remove(),500);
      size();update();loop();
    }}
  }};
  im.src='data:image/webp;base64,'+FR[i];
  imgs.push(im);
}}
addEventListener('scroll',update,{{passive:true}});
addEventListener('resize',()=>{{size();update()}});
</script></body></html>"""

full_html = head_part + script_part
with open('Folio Insurance_ single hero preview.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print('Updated Folio Insurance_ single hero preview.html successfully!')
print(f'New file size: {os.path.getsize("Folio Insurance_ single hero preview.html") / (1024*1024):.2f} MB')
