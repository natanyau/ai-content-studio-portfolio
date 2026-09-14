#!/usr/bin/env bash
# Troca o slug do GitHub Pages e/ou os handles sociais em todo o site, de uma vez.
#
# Por que existe: o slug (/ai-content-studio-portfolio/) vem do NOME DO REPOSITÓRIO.
# Renomear o repositório sem trocar o markup quebra todo link interno, e trocar o
# markup sem renomear o repositório quebra igual. As duas coisas têm que andar
# juntas — este script é a metade que cabe ao repositório, para rodar colada ao
# rename no GitHub.
#
# Uso:
#   bash scripts/rebrand-urls.sh --slug timas-motion-portfolio
#   bash scripts/rebrand-urls.sh --instagram timasmotion --youtube TimasMotion
#   bash scripts/rebrand-urls.sh --slug timas-motion-portfolio \
#                                --instagram timasmotion --youtube TimasMotion
#
#   --dry-run   mostra o que mudaria, sem escrever nada
#
# Depois de rodar: bash scripts/check.sh  (tem que dar 0 erros)

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

SLUG_OLD="ai-content-studio-portfolio"
IG_OLD="aicontentstudious"
YT_OLD="AIContentStudioUS"

SLUG_NEW=""
IG_NEW=""
YT_NEW=""
DRY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --slug)      SLUG_NEW="${2:-}"; shift 2 ;;
    --instagram) IG_NEW="${2:-}";   shift 2 ;;
    --youtube)   YT_NEW="${2:-}";   shift 2 ;;
    --dry-run)   DRY=1; shift ;;
    -h|--help)   sed -n '2,20p' "$0"; exit 0 ;;
    *) printf 'Argumento desconhecido: %s\n' "$1" >&2; exit 2 ;;
  esac
done

if [ -z "$SLUG_NEW" ] && [ -z "$IG_NEW" ] && [ -z "$YT_NEW" ]; then
  printf 'Nada a fazer. Informe --slug, --instagram e/ou --youtube.\n' >&2
  printf 'Veja: bash scripts/rebrand-urls.sh --help\n' >&2
  exit 2
fi

# Um slug de repositório do GitHub só aceita estes caracteres. Barra ou espaço
# aqui viraria um caminho quebrado em toda página, então falha antes de escrever.
if [ -n "$SLUG_NEW" ] && ! printf '%s' "$SLUG_NEW" | grep -qE '^[A-Za-z0-9._-]+$'; then
  printf 'Slug inválido: "%s" (use apenas letras, números, ponto, hífen ou _)\n' "$SLUG_NEW" >&2
  exit 2
fi

# Arquivos que carregam o slug. O CLAUDE.md entra porque documenta a URL de
# produção — deixá-lo para trás faz a próxima sessão trabalhar com o dado errado.
SLUG_FILES="index.html crown-featured-case.html 404.html sitemap.xml robots.txt scripts/check.sh CLAUDE.md"
# Os handles só aparecem na home (links, textos e o alt do QR code).
SOCIAL_FILES="index.html"

apply() { # arquivos, de, para, rótulo
  local files="$1" from="$2" to="$3" label="$4" total=0 n
  for f in $files; do
    [ -f "$f" ] || continue
    n=$(grep -oF "$from" "$f" 2>/dev/null | wc -l | tr -d ' ')
    [ "$n" -eq 0 ] && continue
    total=$((total + n))
    printf '  %-26s %s ocorrência(s)\n' "$f" "$n"
    [ "$DRY" -eq 0 ] && sed -i "s|$from|$to|g" "$f"
  done
  printf '  → %s: %s no total\n\n' "$label" "$total"
}

[ "$DRY" -eq 1 ] && printf '\n*** DRY-RUN — nada será escrito ***\n'
printf '\n'

if [ -n "$SLUG_NEW" ]; then
  printf 'Slug: %s → %s\n' "$SLUG_OLD" "$SLUG_NEW"
  apply "$SLUG_FILES" "$SLUG_OLD" "$SLUG_NEW" "slug"
fi

if [ -n "$IG_NEW" ]; then
  printf 'Instagram: @%s → @%s\n' "$IG_OLD" "$IG_NEW"
  apply "$SOCIAL_FILES" "$IG_OLD" "$IG_NEW" "instagram"
fi

if [ -n "$YT_NEW" ]; then
  printf 'YouTube: @%s → @%s\n' "$YT_OLD" "$YT_NEW"
  apply "$SOCIAL_FILES" "$YT_OLD" "$YT_NEW" "youtube"
fi

if [ -n "$IG_NEW" ]; then
  printf '\033[33mATENÇÃO\033[0m  O QR code da seção de contato é uma imagem embutida\n'
  printf '         (base64) que aponta para instagram.com/%s. O texto ao lado dele\n' "$IG_OLD"
  printf '         foi atualizado, mas a imagem NÃO — ela precisa ser regerada com\n'
  printf '         o handle novo, senão o QR leva ao perfil antigo.\n\n'
fi

if [ "$DRY" -eq 1 ]; then
  printf 'Dry-run: nenhum arquivo alterado.\n'
  exit 0
fi

printf 'Pronto. Agora, nesta ordem:\n'
[ -n "$SLUG_NEW" ] && printf '  1. Renomeie o repositório no GitHub para "%s" (Settings → Repository name)\n' "$SLUG_NEW"
printf '  2. bash scripts/check.sh     # tem que dar 0 erros\n'
printf '  3. commit + push para o main\n'
