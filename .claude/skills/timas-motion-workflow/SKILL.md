---
name: timas-motion-workflow
description: Executa o processo completo da Timas Motion, da pesquisa e criação de cases à preparação de mídia, manutenção do portfólio, validação, revisão, publicação e divulgação. Use ao criar ou revisar um case, alterar o site, preparar vídeos e posters ou produzir carrosséis da Timas Motion.
---

# Processo de trabalho — Timas Motion

## Uso e fontes

Execute as etapas pertinentes ao pedido; um ajuste pontual não exige produzir um case inteiro. Responda em português e mantenha o idioma editorial da página trabalhada.

Localize a raiz do repositório pelos arquivos `CLAUDE.md`, `index.html` e `scripts/check.sh`. Leia o `CLAUDE.md` atual antes de editar.

Os comandos do projeto executam partes deste processo passo a passo: `/novo-case` cobre as etapas 1 a 7 para um case novo e para antes de publicar; `/carrossel <case>` cobre a etapa 8. Quando o pedido for exatamente um desses, siga o comando (`.claude/commands/`); esta skill dá o contexto. Se mudar uma regra aqui, mude também no comando correspondente e no `CLAUDE.md`. Consulte [o guia completo](references/guia-do-projeto.md) para parâmetros, exceções e decisões históricas. Essa referência é uma cópia do `CLAUDE.md` em 15/10/2026, depois do carrossel da Crown; em divergências, confira a versão atual e as instruções do usuário. Não invente etapas históricas, resultados ou aprovações ausentes das fontes.

## 1. Entender a entrega e preparar o trabalho

1. Identifique objetivo, público, case, materiais disponíveis e saída esperada: página, vídeo, poster, preview ou carrossel.
2. Inspecione o estado do Git e preserve alterações existentes. Trabalhe em um ramo para mudanças no projeto.
3. Leia os arquivos e scripts relevantes antes de usá-los. Verifique ferramentas disponíveis; não presuma acesso a Artifact, navegador, rede ou publicação.
4. Para mudanças visuais, rode `bash scripts/shots.sh` antes da edição e preserve as capturas para comparação.
5. Pergunte apenas por informações que bloqueiem a entrega. Avance no restante com as evidências disponíveis.

## 2. Pesquisar e conferir o material

- Assista ao filme ou examine frames, incluindo abertura e fechamento, antes de descrevê-lo. Confira duração e conteúdo real.
- Registre cada afirmação factual com fonte nomeada, URL, o que sustenta e seus limites. Separe fatos sobre a propriedade de referências visuais de paisagem.
- Use tom analítico, simples e comedido. Não atribua resultados comerciais, aprovação ou afiliação sem evidência. O [perfil de voz](references/perfil-de-voz.md) detalha esse tom com exemplos tirados dos cases publicados; siga-o em página, carrossel, post e e-mail.
- Preserve as ressalvas de independência na capa, nos metadados e no fechamento. Na Crown, mantenha o sentido exato: não encomendado, revisado ou endossado; não troque por uma negação de afiliação.

## 3. Criar ou revisar o case

Use `tm-003-casa-cavoquinho.html` e `css/tm-003-case.css` como molde. Reescreva seção por seção; não use substituição global para adaptar nomes, IDs e links.

Mantenha esta sequência:

1. Capa: marca ou lugar como título; código TM-00X e local na linha pequena.
2. The Film, imediatamente abaixo da capa.
3. 01 Challenge, com Strategic focus, Project scope e Evidence standard.
4. Insight, Strategy, Big Idea e Creative Direction.
5. Research & Reality / Research Sources, com fontes e limites.
6. Production e Edit.
7. Outcome, diferenciando entregas Produced e Documented.
8. Transparency.

Use fundo `#0a0a0b`, cards `#17171a`, linhas `#2a2a2e`, textos `#fff` e `#b7b7bc`. Reserve `#e1262f` para destaques grandes e `#ff4a52` para texto vermelho pequeno. Distribua as ressalvas por função, evitando repetição em todas as seções. Remova notas internas antes de publicar.

## 4. Preparar vídeos, imagens e marca

- Nunca grave, altere ou substitua arquivos em `assets/`. Prepare resultados em área de trabalho; a substituição de produção é manual, com o arquivo novo revisado.
- Guarde masters limpos fora do repositório e comprima a partir deles. Não faça reencode sucessivo.
- Para filme novo: 720×1280, CRF 23, maxrate 1800k com texto ou 1000k sem texto, bufsize igual ao maxrate e `-movflags +faststart`. Verifique SSIM ≥ 0,97 contra o master. Solicite versão limpa se houver legenda queimada que precise sair.
- Prepare vídeo e poster juntos. Confira o vínculo real no HTML (`poster` / `data-poster`), incluindo exceções de nome como `cha.jpg`.
- Use `scripts/watermark.sh` após ler o guia: saída em `.watermark/out/`, marca padrão de 120 px em vídeo de 720, margem 140 e opacidade 0,55. Calibre em um arquivo primeiro.
- Preserve o enquadramento do poster existente e escale a marca proporcionalmente. Posters também usados como fotos exigem tratamento separado. Para `cover`, consulte o ajuste `BITRATE_CAP=940`; para `crown`, `MARGIN=220`.
- Para imagens de cases, detecte cortes e extraia frames intermediários do filme: 720×1280, JPEG q82, alt iniciado por `Film still:`. Capa e Big Idea usam primeiro e último plano.
- Em uploads manuais pelo GitHub, confira ramo, pasta e hash resultante. Se o arquivo correto chegou em outro caminho, adapte a referência quando possível.

