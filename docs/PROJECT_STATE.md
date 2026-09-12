# Estado do projeto

## Base técnica

Projeto de análise de destinação RAW, COMC, PSA e CGC a partir de exports Collectr.
Disponíveis: validador CSV, CLI, testes sintéticos e documentação de metodologia.
O motor de recomendação, coletores de mercado e integração com armazenamento privado
não foram implementados. Configurações de taxas são exemplos, não valores vigentes.

## Continuidade

Inventário original, planilhas anteriores e reconciliações permanecem em armazenamento
privado. Este documento público registra apenas evolução de código e metodologia.
Não publicar posições, valores, contagens ou resultados de análises individuais.

## Pendências

1. Reconciliar registros e cópias entre export e plano anterior em ambiente privado.
2. Normalizar identidade, variante, idioma e condição sem inferências silenciosas.
3. Consultar taxas oficiais atuais e vendas realizadas por nota e empresa.
4. Distinguir gem rate observado de previsão por cópia examinada.
5. Definir objetivo econômico, restrições de capital e horizonte com o usuário.
6. Implementar motor de decisão com dados ausentes explícitos.
7. Conectar entradas e saídas a armazenamento privado antes de executar análises no Actions.

## Política de publicação

Código, metodologia e testes sintéticos podem ser públicos. Dados de coleção e seus
resultados ficam privados, inclusive logs, caches, artefatos e resumos de Actions.
