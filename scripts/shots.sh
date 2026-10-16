#!/usr/bin/env bash
# Renderiza as paginas em mobile / tablet / desktop e salva PNGs em .preview/.
# Uso: bash scripts/shots.sh [arquivo.html ...]   (padrao: todas as .html da raiz)
# Requer: pip install playwright && playwright install chromium

set -euo pipefail
cd "$(dirname "$0")/.."

python3 -c "import playwright" 2>/dev/null || {
  echo "Playwright nao instalado. Rode:  pip install playwright && playwright install chromium"
  exit 1
}

FILES=("$@")
if [ ${#FILES[@]} -eq 0 ]; then
  while IFS= read -r line; do FILES+=("$line"); done < <(find . -maxdepth 1 -name '*.html' -exec basename {} \; | grep -v backup | sort)
fi

mkdir -p .preview

# Auditoria de acessibilidade com axe-core (WCAG 2.2 A/AA), por pagina e viewport.
# O arquivo nao entra no repositorio: e baixado uma vez do registro do npm para
# .preview/.axe/ e conferido pelo hash publicado pelo npm. Sem rede, as fotos saem
# do mesmo jeito e a auditoria e pulada. AXE=0 desliga.
AXE_VERSION=4.13.0
AXE_SHA512="UzGt8zg7Ny8djbYMhxl2zuEevVa7r2gJjYY5Lwr1xM7+XU2nd6CkIWFTVcCIbAP63vSz71NaVyyuSk9lHKcy0A=="
AXE_JS=".preview/.axe/axe-core-$AXE_VERSION.min.js"
if [ "${AXE:-1}" = "0" ]; then
  AXE_JS=""
elif [ ! -s "$AXE_JS" ]; then
  mkdir -p .preview/.axe
  tgz=".preview/.axe/axe-core-$AXE_VERSION.tgz"
  if curl -fsSL "https://registry.npmjs.org/axe-core/-/axe-core-$AXE_VERSION.tgz" -o "$tgz" 2>/dev/null &&
     python3 -c "import sys,hashlib,base64; sys.exit(base64.b64encode(hashlib.sha512(open(sys.argv[1],'rb').read()).digest()).decode()!=sys.argv[2])" "$tgz" "$AXE_SHA512" &&
     tar -xzOf "$tgz" package/axe.min.js > "$AXE_JS.tmp"; then
    mv "$AXE_JS.tmp" "$AXE_JS"
  else
    echo "AVISO: nao deu para baixar e conferir o axe-core $AXE_VERSION; seguindo sem a auditoria de acessibilidade."
    rm -f "$AXE_JS.tmp"
    AXE_JS=""
  fi
  rm -f "$tgz"
fi

AXE_JS="$AXE_JS" python3 - "${FILES[@]}" <<'PY'
import sys, os, json, pathlib
from playwright.sync_api import sync_playwright

files = sys.argv[1:]
root = pathlib.Path.cwd()
axe_js = os.environ.get("AXE_JS") or None
AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
audits = {}  # pagina -> {regra: {...}}
sizes = [("mobile", 390, 844, True), ("tablet", 768, 1024, False), ("desktop", 1440, 900, False)]

def launch(p):
    """Usa o Chromium do Playwright; se a versao baixada nao bater, procura um binario existente."""
    try:
        return p.chromium.launch()
    except Exception:
        import glob
        roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""), os.path.expanduser("~/.cache/ms-playwright")]
        for root in filter(None, roots):
            for pat in ("chromium*/chrome-linux/chrome", "chromium*/chrome-mac/*/Chromium", "chromium*/chrome-win/chrome.exe"):
                hits = sorted(glob.glob(os.path.join(root, pat)))
                if hits:
                    return p.chromium.launch(executable_path=hits[-1])
        raise

with sync_playwright() as p:
    browser = launch(p)
    for f in files:
        for name, w, h, mobile in sizes:
            ctx = browser.new_context(viewport={"width": w, "height": h}, is_mobile=mobile)
            page = ctx.new_page()
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(f"file://{root/f}")
            page.wait_for_timeout(1500)
            out = f".preview/{pathlib.Path(f).stem}__{name}.png"
            page.screenshot(path=out)
            sw = page.evaluate("document.documentElement.scrollWidth")
            cw = page.evaluate("document.documentElement.clientWidth")
            compat = page.evaluate("document.compatMode")
            flags = []
            if sw > cw + 1:  flags.append(f"SCROLL HORIZONTAL ({sw}>{cw})")
            if compat != "CSS1Compat": flags.append("QUIRKS MODE (falta <!DOCTYPE html>)")
            if errors: flags.append(f"{len(errors)} erro(s) de JS: {errors[0][:80]}")
            print(f"{out:52} {'  ⚠ ' + ' | '.join(flags) if flags else 'ok'}")
            if axe_js:
                page.add_script_tag(path=axe_js)
                res = page.evaluate("t => axe.run(document, {runOnly: {type: 'tag', values: t}})", AXE_TAGS)
                found = audits.setdefault(f, {})
                for kind in ("violations", "incomplete"):
                    for v in res[kind]:
                        r = found.setdefault((kind, v["id"]), {"impact": v["impact"], "help": v["help"],
                                                               "url": v["helpUrl"], "views": [], "nodes": {}})
                        r["views"].append(name)
                        for n in v["nodes"]:
                            sel = " ".join(map(str, n["target"]))
                            r["nodes"].setdefault(f"{sel}  {' '.join(n['html'].split())[:70]}", n.get("failureSummary") or "")
            ctx.close()
    browser.close()

if axe_js:
    order = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3, None: 4}
    total = 0
    print("\nAcessibilidade (axe-core, WCAG 2.2 A/AA)")
    for f in files:
        found = audits.get(f, {})
        viol = sorted(((k[1], r) for k, r in found.items() if k[0] == "violations"), key=lambda x: order[x[1]["impact"]])
        todo = [k[1] for k in found if k[0] == "incomplete"]
        total += len(viol)
        print(f"  {f:42} {'ok' if not viol else f'⚠ {len(viol)} regra(s) violada(s)'}"
              + (f"  · {len(todo)} a conferir à mão" if todo else ""))
        for rid, r in viol:
            views = "todas as telas" if len(r["views"]) == 3 else "/".join(r["views"])
            print(f"      {r['impact'] or '?':9} {rid}: {r['help']} — {len(r['nodes'])} elemento(s), {views}")
            for sel in list(r["nodes"])[:3]:
                print(f"                {sel[:90]}")
        pathlib.Path(f".preview/axe__{pathlib.Path(f).stem}.json").write_text(json.dumps(
            [{"tipo": k[0], "regra": k[1], **{**r, "nodes": [{"alvo": s, "motivo": m} for s, m in r["nodes"].items()]}}
             for k, r in found.items()], ensure_ascii=False, indent=2))
    print("  Detalhes em .preview/axe__<pagina>.json. O axe cobre só parte da WCAG: teclado,"
          "\n  ordem de foco e leitor de tela continuam pedindo um teste à mão.")
PY
echo
echo "PNGs em .preview/ — abra e compare antes de publicar."
