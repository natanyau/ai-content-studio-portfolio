# Timas Motion — guia do projeto

Portfólio estático da Timas Motion, publicado pelo **GitHub Pages** em
`https://natanyau.github.io/ai-content-studio-portfolio/`.
Sem build, sem framework, sem dependências: o que está no repositório é exatamente
o que vai ao ar quando o `main` recebe um push.

## Estrutura

| Caminho | O que é |
|---|---|
| `index.html` | Site principal. CSS e JS **inline por opção** (arquivo único, zero requisições extras). |
| `crown-featured-case.html` | Case Crown. Único arquivo que usa CSS externo (`css/crown-case.css`). |
| `404.html` | Página de erro servida pelo Pages. |
| `assets/media/` | Vídeos `.mp4` + posters `.jpg` de cada seção. Cada vídeo **precisa** do `.jpg` de mesmo nome como fallback. |
| `preview.jpg` | Imagem de preview de link (Open Graph), 1200×630. |
| `scripts/check.sh` | Verificação pré-publicação. |
| `scripts/shots.sh` | Screenshots em mobile/tablet/desktop. |
| `scripts/watermark.sh` | Aplica a marca d'água nos vídeos e regenera os posters. |
| `docs/archive/` | Deck antigo, fora da raiz publicada e marcado `noindex`. Não é mantido. |

## Regras que evitam quebrar o site

1. **Não converta o CSS/JS inline do `index.html` em arquivos separados.** É decisão de
   arquitetura, não descuido. O mesmo vale para não "modernizar" para React/Vite/Tailwind.
2. **Links internos de navegação usam o caminho absoluto do Pages**
   (`/ai-content-studio-portfolio/`), porque o site vive num subdiretório. Já os assets
   usam caminho relativo (`assets/media/...`). Não unifique os dois — cada um está certo
   no seu contexto.
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
   E saiba que **o `robots.txt` deste repositório não está em vigor**: ele só valeria
   na raiz do domínio (`natanyau.github.io/robots.txt`), que seria servida por um
   repositório `natanyau.github.io` — inexistente. Num *project site* do Pages o
   arquivo fica em subdiretório e nenhum crawler o lê. O próprio arquivo explica isso
   no topo. Não escreva em lugar nenhum que ele bloqueia alguém; hoje não bloqueia.
   Quem sustenta a reserva de direitos é o `terms.html`, que não depende dele.

## Antes de publicar (sempre nesta ordem)

```bash
bash scripts/check.sh     # 0 erros = pode publicar
bash scripts/shots.sh     # olhe .preview/*__mobile.png de verdade
python3 -m http.server 8000   # e abra http://localhost:8000
```

O `check.sh` valida: referências quebradas, tags desbalanceadas, DOCTYPE/meta ausentes,
`img` sem `alt`, sitemap desatualizado, assets órfãos ou pesados, e segredos commitados.
O `shots.sh` acusa scroll horizontal, quirks mode e erros de JS por viewport.

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

O LinkedIn guarda o preview em cache por URL e não relê sozinho. Depois de mudar
qualquer `og:`, force a releitura no `linkedin.com/post-inspector/` — sem isso o
card antigo continua aparecendo por dias.

A descrição do case precisa manter a ressalva sobre a Crown Automotive, igual à que
a página exibe (aparece em três `meta`, na nota do herói e na do rodapé — os cinco
textos andam juntos). Não a remova para encurtar o texto.

O que a ressalva afirma é deliberado: **não encomendado, revisado ou endossado**. Ela
não diz "não afiliado" porque o autor do case trabalha na Crown Automotive Sales, e
negar vínculo seria falso. Se alguém "restaurar" a redação antiga em nome da
concisão, volta a ser uma afirmação incorreta na página publicada.

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

- Em sessão remota do Claude Code, `fonts.googleapis.com` e `natanyau.github.io` são
  bloqueados pela política de rede do ambiente. O `ERR_CONNECTION_RESET` no `shots.sh`
  é isso, não um bug do site — e não dá para buscar a página publicada. Em compensação,
  como o site é estático, `git show origin/main:arquivo` mostra exatamente o que o Pages
  está servindo.
- O Chromium do Playwright não tem codec H.264, então **os `.mp4` não tocam nos
  screenshots do `shots.sh` em sessão remota** — aparecem os posters `.jpg`. No seu
  navegador tocam normalmente. Não confunda isso com vídeo quebrado.
- `scripts/shots.sh` precisa de `pip install playwright && playwright install chromium`.
