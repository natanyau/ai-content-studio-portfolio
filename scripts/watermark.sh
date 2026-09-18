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
#
# O poster de cada video sai do HTML (data-poster / poster), nao do nome do
# arquivo: nem todo video tem poster de mesmo nome. Um poster que o site
# tambem usa como imagem comum e PULADO — marca-lo colocaria a marca em fotos
# de galeria. O script avisa quais, para voce decidir a mao.
#
# A marca e aplicada SOBRE o poster que ja existe, nunca sobre um frame novo
# extraido do video: o poster e um frame escolhido, e troca-lo mudaria a
# imagem que a pagina mostra.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

MARK="${MARK:-.watermark/mark.png}"
OUTDIR=".watermark/out"

# Ajustes da marca -----------------------------------------------------------
OPACITY="${OPACITY:-0.55}"        # 0 = invisivel, 1 = solida
MARGIN="${MARGIN:-140}"           # pixels acima da borda inferior
WIDTH_1080="${WIDTH_1080:-190}"   # largura da marca em video de 1080 de largura
WIDTH_720="${WIDTH_720:-120}"     # largura da marca em video de 720 de largura
CRF="${CRF:-23}"                  # qualidade do reencode (menor = melhor)
BITRATE_CAP="${BITRATE_CAP:-2500}"   # teto absoluto em kbps

ERRORS=0; SKIPPED=0
err()   { printf '  \033[31mERRO\033[0m   %s\n' "$1"; ERRORS=$((ERRORS+1)); }
warn()  { printf '  \033[33mAVISO\033[0m  %s\n' "$1"; }
ok()    { printf '  \033[32mok\033[0m     %s\n' "$1"; }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# 1 ─ Pre-requisitos ----------------------------------------------------------
head_ "1. Pre-requisitos"
command -v ffmpeg  >/dev/null 2>&1 || { err "ffmpeg nao encontrado. Instale:  brew install ffmpeg"; exit 1; }
command -v ffprobe >/dev/null 2>&1 || { err "ffprobe nao encontrado (vem junto com o ffmpeg)"; exit 1; }
ok "ffmpeg $(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f3)"

if [ ! -f "$MARK" ]; then
  err "marca nao encontrada em $MARK"
  printf '         Crie um PNG com fundo transparente ali (o "T" no circulo +\n'
  printf '         "Timas Motion"). Ou aponte outro caminho:\n'
  printf '         MARK=~/Desktop/marca.png bash scripts/watermark.sh\n'
  exit 1
fi
ok "marca: $MARK"

