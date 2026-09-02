# AI Content Studio — guia do projeto

Portfólio estático da AI Content Studio, publicado pelo **GitHub Pages** em
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
| `index.deck-backup-*.html` | Deck antigo. **Está sendo servido publicamente** — ver "Pendências". |

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
   fica preta em quem tem autoplay bloqueado.
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

## Pendências conhecidas

- `index.deck-backup-2026-08-29.html` (52KB) é servido publicamente e indexável.
  Decida: apagar, ou mover para `docs/archive/` (fora do que o Pages publica).
- `crown-featured-case.html` e `404.html` estão sem `description` e `og:image`:
  o link do case compartilhado sai sem preview.
- Nenhuma página tem `<link rel="canonical">`.

## Ambiente

- Em sessão remota do Claude Code, `fonts.googleapis.com` é bloqueado pelo proxy —
  o `ERR_CONNECTION_RESET` que aparece no `shots.sh` é isso, não um bug do site.
- `scripts/shots.sh` precisa de `pip install playwright && playwright install chromium`.
