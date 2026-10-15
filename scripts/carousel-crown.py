# Gera o carrossel do case da Crown (10 slides 1080x1350 + PDF para o LinkedIn).
# A Crown é um case de estratégia, não de filme: o "filme" é um cartão de marca de 4 s.
# Imagens: um frame do cartão (assets/media/crown.mp4, 1080x1920) e as duas imagens de produto
# (assets/images/rt*.png), copiadas para .carousel/crown/frames/ sem a faixa do rodapé: a
# ressalva já aparece na capa e no último slide, e em letra pequena só repetiria. (Até out/2026
# essa faixa dizia "or officially affiliated with...", o que é falso neste case; as imagens
# foram refeitas com a ressalva da página.) Nada é gravado em assets/.
# A ressalva usada é a da página: "Not commissioned, reviewed, or endorsed by Crown Automotive Sales."
# Os textos saem de crown-featured-case.html; se ela mudar, atualize aqui.
# Uso: python3 scripts/carousel-crown.py   -> escreve em .carousel/crown/out/ (não versionado)
# Em sessão remota do Claude Code: CHROMIUM=/opt/pw-browsers/chromium python3 scripts/carousel-crown.py
# Precisa de: ffmpeg e pip install playwright pillow.
import os
import subprocess
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '.carousel', 'crown')
FRAMES = os.path.join(WORK, 'frames')
OUT = os.path.join(WORK, 'out')
os.makedirs(FRAMES, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

card = os.path.join(FRAMES, 'card.jpg')
if not os.path.exists(card):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', '3.5',
                    '-i', os.path.join(ROOT, 'assets', 'media', 'crown.mp4'),
                    '-frames:v', '1', '-q:v', '2', card], check=True)
# 1491x1055; a faixa do rodapé começa logo abaixo da linha 985.
for name in ('rt28111-led-tail-light', 'rt31046-big-brake-kit'):
    dst = os.path.join(FRAMES, name + '.png')
    if not os.path.exists(dst):
        Image.open(os.path.join(ROOT, 'assets', 'images', name + '.png')).crop((0, 0, 1491, 985)).save(dst)

def img(name): return f'file://{FRAMES}/{name}'

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

def foot(i): return f'<div class="foot"><span class="brand">Timas Motion</span><span>Crown · {i:02d}/10</span></div>'
def bg(name, veil, pos='center'):
    return f'<div class="bg" style="background-image:url({img(name)});background-position:{pos}"></div><div class="veil" style="background:{veil}"></div>'

DARK_BOTTOM = 'linear-gradient(180deg,rgba(10,10,11,.5) 0%,rgba(10,10,11,.15) 25%,rgba(10,10,11,.6) 48%,rgba(10,10,11,.94) 64%,rgba(10,10,11,.98) 100%)'
NOTE = 'Not commissioned, reviewed, or endorsed by Crown Automotive Sales.'

def rows(items, size=34):
    return ''.join(f'<div style="display:flex;gap:28px;padding:20px 0;border-bottom:1px solid #2a2a2e"><div style="font-size:22px;font-weight:700;letter-spacing:.18em;color:#ff4a52;padding-top:8px">{k:02d}</div><div style="font-size:{size}px;line-height:1.3;color:#fff">{t}</div></div>' for k, t in enumerate(items, 1))

def product(name, eb, title, part, extra, text, note=''):
    return f'''<div class="c">
<p class="eb"><b>{eb}</b> · Product application visual</p>
<h2 style="font-size:58px;margin-top:40px">{title}</h2>
<div style="margin-top:36px;height:500px;background:url({img(name + '.png')}) center/contain no-repeat;border:1px solid #2a2a2e;border-radius:4px"></div>
<div style="display:flex;gap:56px;margin-top:32px;font-size:26px;color:#b7b7bc"><div><div style="font-size:20px;letter-spacing:.2em;text-transform:uppercase;color:#ff4a52">Part number</div><div style="color:#fff;font-size:32px;margin-top:6px">{part}</div></div><div><div style="font-size:20px;letter-spacing:.2em;text-transform:uppercase;color:#ff4a52">Application</div><div style="color:#fff;font-size:32px;margin-top:6px">Jeep Wrangler JK, 2007–2018</div></div></div>
<p style="margin-top:28px;font-size:28px">{text}</p>{note}
@@FOOT@@</div>'''