# 2 ─ Videos e seus posters ---------------------------------------------------
head_ "2. Videos e posters (lidos do HTML)"
FILES=("$@")
if [ ${#FILES[@]} -eq 0 ]; then
  while IFS= read -r l; do FILES+=("$l"); done < <(find assets -name '*.mp4' | sort)
fi
[ ${#FILES[@]} -eq 0 ] && { err "nenhum .mp4 encontrado"; exit 1; }

# Resolve o poster de cada video a partir das paginas. Emite:
#   <mp4> TAB <poster ou ""> TAB <0 = exclusivo | 1 = tambem usado como imagem>
MAP=$(python3 - "${FILES[@]}" <<'PY'
import re, sys, glob

pages = {p: open(p, encoding="utf-8").read() for p in glob.glob("*.html")}

def poster_for(mp4):
    for src in pages.values():
        for tag in re.findall(r'<[^>]*data-video="[^"]*"[^>]*>', src):
            if mp4 in tag:
                m = re.search(r'data-poster="([^"]+)"', tag)
                if m: return m.group(1)
        for vid in re.findall(r"<video[^>]*>.*?</video>", src, re.S):
            if mp4 in vid:
                m = re.search(r'poster="([^"]+)"', vid)
                if m: return m.group(1)
    return ""

def shared(poster):
    """True se o arquivo aparece fora de um contexto de poster de video."""
    for src in pages.values():
        for tag in re.findall(r"<[^>]+>", src):
            if poster in tag and "data-video=" not in tag and not tag.startswith("<video"):
                return True
    return False

for mp4 in sys.argv[1:]:
    p = poster_for(mp4)
    print(f"{mp4}\t{p}\t{1 if p and shared(p) else 0}")
PY
)
[ -z "$MAP" ] && { err "nao consegui mapear os posters"; exit 1; }
while IFS=$'\t' read -r v p s; do
  if   [ -z "$p" ]; then printf '  %-30s %s\n' "$(basename "$v")" "sem poster declarado"
  elif [ "$s" = "1" ]; then printf '  %-30s %s  \033[33m(tambem usado como imagem)\033[0m\n' "$(basename "$v")" "$p"
  else printf '  %-30s %s\n' "$(basename "$v")" "$p"; fi
done <<< "$MAP"

mkdir -p "$OUTDIR"

# 3 ─ Processamento -----------------------------------------------------------
head_ "3. Processamento"
while IFS=$'\t' read -r src poster is_shared; do
  [ -f "$src" ] || { err "nao existe: $src"; continue; }
  base=$(basename "$src" .mp4)
  out="$OUTDIR/$base.mp4"

  vw=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$src" 2>/dev/null)
  [ -z "$vw" ] && { err "$src: nao consegui ler a largura"; continue; }
  if [ "$vw" -ge 1000 ]; then mw="$WIDTH_1080"; else mw="$WIDTH_720"; fi

  # Teto de bitrate amarrado a ORIGEM: min(origem, BITRATE_CAP). Sem teto o
  # reencode incha, porque as fontes ja vem comprimidas (540-970 kbps nos
  # pequenos) e um crf generoso "melhora" o arquivo em vez de preserva-lo.
  #
  # O bufsize e 1x o maxrate, nao 2x. O buffer VBV comeca cheio, entao ele e
  # folga que o codificador gasta por cima da media — num clipe de 10s essa
  # folga pesa, e um bufsize dobrado deixava o arquivo crescer ~20% mesmo com
  # o teto no lugar.
  srckbps=$(ffprobe -v error -show_entries format=bit_rate -of csv=p=0 "$src" 2>/dev/null)
  srckbps=$(( ${srckbps:-0} / 1000 ))
  if [ "$srckbps" -gt 0 ]; then
    maxk="$srckbps"
    [ "$maxk" -gt "$BITRATE_CAP" ] && maxk="$BITRATE_CAP"
    rate=(-crf "$CRF" -maxrate "${maxk}k" -bufsize "${maxk}k")
    mode="origem ${srckbps}k -> teto ${maxk}k"
  else
    rate=(-crf "$CRF" -maxrate "${BITRATE_CAP}k" -bufsize "${BITRATE_CAP}k")
    mode="bitrate de origem ilegivel -> teto ${BITRATE_CAP}k"
  fi

  if ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of csv=p=0 "$src" 2>/dev/null | grep -q audio
  then audio=(-c:a aac -b:a 128k); else audio=(-an); fi

  printf '  %-30s largura %s  marca %spx  %s\n' "$base" "$vw" "$mw" "$mode"

  if ! ffmpeg -y -loglevel error -i "$src" -i "$MARK" \
      -filter_complex "[1:v]scale=${mw}:-1,format=rgba,colorchannelmixer=aa=${OPACITY}[wm];[0:v][wm]overlay=(W-w)/2:H-h-${MARGIN}" \
      -c:v libx264 "${rate[@]}" -preset slow -pix_fmt yuv420p \
      "${audio[@]}" -movflags +faststart "$out" 2>&1; then
    err "$base: ffmpeg falhou ao aplicar a marca"; continue
  fi

  a=$(wc -c < "$src" | tr -d ' '); b=$(wc -c < "$out" | tr -d ' ')
  ok "$(printf '%s  %sM -> %sM' "$base" \
        "$(awk "BEGIN{printf \"%.1f\", $a/1048576}")" \
        "$(awk "BEGIN{printf \"%.1f\", $b/1048576}")")"

  # ── Poster ────────────────────────────────────────────────────────────────
  if [ -z "$poster" ]; then
    warn "$base: sem poster declarado no HTML — nenhum gerado"
    SKIPPED=$((SKIPPED+1)); continue
  fi
  if [ "$is_shared" = "1" ]; then
    warn "$base: poster $poster tambem e usado como imagem no site — nao vou marca-lo"
    printf '         (marca-lo colocaria a marca em fotos de galeria; decida a mao)\n'
    SKIPPED=$((SKIPPED+1)); continue
  fi

  pout="$OUTDIR/$(basename "$poster")"
  if [ ! -f "$poster" ]; then
    warn "$base: poster $poster nao existe no disco — nada a marcar"
    SKIPPED=$((SKIPPED+1)); continue
  fi

  # A marca vai sobre o POSTER ATUAL, nao sobre um frame extraido do video.
  # O poster e um frame escolhido a dedo — extrair outro trocaria a imagem que
  # a pagina mostra para quem tem autoplay bloqueado, que e a maioria. Marcar o
  # proprio arquivo preserva a escolha, a resolucao e o enquadramento.
  pw=$(ffprobe -v error -select_streams v:0 -show_entries stream=width \
       -of csv=p=0 "$poster" 2>/dev/null)
  if [ -z "$pw" ] || [ "$pw" -le 0 ]; then
    err "$base: nao consegui ler a largura do poster"; continue
  fi
  # Mesma proporcao visual do video: poster maior, marca proporcionalmente maior.
  pmw=$(( mw * pw / vw ))
  pmargin=$(( MARGIN * pw / vw ))

  if ! ffmpeg -y -loglevel error -i "$poster" -i "$MARK" \
      -filter_complex "[1:v]scale=${pmw}:-1,format=rgba,colorchannelmixer=aa=${OPACITY}[wm];[0:v][wm]overlay=(W-w)/2:H-h-${pmargin}" \
      -q:v 2 "$pout" 2>&1; then
    err "$base: ffmpeg falhou ao marcar o poster"; continue
  fi
  ok "$(basename "$pout")  ${pw}px de largura, marca ${pmw}px"
done <<< "$MAP"

# 4 ─ Resultado ---------------------------------------------------------------
head_ "4. Resultado"
if [ "$ERRORS" -gt 0 ]; then
  printf '\n\033[31m%d erro(s).\033[0m Nada foi copiado para assets/.\n' "$ERRORS"
  exit 1
fi

printf '  Arquivos marcados em %s/\n' "$OUTDIR"
[ "$SKIPPED" -gt 0 ] && printf '  \033[33m%d poster(s) nao regenerado(s)\033[0m — veja os avisos acima.\n' "$SKIPPED"
printf '\n  \033[1mOlhe os videos e os posters antes de trocar qualquer coisa.\033[0m\n'
printf '  Guarde os masters limpos fora do repositorio: depois da troca, o\n'
printf '  arquivo original some do projeto.\n\n'
printf '  Quando aprovar, copie por cima:\n\n'
while IFS=$'\t' read -r src poster is_shared; do
  base=$(basename "$src" .mp4)
  [ -f "$OUTDIR/$base.mp4" ] && printf '    cp %s/%s.mp4 %s\n' "$OUTDIR" "$base" "$src"
  if [ -n "$poster" ] && [ -f "$OUTDIR/$(basename "$poster")" ]; then
    printf '    cp %s/%s %s\n' "$OUTDIR" "$(basename "$poster")" "$poster"
  fi
done <<< "$MAP"
printf '\n  Depois:  bash scripts/check.sh && bash scripts/shots.sh\n'
exit 0
