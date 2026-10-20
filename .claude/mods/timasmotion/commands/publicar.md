---
description: Publica com segurança — verifica, mostra o diff, commita e envia
allowed-tools: Bash(bash scripts/check.sh), Bash(bash scripts/shots.sh), Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Read
---

Publique as mudanças pendentes, nesta ordem, parando no primeiro problema:

1. `git status` e `git diff` — me mostre em português o que mudou e o efeito visível de cada mudança.
2. `bash scripts/check.sh` — se houver qualquer ERRO, **pare** e me diga qual.
3. Se algum `.html` ou `.css` mudou, rode `bash scripts/shots.sh` e reporte qualquer aviso
   de scroll horizontal, quirks mode ou erro de JS.
4. Me pergunte a confirmação, mostrando a mensagem de commit que pretende usar
   (uma linha, no imperativo, descrevendo o efeito e não o arquivo).
5. Só depois: `git add`, `git commit`, `git push -u origin <branch atual>`.

Nunca use `--force`, nunca use `git reset --hard`, nunca commite `.preview/`.
