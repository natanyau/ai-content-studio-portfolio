---
description: Gera o carrossel de um case (10 slides 1080×1350 + PDF) a partir da página e do filme
argument-hint: <case, ex.: tm-003, fogo, crown>
---

Carrossel do case **$ARGUMENTS**. O padrão está em `CLAUDE.md`, seção "Divulgação".

1. **Já existe?** Se houver `scripts/carousel-<case>.py`, rode com
   `CHROMIUM=/opt/pw-browsers/chromium python3 scripts/carousel-<case>.py` (o `CHROMIUM`
   só é necessário em sessão remota). Confira se os textos ainda batem com a página do case.
   Se batem, vá direto ao passo 5.
2. **Textos.** Saem da página do case, não de memória. Não acrescente fato, número ou
   resultado que a página não tenha. A ressalva sai igual à da página. O texto do post segue `.claude/skills/timas-motion-workflow/references/perfil-de-voz.md`. Se o case não tiver
   página, use o card da home e aponte o último slide para `timasmotion.com/#work`.
3. **Imagens.** Use frames do próprio filme, na maior resolução disponível. Imagens de
   galeria pequenas borram no slide: as do Fogo, por exemplo, têm 512 px.
   - Monte uma folha de contato para escolher os planos.
   - Deixe de fora planos com marca de terceiros visível, como caixas de peças.
   - Os frames são extraídos na hora para `.carousel/<case>/frames/`. Nada vai para `assets/`.
4. **Script.** Crie `scripts/carousel-<case>.py` a partir do mais parecido:
   - `carousel-fogo.py` para case com página e filme;
   - `carousel-tm002.py` para case só com card.
   A ordem dos slides é: capa com ressalva → desafio → insight → conceito → direção
   criativa → referência/fontes → produção → filme → chamada com o link e a ressalva
   completa. Use as cores da home, e `#ff4a52` em texto vermelho pequeno.
5. **Revisão.**
   - Olhe o `overview.jpg`, e em tamanho real todo slide com texto sobre foto.
   - Confira a legibilidade, título com palavra sozinha na última linha, e o numeral do
     rodapé (`01/10`…).
   - Me mande a visão geral e o PDF.
6. **Depois do meu ok.**
   - Mande os 10 PNGs e o PDF como anexo.
   - Mande o título do documento para o LinkedIn (até 58 caracteres) e o texto do post, com
     o link `timasmotion.com` no fim.
   - Commite o script num ramo e junte ao `main` com `check.sh` limpo. Ele fica fora do site
     (`scripts/` está no `exclude`).
   - Acrescente a linha do script na tabela de estrutura do `CLAUDE.md`.
