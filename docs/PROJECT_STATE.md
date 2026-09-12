# Estado do projeto

## Base técnica

Projeto de análise de destinação RAW, COMC, PSA e CGC a partir de exports Collectr.
Disponíveis: validador CSV, CLI, testes sintéticos e documentação de metodologia.
Nesta revisão: prompt de análise ampliado, validação de quantidade inteira/finita,
datas dinâmicas do export, categorias acentuadas e rejeição de linhas malformadas.
Workflow público de CI preparado para executar apenas testes sintéticos e ajuda da CLI.
O comparador de cenários foi implementado para entradas normalizadas em JSON, com
horizontes de 90, 180 e 365 dias, EV líquido, valor presente, risco versus RAW e orçamento
explícito. Não recomenda lotes: coletores, validação de evidência e alocação de carteira
continuam pendentes. Configurações de taxas são exemplos, não valores vigentes.

## Continuidade

Inventário original, planilhas anteriores e reconciliações permanecem em armazenamento
privado. Este documento público registra apenas evolução de código e metodologia.
Não publicar posições, valores, contagens ou resultados de análises individuais.

## Pendências

1. Reconciliar registros e cópias entre export e plano anterior em ambiente privado.
2. Normalizar identidade, variante, idioma e condição sem inferências silenciosas.
3. Consultar taxas oficiais atuais e vendas realizadas por nota e empresa.
4. Distinguir gem rate observado de previsão por cópia examinada.
5. Informar valor do orçamento, limite operacional de prazo e tolerância de risco.
6. Integrar o comparador a dados verificados e implementar alocação de carteira.
7. Conectar entradas e saídas a armazenamento privado antes de executar análises no Actions.

## Decisões aprovadas

Priorizar lucro incremental líquido, sujeito a prazo e risco. Comparar cenários de
90, 180 e 365 dias. Usar teto total de capital adicional, sem meta fixa de cartas.
O usuário autorizou prosseguir com essas propostas.

O valor numérico do teto, um prazo máximo único e a tolerância de perda não foram
informados. Não supor orçamento ilimitado nem autorização automática para 365 dias.
O prompt está em `docs/ANALYSIS_PROMPT.md`. Limites de evidência seguem em definição.
A entrevista usa a skill pública grill-me/grilling de Matt Pocock, consultada em:
https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
Ela não foi instalada como skill local. O cálculo pode avançar com hipóteses explícitas;
a recomendação operacional aguarda dados de mercado e critérios restantes.

## Política de publicação

Código, metodologia e testes sintéticos podem ser públicos. Dados de coleção e seus
resultados ficam privados, inclusive logs, caches, artefatos e resumos de Actions.