## 5. Integrar ao site

- Preserve HTML estático e CSS/JS inline da home. Não introduza framework ou build.
- Navegação usa caminhos da raiz (`/terms.html`); assets usam caminhos relativos. Remova prefixos antigos `/ai-content-studio-portfolio/` quando encontrados em links ativos.
- Toda página começa com DOCTYPE e inclui lang, charset e viewport.
- Página compartilhável leva title, description, canonical, Open Graph e Twitter. Página nova entra no sitemap; declare o motivo de alterações em sitemap ou robots. O 404 é exceção aos metadados de compartilhamento.
- Preserve CNAME, `_config.yml`, direitos autorais e links para termos. Arquivos de trabalho novos na raiz precisam de exclusão do Pages; esta skill fica em `.claude/`, já excluída.
- Cases levam author, copyright, og:site_name, og:locale, favicon vetorial, vídeo com `controlsList="nodownload"` e `disablePictureInPicture`, e rodapé com `/terms.html`. Evite links diretos para MP4.
- Prepare preview 1200×630. Se o herói mudar, atualize a composição correspondente em área de trabalho e entregue para substituição manual.
- Se mudar o Instagram, confira também o QR embutido: alterar só a URL não atualiza a imagem.

## 6. Validar e preparar revisão

Execute na raiz, nesta ordem antes de publicar:

```bash
bash scripts/check.sh
bash scripts/shots.sh
python3 -m http.server 8000
```

Exija zero erros no check, analise os avisos e abra a prévia local. Compare capturas antes/depois e inspecione de verdade mobile, tablet e desktop, verificando recortes, legibilidade, scroll horizontal, links e erros de JavaScript. As capturas ficam em `.preview/`, fora do versionamento.

Confira vídeos em navegador com suporte a H.264: posters nas capturas do Chromium remoto não provam falha de reprodução. Verifique a política atual antes de atribuir erros a bloqueios de rede; as limitações históricas do guia podem mudar. `origin/main` é referência do Git, não prova de deploy concluído.

Prepare prévia privada para revisão pelo celular. Use Artifact se disponível; caso contrário entregue arquivos ou outra prévia privada disponível e explique a limitação. Nunca afirme ter inspecionado algo que não conseguiu abrir.

## 7. Publicar quando autorizado

A criação ou revisão de arquivos não autoriza publicação. Conforme o guia do projeto, merge no main exige autorização explícita equivalente a “pode publicar”. Prepare primeiro a entrega concreta e revisável; se a autorização já estiver na conversa, não a solicite de novo.

Após autorização, atualize a integração com main, resolva conflitos, valide o resultado e faça merge `--no-ff`. Faça commits com uma mudança coerente e mensagem sobre o efeito. Push para main publica via GitHub Pages; confirme o resultado do workflow/deploy quando acessível.

Depois, confira URLs e previews das páginas afetadas. Atualize o cache no LinkedIn Post Inspector quando disponível; caso contrário, entregue as URLs para essa etapa manual. Não declare a publicação concluída apenas porque o merge ocorreu.

## 8. Preparar divulgação

- Gere carrossel de 10 slides 1080×1350 e PDF para LinkedIn usando `scripts/carousel-tm003.py` como molde.
- Para TM-002, use `scripts/carousel-tm002.py`, aponte para `https://timasmotion.com/#work`, mantenha a ressalva documentada e exclua planos com caixas de marcas de fabricantes.
- Para Fogo, use `scripts/carousel-fogo.py` e frames do filme 1080×1920; as imagens de 512 px da pasta não têm resolução suficiente.
- Para Crown, use `scripts/carousel-crown.py`. É um case de estratégia, não de filme: usa um frame do cartão de marca de 4 s e as duas imagens de produto sem a faixa do rodapé.
- As imagens de produto da Crown (`assets/images/rt28111-led-tail-light.png` e `rt31046-big-brake-kit.png`) trazem a ressalva escrita no rodapé. Se forem refeitas, a faixa sai com a mesma redação da página, sem negar afiliação.
- Confira textos, fontes, ressalvas, resolução e destino do CTA em todas as páginas e slides.
- No Instagram, direcione para bio ou story com figurinha de link. Prepare os materiais; envio ou postagem requer instrução do usuário.

## Entrega e conclusão

Informe o que foi criado ou alterado, caminhos dos arquivos, validações executadas, limitações e pendências manuais concretas. Diferencie preparado, revisado e publicado. Não execute etapas de mídia, deploy ou divulgação que não façam parte do pedido atual.

Ao atualizar esta skill, confira novamente o guia vigente e sincronize a referência, preservando decisões e exceções verificadas.
