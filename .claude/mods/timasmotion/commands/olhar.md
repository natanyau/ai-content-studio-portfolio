---
description: Renderiza o site em mobile/tablet/desktop e me mostra o que está errado
allowed-tools: Bash(bash scripts/shots.sh), Read, Glob
---

Rode `bash scripts/shots.sh` $ARGUMENTS e depois **abra os PNGs de `.preview/` com a ferramenta Read**
— principalmente os `__mobile.png`.

Para cada viewport, me diga o que você realmente vê: texto sobreposto, elemento cortado,
contraste ruim, botão fora da tela, imagem esticada. Descreva o problema e onde ele está.

No fim da saída vem a auditoria de acessibilidade (axe-core). Para cada regra violada,
diga qual é o elemento (pelo trecho de HTML), em que tela falha e qual seria a correção;
os detalhes estão em `.preview/axe__<pagina>.json`. Os itens "a conferir à mão" só
merecem menção quando o screenshot mostrar um problema de verdade.

Se eu tiver acabado de mudar alguma coisa, compare com o estado anterior
(`git stash` não — use `git show HEAD:arquivo.html > /tmp/antes.html` e rode o shots nos dois).
