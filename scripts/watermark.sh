#!/usr/bin/env bash
# Aplica a marca d'agua nos videos do portfolio e regenera os posters .jpg.
# Uso: bash scripts/watermark.sh [arquivo.mp4 ...]   (padrao: todos os .mp4 de assets/)
# Requer: ffmpeg  (macOS: brew install ffmpeg)
#
# NAO substitui nada em assets/. Escreve tudo em .watermark/out/ para voce
# conferir primeiro — a troca dos binarios de producao e manual, por regra do
# projeto. O script imprime os comandos de copia no fim.
#
# A marca deve ser um PNG com fundo transparente em .watermark/mark.png
# (ou aponte outro caminho com MARK=/caminho/para/marca.png).

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

MARK="${MARK:-.watermark/mark.png}"
OUTDIR=".watermark/out"

# Ajustes da marca -----------------------------------------------------------
OPACITY="${OPACITY:-0.55}"   # 0 = invisivel, 1 = solida
MARGIN="${MARGIN:-140}"      # pixels acima da borda inferior
WIDTH_1080="${WIDTH_1080:-190}"   # largura da marca em video 1080 de largura
WIDTH_720="${WIDTH_720:-120}"     # largura da marca em video 720 de largura
POSTER_AT="${POSTER_AT:-1}"       # segundo de onde sai o poster

ERRORS=0
err()   { printf '  \033[31mERRO\033[0m   %s\n' "$1"; ERRORS=$((ERRORS+1)); }
warn()  { printf '  \033[33mAVISO\033[0m  %s\n' "$1"; }
ok()    { printf '  \033[32mok\033[0m     %s\n' "$1"; }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# 1 ─ Pre-requisitos ----------------------------------------------------------
head_ "1. Pre-requisitos"
if ! command -v ffmpeg >/dev/null 2>&1; then
  err "ffmpeg nao encontrado. Instale com:  brew install ffmpeg"
  exit 1
fi
ok "ffmpeg $(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f3)"

if [ ! -f "$MARK" ]; then
  err "marca nao encontrada em $MARK"
  printf '         Crie um PNG com fundo transparente ali (o \"T\" no circulo +\n'
  printf '         \"Timas Motion\"), uns 400px de largura. Ou aponte outro caminho:\n'
  printf '         MARK=~/Desktop/marca.png bash scripts/watermark.sh\n'
  exit 1
fi
ok "marca: $MARK"

# 2 ─ Arquivos a processar ----------------------------------------------------
head_ "2. Arquivos"
FILES=("$@")
if [ ${#FILES[@]} -eq 0 ]; then
  while IFS= read -r line; do FILES+=("$line"); done < <(find assets -name '*.mp4' | sort)
fi
[ ${#FILES[@]} -eq 0 ] && { err "nenhum .mp4 encontrado"; exit 1; }
ok "${#FILES[@]} video(s) na fila"

mkdir -p "$OUTDIR"

# 3 ─ Processamento -----------------------------------------------------------
head_ "3. Processamento"
for src in "${FILES[@]}"; do
  [ -f "$src" ] || { err "nao existe: $src"; continue; }

  base=$(basename "$src" .mp4)
  out="$OUTDIR/$base.mp4"
  poster="$OUTDIR/$base.jpg"

  vw=$(ffprobe -v error -select_streams v:0 -show_entries stream=width \
        -of csv=p=0 "$src" 2>/dev/null)
  [ -z "$vw" ] && { err "$src: nao consegui ler a largura"; continue; }

  if [ "$vw" -ge 1000 ]; then mw="$WIDTH_1080"; else mw="$WIDTH_720"; fi

  # Video grande ganha teto de bitrate: e o momento de aliviar o mobile,
  # ja que o arquivo vai ser reencodado de qualquer jeito.
  bytes=$(wc -c < "$src" | tr -d ' ')
  if [ "$bytes" -gt 5242880 ]; then
    rate=(-crf 23 -maxrate 2200k -bufsize 4400k); mode="crf23 + teto 2200k"
  else
    rate=(-crf 20); mode="crf20"
  fi

  # Sem trilha de audio, nao passe flags de audio.
  if ffprobe -v error -select_streams a:0 -show_entries stream=codec_type \
       -of csv=p=0 "$src" 2>/dev/null | grep -q audio; then
    audio=(-c:a aac -b:a 128k)
  else
    audio=(-an)
  fi

  printf '  %-32s largura %s  marca %spx  %s\n' "$base" "$vw" "$mw" "$mode"

  if ! ffmpeg -y -loglevel error -i "$src" -i "$MARK" \
      -filter_complex "[1:v]scale=${mw}:-1,format=rgba,colorchannelmixer=aa=${OPACITY}[wm];[0:v][wm]overlay=(W-w)/2:H-h-${MARGIN}" \
      -c:v libx264 "${rate[@]}" -preset slow -pix_fmt yuv420p \
      "${audio[@]}" -movflags +faststart "$out" 2>&1; then
    err "$base: ffmpeg falhou ao aplicar a marca"; continue
  fi

  # Poster a partir do video JA marcado: e o que aparece com autoplay bloqueado.
  if ! ffmpeg -y -loglevel error -ss "$POSTER_AT" -i "$out" \
      -frames:v 1 -q:v 3 "$poster" 2>&1; then
    err "$base: ffmpeg falhou ao gerar o poster"; continue
  fi

  a=$(wc -c < "$src" | tr -d ' '); b=$(wc -c < "$out" | tr -d ' ')
  ok "$(printf '%s  %.1fM -> %.1fM  (poster %s)' \
        "$base" "$(echo "$a/1048576" | bc -l)" "$(echo "$b/1048576" | bc -l)" \
        "$(basename "$poster")")"
done

# 4 ─ Resultado ---------------------------------------------------------------
head_ "4. Resultado"
if [ "$ERRORS" -gt 0 ]; then
  printf '\n\033[31m%d erro(s).\033[0m Nada foi copiado para assets/.\n' "$ERRORS"
  exit 1
fi

printf '  Os arquivos marcados estao em %s/\n\n' "$OUTDIR"
printf '  \033[1mOlhe os videos e os posters antes de trocar qualquer coisa.\033[0m\n'
printf '  Guarde os masters limpos fora do repositorio: depois da troca, o\n'
printf '  arquivo original some do projeto.\n\n'
printf '  Quando aprovar, copie por cima (o caminho de destino de cada um):\n\n'
for src in "${FILES[@]}"; do
  [ -f "$src" ] || continue
  base=$(basename "$src" .mp4)
  [ -f "$OUTDIR/$base.mp4" ] || continue
  printf '    cp %s/%s.mp4 %s\n' "$OUTDIR" "$base" "$src"
  printf '    cp %s/%s.jpg %s\n' "$OUTDIR" "$base" "${src%.mp4}.jpg"
done
printf '\n  Depois:  bash scripts/check.sh && bash scripts/shots.sh\n'
exit 0
