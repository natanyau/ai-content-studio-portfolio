#!/usr/bin/env bash
# Verificação pré-publicação do AI Content Studio.
# Site estático servido pelo GitHub Pages em /ai-content-studio-portfolio/.
# Uso: bash scripts/check.sh   (código 0 = pode publicar, 1 = erro bloqueante)

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

BASE="/ai-content-studio-portfolio"
ERRORS=0
WARNS=0

err()  { printf '  \033[31mERRO\033[0m   %s\n' "$1"; ERRORS=$((ERRORS+1)); }
warn() { printf '  \033[33mAVISO\033[0m  %s\n' "$1"; WARNS=$((WARNS+1)); }
ok()   { printf '  \033[32mok\033[0m     %s\n' "$1"; }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

pages_html() { find . -maxdepth 1 -name '*.html' -printf '%f\n' | sort; }

# 1 ─ Referências locais quebradas -------------------------------------------
head_ "1. Referências locais (href/src)"
broken=0
for f in $(pages_html) css/*.css; do
  [ -e "$f" ] || continue
  grep -ohE '(src|href)="[^"]*"' "$f" \
    | sed -E 's/.*="([^"]*)".*/\1/' \
    | grep -vE '^(https?:|mailto:|tel:|data:|#|//)' \
    | sort -u \
    | while read -r ref; do
        p="${ref%%[?#]*}"
        [ -z "$p" ] && continue
        case "$p" in
          "$BASE"/) p="index.html" ;;
          "$BASE"/*) p="${p#$BASE/}" ;;
          /*) p=".$p" ;;
        esac
        [ -e "$p" ] || echo "$f -> $ref"
      done
done > /tmp/_broken_refs 2>/dev/null
if [ -s /tmp/_broken_refs ]; then
  while read -r line; do err "referência inexistente: $line"; done < /tmp/_broken_refs
  broken=1
fi
[ "$broken" -eq 0 ] && ok "todas as referências locais resolvem"
rm -f /tmp/_broken_refs

# 2 ─ Tags estruturais balanceadas -------------------------------------------
head_ "2. Estrutura do HTML"
for f in $(pages_html); do
  for tag in style script section nav footer main head body html; do
    open=$(grep -o "<$tag[ >]" "$f" | wc -l)
    close=$(grep -o "</$tag>" "$f" | wc -l)
    [ "$open" -ne "$close" ] && err "$f: <$tag> aberto ${open}x, fechado ${close}x"
  done
done
[ "$ERRORS" -eq 0 ] && ok "tags estruturais balanceadas em todas as páginas"

# 3 ─ Metadados obrigatórios --------------------------------------------------
head_ "3. Metadados (SEO / preview de link)"
for f in $(pages_html); do
  head -1 "$f" | grep -qi '<!doctype html>' || err  "$f: sem <!DOCTYPE html> na 1a linha (risco de quirks mode)"
  grep -q '<title>'                  "$f" || err  "$f: sem <title>"
  grep -q 'name="description"'       "$f" || warn "$f: sem meta description"
  grep -q 'rel="canonical"'          "$f" || warn "$f: sem <link rel=canonical>"
  grep -q 'property="og:image"'      "$f" || warn "$f: sem og:image (preview quebra no LinkedIn/WhatsApp)"
  grep -q '<html[^>]*lang='          "$f" || warn "$f: <html> sem atributo lang"
done
[ "$WARNS" -eq 0 ] && [ "$ERRORS" -eq 0 ] && ok "metadados completos"

# 4 ─ Imagens sem alt ---------------------------------------------------------
head_ "4. Acessibilidade"
noalt=$(grep -ohE '<img [^>]*>' $(pages_html) 2>/dev/null | grep -vc 'alt=' || true)
[ "${noalt:-0}" -gt 0 ] && warn "$noalt <img> sem alt=" || ok "todas as <img> têm alt"

# 5 ─ Sitemap sincronizado ----------------------------------------------------
head_ "5. sitemap.xml"
if [ -f sitemap.xml ]; then
  for f in $(pages_html); do
    case "$f" in 404.html|*backup*|*.bak.html) continue ;; esac
    loc="$f"; [ "$f" = "index.html" ] && loc=""
    grep -q "$BASE/$loc<" sitemap.xml || warn "sitemap.xml não lista $f"
  done
  ok "sitemap.xml presente"
else
  warn "sitemap.xml ausente"
fi

# 6 ─ Arquivos que não deviam estar públicos ----------------------------------
head_ "6. Higiene do diretório publicado"
for f in $(pages_html); do
  case "$f" in
    *backup*|*.bak.html|*copy*|*old*|*rascunho*|*test*)
      warn "$f é servido publicamente em $BASE/$f — mover para docs/archive/ ou apagar" ;;
  esac
done

# 7 ─ Assets órfãos e peso ----------------------------------------------------
head_ "7. Assets"
find assets -type f 2>/dev/null | while read -r a; do
  grep -qF "$(basename "$a")" $(pages_html) css/*.css 2>/dev/null || echo "$a"
done > /tmp/_orphans
if [ -s /tmp/_orphans ]; then
  while read -r a; do warn "asset não referenciado: $a"; done < /tmp/_orphans
else
  ok "nenhum asset órfão"
fi
rm -f /tmp/_orphans
big=$(find assets -type f -size +5M 2>/dev/null | wc -l)
[ "$big" -gt 0 ] && warn "$big asset(s) acima de 5MB — pesa no carregamento mobile"
tot=$(du -sm assets 2>/dev/null | cut -f1)
[ "${tot:-0}" -gt 90 ] && warn "assets/ com ${tot}MB (limite prático do GitHub Pages: 1GB, recomendado <100MB)"

# 8 ─ Segredos ----------------------------------------------------------------
head_ "8. Segredos"
if grep -rInE '(api[_-]?key|secret|token|password)[[:space:]]*[:=][[:space:]]*["'\''][A-Za-z0-9_\-]{16,}' \
     --include='*.html' --include='*.css' --include='*.js' . 2>/dev/null | grep -v '^./scripts/'; then
  err "possível segredo commitado (revise as linhas acima)"
else
  ok "nenhum segredo aparente"
fi

# Resultado -------------------------------------------------------------------
printf '\n────────────────────────────────────────\n'
if [ "$ERRORS" -gt 0 ]; then
  printf '\033[31m%d erro(s)\033[0m e %d aviso(s). NÃO publique antes de corrigir os erros.\n' "$ERRORS" "$WARNS"
  exit 1
fi
printf '\033[32mSem erros bloqueantes\033[0m (%d aviso(s)). Pode publicar.\n' "$WARNS"
exit 0
