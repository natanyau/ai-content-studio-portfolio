# Gera o carrossel do TM-002 (10 slides 1080x1350 + PDF para o LinkedIn).
# As imagens são frames do próprio reel (assets/media/case2.mp4), extraídos na hora com ffmpeg
# para .carousel/tm002/frames/. Nada é gravado em assets/ (regra 4).
# Os planos das prateleiras com caixas de peças ficam de fora: mostram marca de fabricante.
# Uso: python3 scripts/carousel-tm002.py   -> escreve em .carousel/tm002/out/ (não versionado)
# Em sessão remota do Claude Code: CHROMIUM=/opt/pw-browsers/chromium python3 scripts/carousel-tm002.py
# Precisa de: ffmpeg e pip install playwright pillow.
import os
import subprocess
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILM = os.path.join(ROOT, 'assets', 'media', 'case2.mp4')
WORK = os.path.join(ROOT, '.carousel', 'tm002')
FRAMES = os.path.join(WORK, 'frames')
OUT = os.path.join(WORK, 'out')
os.makedirs(FRAMES, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

# Segundo do reel -> plano usado no slide.
TIMES = ['1', '4.5', '7.5', '15', '22.5', '24', '25.5', '28.5']
for t in TIMES:
    dst = os.path.join(FRAMES, f'f{t}.jpg')
    if not os.path.exists(dst):
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', t, '-i', FILM,
                        '-frames:v', '1', '-q:v', '2', dst], check=True)

