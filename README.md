# Timas Motion

Código do portfólio publicado em [timasmotion.com](https://timasmotion.com): filmes e
estudos de caso de produção com IA, com direção criativa da Timas Motion.

O site é HTML estático servido pelo GitHub Pages, sem build e sem dependências. O que
está no ramo `main` é o que está no ar.

| Página | Arquivo |
|---|---|
| Home | `index.html` |
| Case Crown | `crown-featured-case.html` |
| Case Fogo | `fogo-featured-case.html` |
| Case TM-003 · Casa Cavoquinho | `tm-003-casa-cavoquinho.html` |
| Copyright e termos | `terms.html` |

Para rodar localmente:

```bash
python3 -m http.server 8000   # e abra http://localhost:8000
```

Antes de publicar, `bash scripts/check.sh` precisa terminar sem erros. As regras do
projeto e o processo de cada case estão em `CLAUDE.md`.

## Direitos

Todos os direitos reservados. O repositório é público para que o GitHub Pages sirva o
site; isso não é uma licença de código aberto. Vídeos, imagens e textos não podem ser
reutilizados sem autorização. Detalhes em [`LICENSE`](LICENSE) e em
[timasmotion.com/terms.html](https://timasmotion.com/terms.html).

Contato: hello@timasmotion.com
