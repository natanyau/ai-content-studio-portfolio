# Gera o carrossel do case do Fogo (10 slides 1080x1350 + PDF para o LinkedIn).
# As imagens são frames do próprio filme (assets/fogo/fogo-final-reel.mp4, 1080x1920),
# extraídos na hora com ffmpeg para .carousel/fogo/frames/. As imagens de assets/fogo/
# têm só 512 px de largura e ficariam borradas num slide de 1080. Nada é gravado em assets/.
# Os textos saem da página do case (fogo-featured-case.html); se ela mudar, atualize aqui.
# Uso: python3 scripts/carousel-fogo.py   -> escreve em .carousel/fogo/out/ (não versionado)
# Em sessão remota do Claude Code: CHROMIUM=/opt/pw-browsers/chromium python3 scripts/carousel-fogo.py
# Precisa de: ffmpeg e pip install playwright pillow.
import os
import subprocess
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILM = os.path.join(ROOT, 'assets', 'fogo', 'fogo-final-reel.mp4')
WORK = os.path.join(ROOT, '.carousel', 'fogo')
FRAMES = os.path.join(WORK, 'frames')
OUT = os.path.join(WORK, 'out')
os.makedirs(FRAMES, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

# Segundo do filme -> plano usado no slide.
SHOTS = {'coast': '1.5', 'street': '8', 'church': '10.6', 'coffee': '14',
         'sunset': '21', 'cha': '27', 'village': '34.5', 'last': '38.5'}
for name, t in SHOTS.items():
    dst = os.path.join(FRAMES, f'{name}.jpg')
    if not os.path.exists(dst):
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', t, '-i', FILM,
                        '-frames:v', '1', '-q:v', '2', dst], check=True)

def img(name): return f'file://{FRAMES}/{name}.jpg'

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

def foot(i): return f'<div class="foot"><span class="brand">Timas Motion</span><span>Fogo · {i:02d}/10</span></div>'
def bg(name, veil, pos='center'):
    return f'<div class="bg" style="background-image:url({img(name)});background-position:{pos}"></div><div class="veil" style="background:{veil}"></div>'

DARK_BOTTOM = 'linear-gradient(180deg,rgba(10,10,11,.78) 0%,rgba(10,10,11,.2) 20%,rgba(10,10,11,.45) 42%,rgba(10,10,11,.9) 62%,rgba(10,10,11,.97) 100%)'
DARK_FULL = 'rgba(10,10,11,.74)'