def img(t): return f'file://{FRAMES}/f{t}.jpg'

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden;background:#0a0a0b;color:#fff;font-family:"Liberation Sans",Arial,sans-serif}
.s{position:relative;width:1080px;height:1350px;padding:96px 88px;display:flex;flex-direction:column}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.veil{position:absolute;inset:0}
.c{position:relative;z-index:2;display:flex;flex-direction:column;height:100%}
.eb{font-size:22px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:#b7b7bc}
.eb b{color:#e1262f;font-weight:700}
h1,h2{font-family:"Liberation Serif",Georgia,serif;font-weight:700;line-height:1.02;letter-spacing:-.01em}
h1{font-size:118px}
h2{font-size:84px}
h2 span,h1 span{color:#e1262f}
p{font-size:34px;line-height:1.45;color:#d6d6da}
.lead{font-family:"Liberation Serif",Georgia,serif;font-size:44px;line-height:1.3;color:#fff}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:20px;letter-spacing:.22em;text-transform:uppercase;color:#8b8b90}
.foot .brand{color:#fff;font-weight:700}
.rule{width:64px;height:4px;background:#e1262f;margin:40px 0}
.note{font-size:24px;line-height:1.5;color:#b7b7bc;border-left:4px solid #e1262f;padding-left:22px}
"""

def foot(i):
    return f'<div class="foot"><span class="brand">Timas Motion</span><span>TM-003 · {i:02d}/10</span></div>'

def bg(n, veil, pos='center'):
    return f'<div class="bg" style="background-image:url({img(n)});background-position:{pos}"></div><div class="veil" style="background:{veil}"></div>'

DARK_BOTTOM = 'linear-gradient(180deg,rgba(10,10,11,.78) 0%,rgba(10,10,11,.2) 20%,rgba(10,10,11,.45) 42%,rgba(10,10,11,.9) 62%,rgba(10,10,11,.97) 100%)'
DARK_FULL = 'rgba(10,10,11,.72)'
def foot(i): return f'<div class="foot"><span class="brand">Timas Motion</span><span>TM-002 · {i:02d}/10</span></div>'
def bg(t, veil, pos='center'):
    return f'<div class="bg" style="background-image:url({img(t)});background-position:{pos}"></div><div class="veil" style="background:{veil}"></div>'

def moment(t, n, title, text, pos='center'):
    return bg(t, DARK_BOTTOM, pos) + f'''<div class="c">
<p class="eb"><b>{n}</b> · The sequence</p>
<div style="margin-top:auto">
<h2>{title}</h2>
<p style="margin-top:28px">{text}</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>'''

s = []
s.append(bg('28.5', DARK_BOTTOM, 'center 60%') + '''<div class="c">
<p class="eb"><b>TM-002</b> · Workshop reel</p>
<div style="margin-top:auto">
<h1>Premium Jeep<br>Workshop</h1>
<div class="rule"></div>
<p class="lead">Craftsmanship, on screen.</p>
<p class="note" style="margin-top:40px">Reel created for a specialist Jeep workshop. AI-assisted production.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')
s.append(bg('1', DARK_FULL) + '''<div class="c">
<p class="eb"><b>01</b> · The brief</p>
<h2 style="margin-top:80px">Specialist work <span>is hard to see.</span></h2>
<p class="lead" style="margin-top:56px">Show the precision behind specialist Jeep workmanship through a distinctive cinematic identity.</p>
@@FOOT@@</div>''')
s.append('''<div class="c">
<p class="eb"><b>02</b> · The strategy</p>
<h2 style="margin-top:80px">Build the identity <span>around craftsmanship.</span></h2>
<div style="margin-top:64px">''' + ''.join(
    f'<p class="lead" style="padding:18px 0;border-bottom:1px solid #2a2a2e{";color:#ff4a52" if k==4 else ""}">{t}</p>'
    for k, t in enumerate(['The bay.', 'The tools.', 'The hands at work.', 'The parts.', 'The finished vehicle.'])) + '''</div>
@@FOOT@@</div>''')
s.append(moment('4.5', '03', 'The bay.', 'An empty, lit workshop before any work begins.'))
s.append(moment('7.5', '04', 'The tools.', 'Diagnostics and hand tools laid out on the bench.', 'center 70%'))
s.append(moment('22.5', '05', 'The hands <span>at work.</span>', 'Brake work, shown close: gloves, disc and caliper.'))
s.append(moment('24', '06', 'The parts.', 'Suspension components on the bench.', 'center 60%'))
s.append(moment('25.5', '07', 'The finished <span>vehicle.</span>', 'The Jeep in the bay, after the work.', 'center 60%'))
s.append(bg('15', DARK_BOTTOM, 'center 55%') + '''<div class="c">
<p class="eb"><b>08</b> · The film</p>
<div style="margin-top:auto">
<h2>A 30-second <span>vertical reel.</span></h2>
<p style="margin-top:32px">No on-screen text. The workshop, its tools, brake and suspension work, closing on the finished Jeep at sunset.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')
s.append('''<div class="c">
<p class="eb"><b>09</b> · Watch the film</p>
<h2 style="margin-top:80px">The work tells <span>the story.</span></h2>
<p style="margin-top:48px">No slogan and no on-screen text. Each shot shows one part of the job: the bay, the tools, the brakes, the suspension, the finished Jeep.</p>
<div style="margin-top:auto">
<p class="lead">See the reel and the other cases</p>
<p style="font-size:28px;color:#ff4a52;margin-top:12px">timasmotion.com/#work</p>
<p class="note" style="margin-top:44px">Reel by Timas Motion for a specialist Jeep workshop. AI-assisted production. No commercial results are claimed.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')

s = [b.replace('@@FOOT@@', foot(i)) for i, b in enumerate(s, 1)]
pngs = []
with sync_playwright() as p:
    b = p.chromium.launch(**({'executable_path': os.environ['CHROMIUM']} if os.environ.get('CHROMIUM') else {}))
    pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for i, body in enumerate(s, 1):
        html = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s">{body}</div></body></html>'
        path = os.path.join(OUT, f'slide-{i:02d}.html'); open(path, 'w').write(html)
        pg.goto('file://' + path); pg.wait_for_timeout(300)
        png = os.path.join(OUT, f'tm-002-carousel-{i:02d}.png'); pg.screenshot(path=png); pngs.append(png)
    b.close()
ims = [Image.open(x).convert('RGB') for x in pngs]
ims[0].save(os.path.join(OUT, 'tm-002-carousel-linkedin.pdf'), save_all=True, append_images=ims[1:], resolution=72)
sheet = Image.new('RGB', (5*216+40, 2*270+30), (19,19,18))
for i, im in enumerate(ims): sheet.paste(im.resize((216,270)), (10+(i%5)*220, 10+(i//5)*280))
sheet.save(os.path.join(OUT, 'overview.jpg'), quality=85)
print('ok', len(pngs))
