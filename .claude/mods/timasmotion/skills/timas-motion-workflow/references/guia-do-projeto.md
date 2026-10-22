# Timas Motion — guia do projeto

Portfólio estático da Timas Motion, publicado pelo **GitHub Pages** em
`https://timasmotion.com` (domínio próprio, via arquivo `CNAME` na raiz).
Sem build, sem framework, sem dependências: o que está no repositório é exatamente
o que vai ao ar quando o `main` recebe um push.

## Estrutura

| Caminho | O que é |
|---|---|
| `index.html` | Site principal. CSS e JS **inline por opção** (arquivo único, zero requisições extras). |
| `crown-featured-case.html` | Case Crown. Único arquivo que usa CSS externo (`css/crown-case.css`). |
| `404.html` | Página de erro servida pelo Pages. |
| `assets/media/` | Vídeos `.mp4` + posters `.jpg` de cada seção. Cada vídeo **precisa** do `.jpg` de mesmo nome como fallback. |
| `CNAME` | Domínio próprio do Pages. **Se sumir, o site volta para a URL do github.io e o `robots.txt` deixa de valer.** |
| `preview.jpg` | Imagem de preview de link (Open Graph), 1200×630. |
| `scripts/check.sh` | Verificação pré-publicação. Também roda sozinho no GitHub a cada push (`.github/workflows/check.yml`): erro vira ✗ vermelho no commit, aviso só aparece no resumo da execução. |
| `scripts/shots.sh` | Screenshots em mobile/tablet/desktop. |
| `scripts/watermark.sh` | Aplica a marca d'água nos vídeos e regenera os posters. |
| `scripts/carousel-tm003.py` | Gera o carrossel do TM-003 (PNG 1080×1350 + PDF). Molde para os próximos cases. |
| `scripts/carousel-tm002.py` | Carrossel do TM-002 (oficina Jeep). Tira os frames do próprio `case2.mp4` na hora; não grava em `assets/`. |
| `scripts/carousel-fogo.py` | Carrossel do Fogo. Frames do próprio filme (1080×1920); as imagens de `assets/fogo/` têm 512 px e borram no slide. |
| `scripts/carousel-crown.py` | Carrossel da Crown. Case de estratégia: usa um frame do cartão de marca e as duas imagens de produto (`assets/images/rt*.png`) sem a faixa do rodapé. |
| `docs/archive/` | Deck antigo, fora da raiz publicada e marcado `noindex`. Não é mantido. |
| `_config.yml` | Única função: tirar `CLAUDE.md`, `scripts/` e `.claude/` do site publicado. Não é build. |
| `.claude/mods/timasmotion/` | Plugin `timasmotion` do Claude Code, com tudo o que é do processo: os comandos em `commands/` (`/verificar`, `/olhar`, `/publicar`, `/novo-case <código e nome>`, que leva um case novo do material à prévia e para antes de publicar, e `/carrossel <case>`, que monta o carrossel a partir da página e do filme), a skill `skills/timas-motion-workflow/` com o processo completo e, em `hooks/`, a trava que barra `Edit`, `Write` e comandos de shell que alterem `assets/` (regra 4). Na skill, `references/guia-do-projeto.md` é uma cópia deste arquivo: ao mudar uma regra aqui, copie de novo. `references/perfil-de-voz.md` descreve a voz dos textos, com exemplos dos cases. |
| `.claude/mods/` | Marketplace local (`timas-mods`). Um hook de `SessionStart` em `.claude/settings.json` instala o `timasmotion` com escopo `local` quando ele falta, inclusive em container novo na nuvem, e remove o antigo `trava-assets`. Vale já na sessão que o instalou. Se a instalação falhar, os comandos somem e o hook avisa; a regra 4 continua valendo. O plugin é lido direto da pasta: depois de editar, `/reload-plugins`. Testes: `claude plugin test .claude/mods/timasmotion`. |

## Regras que evitam quebrar o site