s = []
# 1 capa
s.append(bg('cha', DARK_BOTTOM, 'center 45%') + '''<div class="c">
<p class="eb"><b>Fogo</b> · Independent creative case study</p>
<div style="margin-top:auto">
<h1>Fogo</h1>
<p class="eb" style="margin-top:14px">Cape Verde</p>
<div class="rule"></div>
<p class="lead">Shaped by Fire. Defined by Life.</p>
<p style="margin-top:18px">A reference-informed cinematic interpretation of Fogo Island.</p>
<p class="note" style="margin-top:40px">Self-initiated by Timas Motion. Not a commissioned tourism campaign.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')
# 2 desafio
s.append('''<div class="c">
<p class="eb"><b>01</b> · The challenge</p>
<h2 style="margin-top:80px">More than <span>the volcano.</span></h2>
<p class="lead" style="margin-top:56px">How can an island shaped by a volcano be presented without reducing it to the volcano itself?</p>
<p style="margin-top:48px">Fogo combines black volcanic landscapes with agriculture, historic architecture, mountain communities and everyday life.</p>
<p style="margin-top:28px;color:#fff">The aim was to show what is already there, not to reinvent the island.</p>
@@FOOT@@</div>''')
# 3 insight
s.append(bg('coast', DARK_FULL) + '''<div class="c">
<p class="eb"><b>02</b> · The insight</p>
<h2 style="margin-top:80px">Authenticity became <span>the strategy.</span></h2>
<p style="margin-top:56px">The material for the story already existed: land, communities, cultivation, architecture and the Atlantic.</p>
<p class="lead" style="margin-top:48px">AI could support light, composition and atmosphere. Local reference remained the filter.</p>
@@FOOT@@</div>''')
# 4 conceito
s.append(bg('sunset', DARK_BOTTOM, 'center 40%') + '''<div class="c">
<p class="eb"><b>03</b> · The concept</p>
<div style="margin-top:auto">
<h1 style="font-size:96px">SHAPED BY FIRE.<br> <span>DEFINED BY LIFE.</span></h1>
<p style="margin-top:40px">The volcano formed the island’s landscape. The concept places equal weight on the people, crops and towns that live within it.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')
# 5 direção criativa (grade)
grid = [('coast', 'Volcanic coast'), ('street', 'São Filipe'), ('coffee', 'Coffee cultivation'),
        ('cha', 'Volcanic terrain'), ('village', 'Community life'), ('last', 'Rural daily life')]
cells = ''.join(f'''<div style="position:relative;overflow:hidden;border-radius:4px">
<div style="position:absolute;inset:0;background:url({img(n)}) center/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,transparent 50%,rgba(10,10,11,.92))"></div>
<div style="position:absolute;left:16px;bottom:14px;right:12px;font-family:'Liberation Serif',serif;font-size:26px;line-height:1.1">{t}</div></div>''' for n, t in grid)
s.append(f'''<div class="c">
<p class="eb"><b>04</b> · Creative direction</p>
<h2 style="font-size:64px;margin-top:40px">Elevated in presentation, <span>believable in place.</span></h2>
<div style="flex:1;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr);gap:12px;margin:40px 0 40px">{cells}</div>
@@FOOT@@</div>''')
# 6 referência
s.append(bg('coffee', 'linear-gradient(180deg,rgba(10,10,11,.6) 0%,rgba(10,10,11,.25) 25%,rgba(10,10,11,.92) 50%,rgba(10,10,11,.97) 100%)', 'center 30%') + '''<div class="c">
<p class="eb"><b>05</b> · Reference &amp; decisions</p>
<div style="margin-top:auto">
<h2 style="font-size:72px">Could this realistically <span>belong to Fogo?</span></h2>
<p style="margin-top:32px">The municipality of Mosteiros describes coffee cultivation on volcanic soils at 350–1,300 meters. The coffee study keeps three elements: cultivation in front, mountain relief and settlement behind.</p>
<p class="note" style="margin-top:32px">An AI-assisted visual study. It does not document a real plantation or viewpoint.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')
# 7 fontes
srcs = [('Câmara Municipal dos Mosteiros — Café do Fogo', 'Coffee cultivation, volcanic soils and the upland growing areas of Mosteiros.'),
        ('Portal da Ilha do Fogo — História de São Filipe', 'The coastal setting and historic sobrados of São Filipe.')]
rows = ''.join(f'<div style="padding:28px 0;border-bottom:1px solid #2a2a2e"><div style="font-size:30px;font-weight:700;color:#fff">{a}</div><div style="font-size:26px;color:#b7b7bc;margin-top:10px;line-height:1.4">{b}</div></div>' for a, b in srcs)
s.append(f'''<div class="c">
<p class="eb"><b>05</b> · Local context</p>
<h2 style="font-size:72px;margin-top:60px">Public sources <span>set the boundaries.</span></h2>
<div style="margin-top:44px">{rows}</div>
<p class="note" style="margin-top:44px">The sources give context for the themes. They do not certify the generated scenes or document the original production process.</p>
@@FOOT@@</div>''')
# 8 produção
s.append(bg('church', DARK_FULL) + '''<div class="c">
<p class="eb"><b>06</b> · The production</p>
<h2 style="margin-top:80px">AI assisted. <span>Human direction decided.</span></h2>
<p style="font-family:'Liberation Serif',serif;font-size:40px;color:#fff;margin-top:56px;line-height:1.4">Reference → Prompt → Generate → Evaluate → Refine → Approve</p>
<p style="margin-top:48px">Each scene was judged for believability before visual impact. Scenes that looked striking but did not read as Fogo were refined or left out.</p>
@@FOOT@@</div>''')
# 9 filme
s.append(bg('last', DARK_BOTTOM, 'center 40%') + '''<div class="c">
<p class="eb"><b>07</b> · The film</p>
<div style="margin-top:auto">
<h2>A 39-second <span>vertical film.</span></h2>
<p style="margin-top:32px">From the volcanic landscape to the life around it. The film ends on everyday village life, not on the volcano.</p>
<p class="note" style="margin-top:36px">AI-assisted cinematic interpretation. Not presented as documentary photography.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')
# 10 chamada
s.append('''<div class="c">
<p class="eb"><b>08</b> · The outcome</p>
<h2 style="margin-top:80px">Research, direction, <span>studies and a film.</span></h2>
<p style="margin-top:48px">Understand the place. Find the story. Protect the identity. Elevate the presentation.</p>
<div style="margin-top:auto">
<p class="lead">Explore the full case</p>
<p style="font-size:28px;color:#ff4a52;margin-top:12px">timasmotion.com/fogo-featured-case.html</p>
<p class="note" style="margin-top:44px">Independent creative case study, self-initiated by Timas Motion. Not a commissioned tourism campaign. No commercial results are claimed.</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')

s = [b.replace('@@FOOT@@', foot(i)) for i, b in enumerate(s, 1)]
pngs = []
with sync_playwright() as p:
    b = p.chromium.launch(**({'executable_path': os.environ['CHROMIUM']} if os.environ.get('CHROMIUM') else {}))
    pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for i, body in enumerate(s, 1):
        html = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s">{body}</div></body></html>'
        path = os.path.join(OUT, f'slide-{i:02d}.html')
        open(path, 'w').write(html)
        pg.goto('file://' + path)
        pg.wait_for_timeout(300)
        png = os.path.join(OUT, f'fogo-carousel-{i:02d}.png')
        pg.screenshot(path=png)
        pngs.append(png)
    b.close()

ims = [Image.open(x).convert('RGB') for x in pngs]
ims[0].save(os.path.join(OUT, 'fogo-carousel-linkedin.pdf'), save_all=True, append_images=ims[1:], resolution=72)
sheet = Image.new('RGB', (5 * 216 + 40, 2 * 270 + 30), (19, 19, 18))
for i, im in enumerate(ims):
    sheet.paste(im.resize((216, 270)), (10 + (i % 5) * 220, 10 + (i // 5) * 280))
sheet.save(os.path.join(OUT, 'overview.jpg'), quality=85)
print('ok', len(pngs))
