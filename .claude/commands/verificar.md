---
description: Roda a verificação pré-publicação e explica cada achado
allowed-tools: Bash(bash scripts/check.sh), Bash(bash scripts/shots.sh), Read, Grep, Glob
---

Rode `bash scripts/check.sh`.

Depois, para cada ERRO e cada AVISO:
1. Abra o arquivo citado e confirme o achado (o script pode dar falso positivo).
2. Diga em uma linha o que quebra na prática para um visitante do site.
3. Proponha a correção mínima — não reescreva o arquivo inteiro.

Termine com um veredito único: **pode publicar** ou **não pode publicar, porque X**.
Não corrija nada sem me perguntar antes.
