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
regra 4 vale aqui também. Vídeo acima de 5MB ganha teto de bitrate no reencode, já
que vai ser recomprimido de qualquer jeito.

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

A descrição do case precisa manter a ressalva de não-afiliação com a Crown
Automotive, igual à que a página exibe. Não a remova para encurtar o texto.

## Pendências conhecidas

- Os nomes exibidos no site foram atualizados. O Instagram ainda usa o endereço
  `https://instagram.com/aicontentstudious`; o YouTube usa o endereço estável do canal
  `https://www.youtube.com/channel/UCWr4GlFo173CoBw1g8Jk_IA`.
  A renomeação das contas para `@timasmotion` continua pendente nas plataformas.
  Só atualize os destinos e o QR code depois de confirmar que as novas URLs funcionam.

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
