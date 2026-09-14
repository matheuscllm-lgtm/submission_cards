<!-- FLEET:ESTILO-RESPOSTA v1 (2026-09-14) — cópia-mestra: scanners-commons/08-ESTILO-RESPOSTA.md. Editar LÁ e replicar; não divergir nesta cópia. -->
> **Estilo de resposta obrigatório (operador, 2026-09-14): CONCISO — teto de 200 palavras.**
> Toda resposta no chat, nesta ordem: **1) Objetivo** — 1 linha do que foi pedido · **2) O que foi feito** — bullets curtos, cada um com o *porquê* da decisão · **3) Dependências/pendências** — o que falta, o que bloqueia, de quem depende (`nenhuma` quando não houver).
> O teto conta **só prosa**. **Fora do teto** (nunca resumir, cortar nem "amostrar" pra caber): a tabela de entrega gerada pela ferramenta do repo (colada VERBATIM), blocos de comando/código, saída de teste colada como prova e artefato canônico do repo (brief, relatório, análise).
> Sem preâmbulo, sem repetir o pedido, sem recapitular o que já foi dito. Não cabe em 200 palavras? Entregue o essencial dentro do teto e ofereça o detalhe ("quer o detalhe de X?") — nunca estoure em silêncio.

# CLAUDE.md — submission_cards

Decide, **por carta e por cópia**, o melhor destino econômico: vender/manter RAW,
mandar pra COMC (Standard/Select/Elite), submeter a PSA ou CGC, ou **reter até
existir dado confiável**.

> ⚠️ **A fonte de verdade das regras deste repo é [`AGENTS.md`](AGENTS.md)** — leia-o
> antes de qualquer mudança. Este arquivo só aponta pra lá (e traz o bloco de estilo
> da frota acima); não duplica as regras, pra não criar duas fontes divergentes.

Leitura obrigatória antes de mexer (ordem do `AGENTS.md`): `README.md` →
`docs/PROJECT_STATE.md` → `docs/METHODOLOGY.md`.

Testes: `PYTHONPATH=src python -m unittest discover -s tests -v` (rodar antes de publicar).

Invariantes que valem lembrar (detalhe no `AGENTS.md`): nunca commitar
`data/private/`, `outputs/private/`, credencial ou sessão autenticada; identidade
de carta casa jogo+set+número+variante+idioma+condição (graded também casa
certificadora+nota); **valuation por venda concluída**, anúncio ativo rotulado
à parte; gem rate/amostra/liquidez/data sempre visíveis; sem meta de quantidade de
cartas elegíveis; evidência insuficiente → `REVIEW_DATA`, nunca certeza imputada;
"Near Mint" da Collectr é metadado de estoque, **não** previsão de nota.

Fluxo: **branch + PR**; atualizar `docs/PROJECT_STATE.md` quando marco ou regra de
decisão mudar; nunca publicar resultado de scan ou inventário no GitHub.