s = []
# 1 capa
s.append('<div class="bg" style="bottom:auto;height:430px;background-image:url(' + img('card.jpg') + ');background-size:100% auto;background-position:0 -690px"></div><div class="veil" style="bottom:auto;height:430px;background:linear-gradient(180deg,rgba(10,10,11,.2) 0%,rgba(10,10,11,0) 40%,#0a0a0b 100%)"></div>' + f'''<div class="c">
<p class="eb"><b>Crown</b> · Independent strategic case study</p>
<div style="margin-top:auto">
<h1 style="font-size:104px">Crown<br>Automotive</h1>
<div class="rule"></div>
<p class="lead">Brand visibility &amp; content strategy for the Jeep parts market.</p>
<p class="note" style="margin-top:40px">A personal project by Timas Motion. {NOTE}</p>
</div>
<div style="height:48px"></div>@@FOOT@@</div>''')
# 2 contexto
s.append('''<div class="c">
<p class="eb"><b>01</b> · Context</p>
<h2 style="margin-top:80px">More than a <span>traditional listing.</span></h2>
<p class="lead" style="margin-top:56px">In a competitive aftermarket, product availability alone may not be enough to create strong brand visibility.</p>
<p style="margin-top:48px">Jeep parts customers may also value clear product education, application examples, compatibility information and installation context.</p>
<p class="note" style="margin-top:48px">The analysis does not evaluate confidential operations or internal performance. It covers publicly observable communication only.</p>
@@FOOT@@</div>''')
# 3 avaliação
s.append('''<div class="c">
<p class="eb"><b>02</b> · Communication assessment</p>
<h2 style="font-size:72px;margin-top:60px">Answer the customer’s <span>practical questions.</span></h2>
<div style="margin-top:40px">''' + rows(['What is the part?', 'Where does it fit?', 'What customer need does it address?', 'How is it used or installed?', 'Why is it relevant to the intended audience?']) + '''</div>
@@FOOT@@</div>''')
# 4 públicos
aud = [('Jeep owners &amp; enthusiasts', 'Vehicle-specific parts, upgrades, restoration support and clearer explanations.'),
       ('DIY customers, technicians &amp; installers', 'Fitment clarity, application context and installation guidance.'),
       ('Retailers &amp; industry professionals', 'Clearer product communication and customer-education assets.')]
s.append('''<div class="c">
<p class="eb"><b>02</b> · Audience</p>
<h2 style="font-size:72px;margin-top:60px">Who the communication <span>should serve.</span></h2>
<div style="margin-top:40px">''' + ''.join(f'<div style="padding:24px 0;border-bottom:1px solid #2a2a2e"><div style="font-size:32px;font-weight:700;color:#fff">{a}</div><div style="font-size:26px;color:#b7b7bc;margin-top:8px;line-height:1.4">{b}</div></div>' for a, b in aud) + '''</div>
<p class="note" style="margin-top:40px">Proposed for strategic planning. Not official Crown Automotive customer data or internal market research.</p>
@@FOOT@@</div>''')
# 5 pilares
s.append('''<div class="c">
<p class="eb"><b>04</b> · Content strategy</p>
<h2 style="font-size:72px;margin-top:60px">Five pillars for <span>clarity and consistency.</span></h2>
<div style="margin-top:40px">''' + rows(['Product education', 'Vehicle-specific applications', 'Installation &amp; practical guidance', 'Jeep culture &amp; visual storytelling', 'Retailer &amp; professional support']) + '''</div>
@@FOOT@@</div>''')
# 6 entregas
dl = [('Produced', 'Animated brand card', 'A 4-second vertical opener.'),
      ('Produced', 'Product application visuals', 'Two product-focused visuals.'),
      ('Storyboard ready', 'Educational short-form pilot', 'A five-scene vertical concept.'),
      ('Documented', 'AI-assisted script &amp; workflow', 'How AI supported planning, writing and visual direction.'),
      ('Documented', 'Technical validation guidelines', 'Fitment, specifications, claims, safety and sources.')]
