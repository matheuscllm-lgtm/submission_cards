# Metodologia de decisão

## 1. Identidade canônica

Nenhum preço ou população deve ser agregado antes de confirmar:

- jogo;
- nome da carta;
- set e número;
- variante/acabamento;
- idioma;
- condição;
- certificadora e nota, quando graduada.

Itens ambíguos recebem `REVIEW_DATA`.

## 2. Dados mínimos

Para cada alternativa, registrar:

- preço e data de cada venda realizada comparável;
- número de vendas e janela observada;
- preço RAW líquido;
- preços PSA e CGC por nota relevante;
- população por nota e submissões observadas;
- custos fixos, percentuais, frete, seguro e prazo;
- fonte e data de atualização.

## 3. Gem rate

O *gem rate* deve ser específico da carta e da certificadora:

```text
gem_rate = quantidade_na_nota_alvo / total_graduado_da_carta
```

A amostra e a incerteza acompanham a estimativa. Amostras pequenas não justificam uma
recomendação forte; devem sofrer ajuste conservador ou resultar em `REVIEW_DATA`.

A taxa populacional é uma observação de exemplares já submetidos, não uma probabilidade
individual calibrada. Seleção prévia, reenvios e mudanças de etiqueta podem afetá-la.
Qualquer ajuste por pré-screen precisa de evidência, hipóteses identificadas e sensibilidade.
Incluir notas inferiores e resultados sem graduação; as probabilidades devem somar 1.
CGC Gem Mint, Pristine e etiquetas históricas exigem comparáveis separados.

## 4. Valor líquido

Para cada nota `g`:

```text
liquido_g = preco_venda_g
            - taxas_de_venda_g
            - cashout_g
            - custos_logisticos_g
            - custos_de_grading_g
            - demais_custos_aplicaveis_g
```

O valor esperado do grading é:

```text
EV_grading = soma(probabilidade_g * liquido_g)
```

O ganho econômico relevante é incremental:

```text
EV_incremental = EV_grading - liquido_RAW
ROI_incremental = EV_incremental / capital_incremental
```

O cálculo final também deve considerar prazo, liquidez e risco de dados obsoletos.
Custos desconhecidos permanecem ausentes. Os zeros do arquivo de configuração são
placeholders, não taxas confirmadas. Não contar custos por lote novamente por resultado.
Custo histórico pertence ao lucro total; a decisão de submeter usa o valor RAW como
custo de oportunidade. Retenção deliberada e dados insuficientes são estados distintos.

## 5. Escolha de rota

Uma rota só é elegível quando:

1. os dados de identidade estão completos;
2. existe liquidez mínima configurada;
3. a amostra de preço e grading é utilizável;
4. o retorno incremental supera os limites configurados;
5. o capital e o prazo são compatíveis;
6. a carta passa no pré-screen exigido para grading.

Entre rotas elegíveis, escolher a de maior valor ajustado a risco e prazo. Não existe meta de
“encontrar 100 cartas”. O total recomendado é consequência dos critérios.

## 6. Estados de incerteza

- `LOW_SAMPLE`: poucos dados de preço ou população;
- `STALE_PRICE`: vendas antigas;
- `LOW_LIQUIDITY`: baixa frequência de vendas;
- `IDENTITY_AMBIGUOUS`: variante/idioma/condição incertos;
- `PHYSICAL_SCREEN_REQUIRED`: cópia ainda não examinada;
- `COSTS_STALE`: taxas não atualizadas;
- `REVIEW_DATA`: não emitir recomendação econômica.