1. **Não converta o CSS/JS inline do `index.html` em arquivos separados.** É decisão de
   arquitetura, não descuido. O mesmo vale para não "modernizar" para React/Vite/Tailwind.
2. **Links internos de navegação saem da raiz** (`/`, `/terms.html`), porque o site tem
   domínio próprio. Já os assets usam caminho relativo (`assets/media/...`). Não unifique
   os dois — cada um está certo no seu contexto.
   Até setembro de 2026 o site vivia em `natanyau.github.io/ai-content-studio-portfolio/`
   e esses links carregavam o prefixo do subdiretório. Se encontrar `/ai-content-studio-portfolio/`
   em algum lugar, é resquício: hoje leva a 404.
3. **Toda página precisa começar com `<!DOCTYPE html>`** e ter `<html lang>`, `<meta charset>`
   e `<meta name="viewport">`. Sem o DOCTYPE o browser entra em *quirks mode*; sem o viewport
   o celular renderiza a 980px. Já aconteceu neste repositório.
4. **Nunca edite nada em `assets/`.** São arquivos binários de produção; substituir só
   manualmente, com o arquivo novo em mãos.
5. **Vídeo novo entra sempre em par**: `nome.mp4` + `nome.jpg` (poster). Sem poster, a seção
   fica preta em quem tem autoplay bloqueado. Se o vídeo tem marca d'água, o poster
   precisa ter também — é o poster que a maioria vê, não o vídeo.
6. **Página nova precisa entrar no `sitemap.xml`** e levar `title`, `description`, `canonical`
   e `og:image` — senão o link compartilhado no LinkedIn/WhatsApp sai sem preview.
7. **Não mexa em `robots.txt` nem em `sitemap.xml` sem motivo declarado.**
   O `robots.txt` **está em vigor** desde a migração para domínio próprio: ele é servido
   em `timasmotion.com/robots.txt`, que é a raiz do domínio — o único lugar onde
   `robots.txt` vale. Antes disso o site era um *project site* e o arquivo ficava num
   subdiretório, onde nenhum crawler o lia. **Se o `CNAME` sair, ele volta a ser inerte.**
   Quem sustenta a reserva de direitos independente disso é o `terms.html`.
8. **Não apague o `_config.yml`.** Ele parece contradizer o "sem build" do topo, mas não
   adiciona etapa nenhuma: o GitHub Pages já roda o Jekyll neste repositório, com ou sem
   ele. O que o arquivo faz é preencher o `exclude`. Sem isso o build copia todo arquivo
   da raiz que não comece com `.` ou `_`, e `CLAUDE.md` vira uma página legível em
   `/ai-content-studio-portfolio/CLAUDE.md` — Markdown sem front matter não é convertido,
   é servido verbatim. O mesmo valia para os `.sh` de `scripts/`. Isso cobre só o site;
   o repositório é público e esses arquivos continuam à vista no GitHub, que é onde eles
   têm utilidade. Ao criar um arquivo de trabalho novo na raiz, acrescente-o ao `exclude`.
   O `check.sh` cobra isso: avisa a cada arquivo da raiz que iria ao ar sem estar listado,
   e falha de vez se o `_config.yml` sumir.

## Antes de publicar (sempre nesta ordem)

```bash
bash scripts/check.sh     # 0 erros = pode publicar
bash scripts/shots.sh     # olhe .preview/*__mobile.png de verdade
python3 -m http.server 8000   # e abra http://localhost:8000
```