s.append('''<div class="c">
<p class="eb"><b>05</b> · Deliverables</p>
<h2 style="font-size:72px;margin-top:60px">A realistic set <span>of assets.</span></h2>
<div style="margin-top:36px">''' + ''.join(f'<div style="padding:20px 0;border-bottom:1px solid #2a2a2e"><div style="font-size:19px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#ff4a52">{a}</div><div style="font-size:31px;font-weight:700;color:#fff;margin-top:6px">{b}</div><div style="font-size:24px;color:#b7b7bc;margin-top:4px">{c}</div></div>' for a, b, c in dl) + '''</div>
@@FOOT@@</div>''')
# 7 e 8 produtos
s.append(product('rt28111-led-tail-light', '07', 'RT Off-Road <span>LED Tail Light Set.</span>', 'RT28111',
                 '', 'Red lens. The visual introduces the product, its vehicle application and the customer need it addresses.'))
s.append(product('rt31046-big-brake-kit', '07', 'RT Off-Road <span>Front Big Brake Kit.</span>', 'RT31046',
                 '', 'A two-box product system, presented through packaging context, application and structured customer education.',
                 '<p class="note" style="margin-top:24px">Names, part numbers and applications checked against public listings from RT Off-Road and Quadratec.</p>'))
# 9 piloto
s.append('''<div class="c">
<p class="eb"><b>08</b> · Educational short-form pilot</p>
<h2 style="font-size:72px;margin-top:60px">Five scenes, <span>one product.</span></h2>
<p style="margin-top:28px">Built around the RT28111 LED Tail Light Set.</p>
<div style="margin-top:24px">''' + rows(['Hook: the visible upgrade', 'Product identification', 'Vehicle application', 'Customer need', 'Validation &amp; closing'], 32) + '''</div>
<p class="note" style="margin-top:36px">A storyboard and content concept, not a published campaign.</p>
@@FOOT@@</div>''')
# 10 chamada
s.append(f'''<div class="c">
<p class="eb"><b>Outcome</b></p>
<h2 style="margin-top:80px">Strategy <span>made visible.</span></h2>
<p style="margin-top:48px">An animated brand card, two product visuals and a five-scene storyboard. The educational pilot remains a concept.</p>
<div style="margin-top:auto">
<p class="lead">Explore the full case</p>
<p style="font-size:28px;color:#ff4a52;margin-top:12px">timasmotion.com/crown-featured-case.html</p>
<p class="note" style="margin-top:44px">Independent work by Timas Motion, produced on personal initiative. {NOTE} No measured commercial results are claimed.</p>
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
        png = os.path.join(OUT, f'crown-carousel-{i:02d}.png')
        pg.screenshot(path=png)
        pngs.append(png)
    b.close()

ims = [Image.open(x).convert('RGB') for x in pngs]
ims[0].save(os.path.join(OUT, 'crown-carousel-linkedin.pdf'), save_all=True, append_images=ims[1:], resolution=72)
sheet = Image.new('RGB', (5 * 216 + 40, 2 * 270 + 30), (19, 19, 18))
for i, im in enumerate(ims):
    sheet.paste(im.resize((216, 270)), (10 + (i % 5) * 220, 10 + (i // 5) * 280))
sheet.save(os.path.join(OUT, 'overview.jpg'), quality=85)
print('ok', len(pngs))
