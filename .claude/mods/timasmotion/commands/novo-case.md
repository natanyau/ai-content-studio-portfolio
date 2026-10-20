---
description: Monta um case novo no padrão do TM-003, do filme à prévia, e para antes de publicar
argument-hint: <código e nome, ex.: TM-004 Nome da Marca>
---

Case novo: **$ARGUMENTS**. O padrão está em `CLAUDE.md`, seção "Como fazer um case novo".
Releia essa seção antes de começar e siga a ordem abaixo. Pare e me pergunte em cada ponto
marcado com **[pare]**.

1. **Material.** Confira o que existe e me diga o que falta antes de escrever qualquer texto:
   - o master do filme (não uma versão já comprimida);
   - a relação com a marca: independente, feito para um cliente ou outra coisa;
   - se as cenas foram geradas com IA;
   - as fontes públicas sobre o lugar ou a marca.
   Não suponha nenhum desses pontos. **[pare]** se faltar algum.
2. **Ramo.** `git fetch origin main` e crie um ramo `tm-00X-<nome>` a partir de `origin/main`.
3. **Filme.**
   - Assista pelo que ele mostra: detecte os cortes, tire um frame do meio de cada um e
     confira o primeiro e o último plano.
   - Se houver legenda queimada, **[pare]** e peça a versão limpa.
   - Prepare o vídeo comprimido, a marca d'água, o poster e os stills no scratchpad, com os
     parâmetros do `CLAUDE.md`.
   - Eu não gravo em `assets/` (regra 4). Me diga o nome e a pasta exata de cada arquivo
     para o upload pelo GitHub, e depois confira o que chegou pelo hash.
4. **Página.** Copie `tm-003-casa-cavoquinho.html` e `css/tm-003-case.css` e reescreva
   seção por seção.
   - Nunca use busca-e-troca global: sobra nome, alt, ID e link do case antigo.
   - Escreva na voz de `.claude/mods/timasmotion/skills/timas-motion-workflow/references/perfil-de-voz.md`.
   - Toda afirmação factual leva fonte nomeada e link, com o que a fonte não prova.
   - Nenhum resultado comercial, aprovação do cliente ou afiliação afirmados.
   - A ressalva só diz o que é verdade para este case. Se negar afiliação for falso, não negue
     (veja o caso da Crown no `CLAUDE.md`).
5. **Site.**
   - Entrada no `sitemap.xml`.
   - Card na home só se eu pedir.
   - `og:image` 1200×630 preparado no scratchpad, para eu subir.
6. **Verificação.**
   - Rode `bash scripts/check.sh` e corrija até zerar os erros.
   - Rode `bash scripts/shots.sh` e olhe os PNGs de mobile.
   - Procure na página nova restos de outro case (nomes, IDs, links).
7. **Prévia.** Publique um Artifact privado com a página e os assets, para eu revisar pelo
   celular. Commite e faça push no ramo.
8. **[pare]** Junte ao `main` (`--no-ff`, depois de trazer o `main`) só quando eu disser
   "pode publicar". Depois confira as execuções `check` e `pages build` no GitHub e me
   lembre do Post Inspector com o endereço `timasmotion.com` da página.