O `check.sh` valida: referências quebradas, tags desbalanceadas, DOCTYPE/meta ausentes,
`img` sem `alt`, sitemap desatualizado, assets órfãos ou pesados, arquivo de trabalho
vazando para o site publicado, e segredos commitados. A varredura de segredos cobre todo
arquivo de texto do repositório, não só o que vai ao ar: num repositório público um token
num `.md` ou num `.yml` fica igualmente exposto.
O `shots.sh` acusa scroll horizontal, quirks mode e erros de JS por viewport, e roda o
axe-core (WCAG 2.2 A/AA) em cada tela. O axe é baixado do npm na primeira vez para
`.preview/.axe/`, com versão e hash fixos no script; sem rede, as fotos saem e a
auditoria é pulada. "A conferir à mão" não é erro: é onde o axe não decide sozinho,
como texto sobre gradiente ou vídeo e falta de legenda. Um resultado limpo não quer
dizer página acessível: teclado, foco e leitor de tela continuam sendo teste manual.

Nenhum dos dois substitui abrir o site no seu celular antes de divulgar um link.

## Fluxo de trabalho

- Uma mudança por commit, com mensagem que diz **o efeito**, não o arquivo mexido.
- Mudança visual: rode `shots.sh` **antes e depois** e compare os PNGs. É a única forma
  barata de saber que você não quebrou o mobile ao consertar o desktop.
- Nunca commite direto no `main` sem ter rodado o `check.sh`.
- `.preview/` é ignorado pelo git — é área de trabalho, não entra no repositório.

## Marca d'água nos vídeos

`scripts/watermark.sh` aplica a marca e regenera os posters a partir do vídeo **já
marcado**. Precisa de `ffmpeg` (`brew install ffmpeg`) e de um PNG com fundo
transparente em `.watermark/mark.png`.

```bash
bash scripts/watermark.sh                      # todos os .mp4 de assets/
bash scripts/watermark.sh assets/media/who.mp4 # um só, para calibrar
MARK=~/Desktop/marca.png OPACITY=0.4 bash scripts/watermark.sh
```

O script **não** substitui nada em `assets/` — escreve em `.watermark/out/` e imprime
os comandos de cópia no fim. A troca é sua, depois de olhar o resultado, porque a
regra 4 vale aqui também.

**O teto de bitrate é amarrado à origem de cada arquivo** (`min(origem, BITRATE_CAP)`).
Sem isso o reencode incha: as fontes já vêm comprimidas entre 540 e 970 kbps, e um
`crf` generoso "melhora" o arquivo em vez de preservá-lo. Com o teto, os sete pequenos
param de inflar e só o reel do Fogo é de fato reduzido.

O `bufsize` é **1×** o `maxrate`, não 2×. O buffer VBV começa cheio, então ele é folga
que o codificador gasta por cima da média — num clipe de 10s essa folga pesa, e com o
buffer dobrado o arquivo ainda crescia ~20% apesar do teto.

O poster de cada vídeo sai do **HTML** (`data-poster` / `poster`), não do nome do
arquivo — o reel do Fogo, por exemplo, usa `cha.jpg`. Duas consequências que já
morderam:

- **Poster que o site também usa como imagem comum é pulado.** O `cha.jpg` aparece
  4× na galeria do case e como fundo no `index.html`; marcá-lo colocaria a marca em
  fotos. O script avisa quais pulou, para você decidir à mão.
- **A marca é aplicada sobre o poster que já existe**, nunca sobre um frame novo
  extraído do vídeo. O poster é um frame escolhido a dedo: no `who`, por exemplo,
  o segundo 1 do vídeo mostra o Jeep, não a garagem que a página exibe hoje. Marcar
  o próprio arquivo preserva o enquadramento e a resolução — quatro posters
  (`contact`, `cover`, `philosophy`, `who`) são 1080×1920 num vídeo de 720×1280.
  A marca escala junto: 120px no vídeo de 720 vira 180px no poster de 1080.

### Dois arquivos precisam de ajuste próprio

Descobertos medindo os oito, não dá para o script adivinhar:

```bash
BITRATE_CAP=940 bash scripts/watermark.sh assets/media/cover.mp4  # cena difícil
MARGIN=220      bash scripts/watermark.sh assets/media/crown.mp4  # rodapé ocupado
```

