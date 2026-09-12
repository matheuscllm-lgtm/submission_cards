# Submission Cards

Projeto para decidir, por carta e por cópia, a melhor destinação econômica:

- vender ou manter RAW;
- enviar para COMC Standard, Select ou Elite;
- submeter para PSA ou CGC;
- reter até existirem dados confiáveis.

O modelo não procura uma quantidade fixa de cartas elegíveis. Cada item precisa superar
critérios mínimos de identificação, liquidez, qualidade dos dados e retorno incremental.

## Regras centrais

1. Comparar apenas a mesma carta, set, número, variante, idioma e condição.
2. Para graduadas, comparar também a mesma certificadora e nota.
3. Usar vendas realizadas; anúncios ativos servem apenas como contexto.
4. Aplicar o *gem rate* específico da carta. Taxas genéricas só podem ser usadas como
   estimativa explicitamente marcada.
5. Incluir grading, processamento, frete, seguro, taxas de venda e demais custos aplicáveis.
6. Comparar o valor esperado da submissão ao líquido de venda RAW e ao custo de espera.
7. Bloquear recomendações quando identificação, amostra ou liquidez forem insuficientes.

## Uso atual

Instale o pacote no ambiente de desenvolvimento:

```bash
python -m pip install -e .
```

Valide um export do Collectr:

```bash
python -m submission_cards.cli validate data/private/export.csv
```

Execute os testes:

```bash
python -m unittest discover -s tests -v
```

Durante o desenvolvimento sem instalação:

```bash
PYTHONPATH=src python -m submission_cards.cli validate data/private/export.csv
```

## Dados privados

O repositório é público. Exports do Collectr e planilhas com inventário individual devem
ficar em `data/private/`, que é ignorado pelo Git. Não publique preços de aquisição,
quantidades ou posições pessoais sem autorização explícita.

O estado herdado da análise de 11/09/2026 está em
[`docs/PROJECT_STATE.md`](docs/PROJECT_STATE.md). A metodologia está em
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

O [prompt de análise](docs/ANALYSIS_PROMPT.md) define entradas, comparáveis, custos,
incerteza e formato de saída. Objetivo incremental e cenários de prazo foram aprovados.

GitHub Actions executa somente testes sintéticos em pushes e PRs.
O [comparador de cenários](docs/SCENARIOS.md) calcula ganho versus RAW e prazos de
90/180/365 dias a partir de hipóteses normalizadas. Para simular:

```bash
PYTHONPATH=src python -m submission_cards.cli compare examples/scenario.synthetic.json --output outputs/private/example-comparison.json
```

O exemplo é inteiramente fictício. O comparador não consulta preços nem recomenda
submissões. Coleta de mercado, pré-screen, limites de risco e alocação do orçamento
continuam pendentes. Orçamento ausente é sinalizado, nunca tratado como ilimitado.
