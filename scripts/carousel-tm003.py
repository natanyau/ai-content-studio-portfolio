# Gera o carrossel do TM-003 (10 slides 1080x1350 + PDF para o LinkedIn).
# Molde para os próximos cases: troque os textos dos slides e a função img().
# Uso: python3 scripts/carousel-tm003.py   -> escreve em .carousel/out/ (área de trabalho, não versionada)
# Precisa de: pip install playwright pillow. Os textos usam Liberation Serif/Sans; no Mac,
# troque por Georgia/Helvetica se quiser as fontes do site.
import os
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'images')
OUT = os.path.join(ROOT, '.carousel', 'out')
os.makedirs(OUT, exist_ok=True)

def img(n):
    names = {1: '01-morning', 2: '02-wake', 3: '03-breakfast', 4: '04-prepare', 5: '05-into-valley',
             6: '06-through-valley', 7: '07-return', 8: '08-rest', 9: '09-closing'}
    return f'file://{IMG}/tm-003-{names[n]}.jpg'

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

slides = []

# 1 cover
slides.append(bg(1, DARK_BOTTOM, 'center 40%') + f'''<div class="c">
<p class="eb"><b>TM-003</b> · Independent creative case study</p>
<div style="margin-top:auto">
<h1>Casa<br>Cavoquinho</h1>
<div class="rule"></div>
<p class="lead">Stay in the Rhythm of the Valley.</p>
<p style="margin-top:18px">A hospitality study built around the guest journey through the Paul Valley, Santo Antão, Cape Verde.</p>
<p class="note" style="margin-top:40px">Not commissioned by or officially affiliated with Casa Cavoquinho.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')

# 2 challenge
slides.append(f'''<div class="c">
<p class="eb"><b>01</b> · The challenge</p>
<h2 style="margin-top:80px">More than a place <span>to stay.</span></h2>
<p style="margin-top:56px">Casa Cavoquinho already publishes the practical side of a stay: valley-view rooms, breakfast and dinner, hiking information and access to the Paul Valley.</p>
<p class="lead" style="margin-top:56px">How can a rural guesthouse be presented not only as accommodation in the valley, but as a base for experiencing the valley itself?</p>
@@FOOT@@</div>''')

# 3 insight
slides.append(bg(5, DARK_FULL) + f'''<div class="c">
<p class="eb"><b>02</b> · The insight</p>
<h2 style="margin-top:80px">The stay already <span>follows a sequence.</span></h2>
<div style="margin-top:64px">''' + ''.join(
    f'<p class="lead" style="padding:18px 0;border-bottom:1px solid rgba(255,255,255,.18){";color:#ff4a52" if k==4 else ""}">{t}</p>'
    for k, t in enumerate(['Wake in the valley.', 'Move through it.', 'Experience the landscape.', 'Return to the same base.', 'Slow down.'])) + f'''</div>
@@FOOT@@</div>''')

# 4 strategy
slides.append(f'''<div class="c">
<p class="eb"><b>03</b> · The strategy</p>
<h2 style="margin-top:80px">The property is the base.<br><span>The valley is the experience.</span></h2>
<p class="lead" style="margin-top:56px">The guest connects the two.</p>
<div class="rule"></div>
<p style="font-family:'Liberation Serif',serif;font-size:56px;color:#fff">Casa <span style="color:#e1262f">→</span> Valley <span style="color:#e1262f">→</span> Casa</p>
<p style="margin-top:28px;color:#b7b7bc">wake → prepare → explore → return → rest</p>
@@FOOT@@</div>''')

# 5 big idea
slides.append(bg(9, DARK_BOTTOM, 'center 55%') + f'''<div class="c">
<p class="eb"><b>04</b> · The big idea</p>
<div style="margin-top:auto">
<h1 style="font-size:104px">STAY IN THE RHYTHM <span>OF THE VALLEY.</span></h1>
<p style="margin-top:40px">“Stay” ties the line to hospitality. “Rhythm” carries the pace of the day: waking, moving through the valley, returning and slowing down.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')

# 6 nine moments
labels = ['Morning Presence', 'Wake', 'Breakfast', 'Preparation', 'Into the Valley', 'Through the Valley', 'The Return', 'Late-Afternoon Rest', 'The Promise']
cells = ''.join(f'''<div style="position:relative;overflow:hidden;border-radius:4px">
<div style="position:absolute;inset:0;background:url({img(k+1)}) center/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(10,10,11,.92))"></div>
<div style="position:absolute;left:16px;bottom:14px;right:12px"><div style="font-size:18px;font-weight:700;letter-spacing:.18em;color:#e1262f">{k+1:02d}</div><div style="font-family:'Liberation Serif',serif;font-size:26px;line-height:1.1;margin-top:4px">{labels[k]}</div></div></div>''' for k in range(9))
slides.append(f'''<div class="c">
<p class="eb"><b>07</b> · The production</p>
<h2 style="font-size:64px;margin-top:40px">Nine moments. <span>One guest journey.</span></h2>
<div style="flex:1;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:12px;margin:40px 0 40px">{cells}</div>
@@FOOT@@</div>''')

# 7 creative direction
trio = [(3, 'Inside', 'Closer, calmer, human.'), (6, 'Outside', 'Wider landscapes, movement.'), (8, 'Return', 'Intimate again.')]
cols = ''.join(f'''<div style="display:flex;flex-direction:column;gap:18px">
<div style="flex:1;background:url({img(n)}) center/cover;border-radius:4px"></div>
<div style="font-size:20px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#e1262f">{t}</div>
<div style="font-size:26px;line-height:1.35;color:#d6d6da">{d}</div></div>''' for n, t, d in trio)
slides.append(f'''<div class="c">
<p class="eb"><b>05</b> · Creative direction</p>
<h2 style="font-size:64px;margin-top:40px">A day in the valley, <span>not an ad about it.</span></h2>
<div style="flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:44px 0 40px">{cols}</div>
@@FOOT@@</div>''')

# 8 research
srcs = [('Casa Cavoquinho — Official website', 'Rooms, meals, hiking information.'),
        ('Casa Cavoquinho — The Guesthouse', 'Breakfast, dinner after hiking, environmental practices.'),
        ('UNESCO World Heritage Centre', 'Tentative List: Parc Naturel Cova, Paúl et Ribeira da Torre.'),
        ('Visit Santo Antão', 'Location and destination context.')]
rows = ''.join(f'<div style="padding:26px 0;border-bottom:1px solid #2a2a2e"><div style="font-size:30px;font-weight:700;color:#fff">{a}</div><div style="font-size:26px;color:#b7b7bc;margin-top:8px">{b}</div></div>' for a, b in srcs)
slides.append(f'''<div class="c">
<p class="eb"><b>06</b> · Research &amp; reality</p>
<h2 style="font-size:72px;margin-top:60px">Public sources <span>set the boundaries.</span></h2>
<div style="margin-top:44px">{rows}</div>
<p class="note" style="margin-top:44px">Sources ground the context. They do not authenticate the AI-generated scenes, which are conceptual interpretations.</p>
@@FOOT@@</div>''')

# 9 film
slides.append(bg(7, DARK_BOTTOM, 'center 40%') + f'''<div class="c">
<p class="eb"><b>09</b> · The final film</p>
<div style="margin-top:auto">
<h2>A 36-second <span>hospitality film.</span></h2>
<p style="margin-top:32px">One complete guest journey: wake, explore, return, rest. Vertical 9:16.</p>
<p class="note" style="margin-top:36px">AI-assisted cinematic interpretation. Not documentary footage of the property.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')

# 10 CTA
slides.append(f'''<div class="c">
<p class="eb"><b>10</b> · The outcome</p>
<h2 style="margin-top:80px">A complete hospitality <span>communication concept.</span></h2>
<p style="margin-top:48px">Research grounded the project. Strategy gave it direction. The guest journey gave it structure. The film gave it form.</p>
<div style="margin-top:auto">
<p class="lead">Explore the full case</p>
<p style="font-size:28px;color:#ff4a52;margin-top:12px">timasmotion.com/tm-003-casa-cavoquinho.html</p>
<p class="note" style="margin-top:44px">Independent creative case study by Timas Motion. Not commissioned by or officially affiliated with Casa Cavoquinho. No commercial results are claimed.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')

slides = [slides[i] for i in (0,1,2,3,4,6,7,5,8,9)]
slides = [b.replace('@@FOOT@@', foot(i)) for i, b in enumerate(slides, 1)]
pngs = []
with sync_playwright() as p:
    # Em sessão remota do Claude Code: CHROMIUM=/opt/pw-browsers/chromium python3 scripts/carousel-tm003.py
    b = p.chromium.launch(**({'executable_path': os.environ['CHROMIUM']} if os.environ.get('CHROMIUM') else {}))
    pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for i, body in enumerate(slides, 1):
        html = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s">{body}</div></body></html>'
        path = os.path.join(OUT, f'slide-{i:02d}.html')
        open(path, 'w').write(html)
        pg.goto('file://' + path)
        pg.wait_for_function("document.fonts.ready.then(()=>true)")
        pg.wait_for_timeout(400)
        png = os.path.join(OUT, f'tm-003-carousel-{i:02d}.png')
        pg.screenshot(path=png)
        pngs.append(png)
    b.close()

ims = [Image.open(x).convert('RGB') for x in pngs]
ims[0].save(os.path.join(OUT, 'tm-003-carousel-linkedin.pdf'), save_all=True, append_images=ims[1:], resolution=72)
sheet = Image.new('RGB', (5 * 216 + 40, 2 * 270 + 30), (19, 19, 18))
for i, im in enumerate(ims):
    sheet.paste(im.resize((216, 270)), (10 + (i % 5) * 220, 10 + (i // 5) * 280))
sheet.save(os.path.join(OUT, 'overview.jpg'), quality=85)
print('ok', len(pngs))
