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
  mapfile -t FILES < <(find . -maxdepth 1 -name '*.html' -printf '%f\n' | grep -v backup | sort)
fi

mkdir -p .preview
python3 - "${FILES[@]}" <<'PY'
import sys, os, pathlib
from playwright.sync_api import sync_playwright

files = sys.argv[1:]
root = pathlib.Path.cwd()
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
            ctx.close()
    browser.close()
PY
echo
echo "PNGs em .preview/ — abra e compare antes de publicar."