- **`cover`** é a cena do Jeep levantando poeira sobre cascalho: detalhe fino em
  movimento, o pior caso para o x264. No padrão é o único que ainda cresce (~1,7%) e o
  de pior VMAF (84,4). A culpa é do codec, não da marca — medido com e sem ela, a
  diferença foi de 1,4 ponto.

  **`BITRATE_CAP=940` é o ajuste, e foi medido:** a nota fica perto de 84, o arquivo
  para de crescer, e lado a lado com o `crf 23` não há diferença visível (mesma textura
  nas pedras, mesma suavização da poeira). `CRF=21` foi tentado antes e **não** resolveu
  — o gargalo é o teto, não a qualidade-alvo.

- **`crown`** tem texto queimado no rodapé do vídeo ("THE JEEP AUTHORITY /
  CROWNAUTOMOTIVE.NET") com uma linha horizontal acima. Na margem padrão de 140 a marca
  cai em cima da linha, entre os dois textos. `MARGIN=220` sobe para a área limpa —
  medido no vídeo e no `crown.jpg`.

  Ele encolhe muito (−56%, 1,13 MB → 0,49 MB, VMAF 95,1) porque a origem vinha a 2265
  kbps, bitrate muito acima do que um card de gradiente precisa. Em contraste normal é
  indistinguível da origem e o texto do rodapé segue nítido. **Com contraste forçado 4×
  aparece um bloqueio leve nas bordas do brilho amarelo** — ponto fraco clássico de
  gradiente escuro. Não aparece em uso normal, mas pode surgir como banding em tela de
  brilho alto no escuro. Se aparecer, regenere o crown com um teto mais alto.

A marca em si (`.watermark/mark.png`) **não é versionada** — `.watermark/` é área de
trabalho, como `.preview/`. Guarde uma cópia fora do repositório.

Duas coisas que não dá para desfazer depois: **guarde os masters limpos fora do
repositório** (depois da troca o original some do projeto) e **calibre num arquivo só**
antes de processar os oito — reencode é perda, e rodar duas vezes perde duas vezes.

## Preview de link (Open Graph)

Cada página compartilhável tem `description`, `canonical`, `og:*` e `twitter:*`.
O `404.html` **não** tem, e isso está correto: página de erro não é indexada nem
compartilhada, e um `canonical` nela apontaria para o lugar errado.

- Home → `preview.jpg`
- Case da Crown → `assets/images/crown-case-preview.jpg`, que é o próprio herói da
  página renderizado a 1200x630. **Se o herói do case mudar, regenere a imagem**,
  senão o card compartilhado passa a mostrar uma versão que não existe mais.
- Case do Fogo → `assets/fogo-case-preview.jpg`, também o herói renderizado. Para caber
  o herói inteiro, renderize num viewport maior e reduza (1760×924 com
  `device_scale_factor` 1200/1760), ou capture só a `section.hero` e recorte 1200×630.
- Case TM-003 → `assets/tm-003-preview.jpg`, composição própria: grafite à esquerda
  com nome, linha e ressalva; frame do filme à direita.

O LinkedIn guarda o preview em cache por URL e não relê sozinho. Depois de mudar
qualquer `og:`, force a releitura no `linkedin.com/post-inspector/` — sem isso o
card antigo continua aparecendo por dias.

A descrição do case precisa manter a ressalva sobre a Crown Automotive, igual à que
a página exibe (aparece em três `meta`, na nota do herói e na do rodapé — os cinco
textos andam juntos). Não a remova para encurtar o texto.

O que a ressalva afirma é deliberado: **não encomendado, revisado ou endossado**. Ela
não diz "não afiliado" porque, neste caso, negar afiliação seria falso. A redação atual
é a única que cobre as duas coisas ao mesmo tempo: o case é independente e a página não
faz uma afirmação incorreta. Se alguém "restaurar" a redação antiga em nome da concisão,
volta a ser uma afirmação incorreta na página publicada.

As duas imagens de produto (`assets/images/rt28111-led-tail-light.png` e
`rt31046-big-brake-kit.png`) têm a ressalva escrita no rodapé, dentro da imagem. Até outubro
de 2026 elas ainda diziam "or officially affiliated with…" e foram refeitas com a redação
certa. Se forem regeneradas, a faixa do rodapé precisa sair com a mesma ressalva da página.

## Como fazer um case novo

Padrão fechado com o TM-003 e aplicado depois ao Fogo e à Crown. Para o próximo,
copie o `tm-003-casa-cavoquinho.html` e o `css/tm-003-case.css` como molde e
reescreva o conteúdo seção por seção. Nunca faça busca-e-troca global a partir de
outro case: sobra nome, alt, ID e link do case antigo.

**Ordem da página.** Capa (o nome da marca ou do lugar é o título grande; o código
`TM-00X` vai na linha pequena de cima, com o local) → **The Film** logo abaixo da capa
(ninguém deve precisar rolar oito seções para ver o trabalho) → 01 Challenge, com os
cards *Strategic focus / Project scope / Evidence standard* → Insight → Strategy →
Big Idea → Creative Direction → Research & Reality (fontes) → Production → Edit →
Outcome, com as entregas marcadas *Produced* ou *Documented* → bloco Transparency.

**Cores.** As da home, não as de cada case: fundo `#0a0a0b`, cards `#17171a`, linha
`#2a2a2e`, texto `#fff` e `#b7b7bc`. Vermelho `#e1262f` em títulos, botões e
destaques grandes; **texto vermelho pequeno (rótulos, números, links) usa `#ff4a52`**,
que passa de 4,5:1 no preto (o `#e1262f` fica em 3,9–4,3:1). O bege antigo do Fogo
saiu do site.

**Tom.** O da Crown: analítico e comedido ("could", "may"), frases simples, sem slogan
em destaque. Nenhum resultado comercial, aprovação do cliente ou afiliação afirmados.
A ressalva de independência aparece na capa, nos `meta` e no bloco final.

**Toda afirmação factual tem fonte nomeada e link**, numa seção *Research Sources* que
diz o que cada fonte sustenta e o que ela **não** prova. Fontes sobre a propriedade
ficam separadas das referências visuais de paisagem. Cada ressalva aparece uma vez por
papel (resumo na seção 01, detalhe junto das fontes, fechamento em Transparency), não
em toda seção.

**Descreva o filme pelo que ele mostra.** Antes de escrever "the film closes on…",
extraia os últimos frames e confira; antes de chamar um vídeo de "cinematic film",
veja o que ele contém. Já aconteceu duas vezes: TM-003 e Fogo diziam fechar com a
frase do conceito, que não aparece na tela; a Crown chamava de filme sobre a
comunidade Jeep um cartão de logo de 4 s. Nota interna do tipo "must be reviewed
before publication" não pode ficar numa página publicada: confira e cite a fonte.

**Proteções que todo case leva** (iguais às do `main`): `meta author` e `copyright`,
`og:site_name` e `og:locale`, favicon vetorial, `<video controlsList="nodownload"
disablePictureInPicture>`, nenhum link direto para o `.mp4`, e a linha de copyright
com `/terms.html` no rodapé.

**Imagens do case.** Frames do próprio filme: detecte os cortes
(`ffmpeg -vf "select='gt(scene,0.3)',showinfo"`) e tire um frame do meio de cada um,
720×1280, JPEG q82. Alt começa com "Film still:". Capa e Big Idea usam o primeiro e o
último plano como fundo.

**Filme.** Comprima a partir do master, nunca de uma versão já comprimida: 720×1280,
`crf 23`, `maxrate` 1800k se houver texto na imagem ou 1000k sem texto, `bufsize`
igual ao `maxrate`, `-movflags +faststart`. Confira o SSIM contra o master (≥ 0,97).
A marca vai junto, com os parâmetros do `watermark.sh` (120 px de largura em vídeo de
720, 140 px acima da borda, opacidade 0,55); poster com a mesma marca, e sem texto
queimado. **Legenda queimada na imagem não sai**: peça a versão limpa.

**Uploads pelo celular** (o Claude não grava em `assets/`, regra 4). O "Upload files"
do GitHub cai **na pasta aberta e no ramo selecionado**: confira os dois antes do
"Commit changes" e confira o resultado pelo hash depois. Já caiu na raiz, em
`assets/` em vez de `assets/images/`, e no ramo errado. Se o arquivo certo chegou com
outro nome ou outra pasta, ajuste a página em vez de pedir outro upload; cópia
duplicada se reverte com `git revert`.

**Publicação.** Trabalhe num ramo; traga o `main` antes de juntar; prévia privada
(Artifact no claude.ai com as páginas e os assets) para revisar pelo celular; merge
`--no-ff` no `main` só com "pode publicar" explícito. Depois: Post Inspector com o
endereço `timasmotion.com` de cada página que mudou.

**Divulgação.** Carrossel de 10 slides 1080×1350 + o mesmo em PDF para o LinkedIn,
gerado por `scripts/carousel-tm003.py` (molde: troque textos e imagens).
O do TM-002 (`scripts/carousel-tm002.py`) segue o mesmo molde com duas diferenças: o
case não tem página própria, então o último slide aponta para `timasmotion.com/#work`; e a
ressalva diz o que é sabido ("Reel created for a specialist Jeep workshop. AI-assisted
production."), sem nomear a oficina nem afirmar aprovação ou resultado. Os planos das
prateleiras com caixas de peças ficam fora porque mostram marca de fabricante. No Instagram
link não é clicável na legenda: use a bio e o story com figurinha de link.

## E-mail do domínio (`hello@timasmotion.com`)

O domínio está registrado na **Porkbun**, que também cuida do DNS. Desde 22/10/2026 o
`hello@` é uma **caixa hospedada na Porkbun** (Email Hosting: 10 GB, US$ 36 por ano, renovação
automática, vence em 23/10/2027). Ela substituiu o arranjo de outubro de 2026, um
encaminhamento para o Gmail pessoal com o `hello@` como alias "Send mail as" do Gmail. Esse
caminho saía sem assinatura do domínio: o Outlook mostrava "Unverified Sender", e o "Show
original" dava `spf=pass` para `gmail.com` e `dmarc=fail`. O alias foi apagado do Gmail no mesmo dia.

**Onde ler e escrever.** No app do Gmail do iPhone, conta **Timas Motion** (IMAP), separada da
pessoal. Escreva para clientes por ela. Servidores: `imap.porkbun.com` porta 993 SSL/TLS;
`smtp.porkbun.com` porta 587 STARTTLS (se o app reclamar do envio, 465 SSL/TLS); usuário é o
endereço completo. A senha da caixa fica no app Senhas, no item **mail.porkbun.com**, separado
do item **porkbun.com** da conta: criar a senha no próprio formulário da Porkbun faria o iPhone
gravá-la por cima da senha da conta. Para redefinir: Porkbun → coluna EMAIL → Current Accounts
→ **password**. O Gmail de computador não busca mais caixas de fora (fim do POP, jan/2026); os
apps sim. Os botões de webmail da Porkbun abrem uma janela que o Safari bloqueia.

**Encaminhamento e caixa não convivem no mesmo endereço**: a Porkbun recusa criar a caixa
enquanto existir o forward. A troca foi apagar o forward e criar a caixa logo em seguida.

Para testar o recebimento, mande de **outro** endereço: o Gmail esconde a cópia de uma
mensagem que saiu dele mesmo, e o teste parece falhar sem ter falhado.

**DNS do e-mail na Porkbun** (não apague os outros registros):

| Tipo | Host | Valor |
|---|---|---|
| MX | (raiz) | `fwd1.porkbun.com` (10) e `fwd2.porkbun.com` (20): servem também à caixa hospedada |
| TXT | (raiz) | `v=spf1 include:_spf.porkbun.com include:_spf.google.com ~all` |
| TXT | `default._domainkey` | DKIM, criado pela Porkbun |
| TXT | `_dmarc` | `v=DMARC1; ...` |

O DKIM não nasce com a caixa: sai do botão **Configure DMARC**, no quadro "DMARC Notice" da
página de e-mail do domínio, e leva até 10 minutos. O mesmo quadro tem **Delete DMARC** e
**Reset DMARC**: não use.

O SPF é **um registro só**: para autorizar outro serviço, edite este e acrescente o `include`,
nunca crie um segundo `v=spf1` (dois SPF invalidam os dois). O `include:_spf.porkbun.com`
sustenta a caixa e não pode sair. Os dois `_acme-challenge` são do certificado HTTPS.

**Verificado em 22/10/2026** com o mail-tester.com: SPF, DKIM (`DKIM_VALID_AU`, assinado por
`timasmotion.com`) e DMARC passaram. A nota foi 6,1/10 por dois motivos fora da configuração:
corpo de teste vazio (`EMPTY_MESSAGE`) e domínio com menos de 14 dias (`FROM_FMBLA_NEWDOM14`),
que some com o tempo.

**DMARC.** Agora todo envio como `@timasmotion.com` sai assinado, então endurecer para
`p=quarantine` passou a ser possível. Só faça depois de confirmar que nenhum outro serviço
envia em nome do domínio: o que não sair pela Porkbun iria para o spam.

**Pendências do e-mail:**
- Conferir no DNS o valor do `_dmarc` depois do Configure DMARC (era `p=none`; o botão pode
  ter mudado) e se há um registro `_dmarc` só.
- Tirar o `include:_spf.google.com` do SPF: ele só existia por causa do alias do Gmail.
- Apagar a senha de app do Google criada para o alias (myaccount.google.com/apppasswords).

**Conta da Porkbun.** Ela controla o domínio, o site e o e-mail. A verificação em duas
etapas por app está ativa desde 21/10/2026, com o código no app Senhas do iPhone. Os códigos
de backup foram gerados de novo no mesmo dia e os anteriores deixaram de valer; sem o
celular, é com um deles que se entra. Nunca mande print da tela do QR code nem dos códigos:
quem tem a chave gera os códigos.

A senha também foi trocada em 21/10/2026 por uma senha forte gerada pelo iPhone, salva no
app Senhas: a anterior era reutilizada em outro site.

## Pendências conhecidas

- O Instagram já foi renomeado para `@timasmotion` e o site aponta para
  `https://instagram.com/timasmotion`. O YouTube usa o endereço estável do canal
  `https://www.youtube.com/channel/UCWr4GlFo173CoBw1g8Jk_IA`, que não depende do nome
  de exibição.
- O QR code do bloco de contato é um PNG em base64 embutido no `index.html` e codifica
  `https://www.instagram.com/timasmotion`. Se o handle mudar de novo, trocar os links não
  basta — o QR precisa ser regerado (versão 4, correção Q, módulo de 10px, borda de 4
  módulos, preto `#0a0a0b`, 410x410), senão ele continua levando para o endereço antigo
  sem que nada no HTML denuncie.

## Ambiente

- Em sessão remota do Claude Code, `fonts.googleapis.com` e o domínio do site são
  bloqueados pela política de rede do ambiente. O `ERR_CONNECTION_RESET` no `shots.sh`
  é isso, não um bug do site — e não dá para buscar a página publicada. Em compensação,
  como o site é estático, `git show origin/main:arquivo` mostra exatamente o que o Pages
  está servindo.
- O Chromium do Playwright não tem codec H.264, então **os `.mp4` não tocam nos
  screenshots do `shots.sh` em sessão remota** — aparecem os posters `.jpg`. No seu
  navegador tocam normalmente. Não confunda isso com vídeo quebrado.
- `scripts/shots.sh` precisa de `pip install playwright && playwright install chromium`.
