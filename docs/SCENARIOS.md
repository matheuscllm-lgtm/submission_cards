# Comparador de cenários

## Escopo atual

Simula rotas para uma mesma cópia com dados já normalizados e uma única moeda.
Não consulta preços, não verifica comparáveis e não estima gem rate.
Não substitui o motor de recomendação nem otimiza lotes.
Toda saída inclui `simulation_only: true` e `submission_ready: false`.

```bash
PYTHONPATH=src python -m submission_cards.cli compare data/private/scenario.json --output outputs/private/comparison.json
```

O JSON de entrada deve seguir `examples/scenario.synthetic.json`. O exemplo contém
valores fictícios para demonstrar o cálculo; não são preços nem probabilidades reais.
O comando não sobrescreve arquivos existentes e não imprime dados individuais.

## Campos obrigatórios

- `card`: game, set, number, variant, language e condition, sem lacunas.
- `currency`: código de três letras maiúsculas; todas as rotas devem usar a mesma moeda.
- `as_of`: data de referência ISO.
- `raw_net`: valor RAW já líquido de todos os custos dessa alternativa.
- `raw_receipt_days`: dias até recebimento da venda RAW.
- `annual_discount_rate`: taxa anual explicitamente informada. Zero significa cenário
  sem desconto, não estimativa de custo de capital vigente.
- `budget`: teto adicional na moeda informada ou `null` se desconhecido.
- `routes`: alternativas com IDs únicos e `assumption_basis` descrevendo as hipóteses.
- `upfront_costs`: mapa de custos pagos hoje, deduzidos uma única vez por rota.
- `outcomes`: resultados mutuamente exclusivos, com probabilidades somando 1.
- Cada resultado tem `label`, `probability`, `gross_sale`, `sale_fee_rate`,
  `cashout_fee_rate`, `receipt_costs` e `receipt_days`.

Identificar empresa, nota e designação de etiqueta em cada `label`. A verificação
dessas identidades e da qualidade das fontes é responsabilidade da futura camada de dados.
Datas de recebimento são hipóteses; o cálculo não prevê tempo de venda.
Valores desconhecidos não podem ser substituídos por zero para viabilizar uma análise.

## Fórmulas

```text
receipt = gross_sale × (1 − sale_fee_rate) × (1 − cashout_fee_rate) − receipt_costs
EV = Σ(probability × receipt) − Σ(upfront_costs)
incremental_net = EV − raw_net
PV = Σ(probability × receipt / (1 + annual_discount_rate)^(receipt_days / 365)) − Σ(upfront_costs)
incremental_PV = PV − raw_net / (1 + annual_discount_rate)^(raw_receipt_days / 365)
```

Venda incide sobre bruto. Cashout incide sobre o saldo após venda. `receipt_costs` são
despesas adicionais no recebimento; taxas reais com outra base devem ser normalizadas
explicitamente antes de usar este modelo. Grading, frete e seguro devem ser alocados
uma vez em custos iniciais ou de recebimento, conforme o fluxo.

Capital necessário = custos iniciais + reserva para eventual recebimento líquido negativo
no pior resultado de probabilidade positiva. ROI incremental = ganho nominal / capital.
Capital zero produz ROI ausente, não infinito. O custo histórico da carta não entra no
ganho incremental, pois a alternativa RAW já representa seu custo de oportunidade.

## Prazos e risco

Comparar horizontes de 90, 180 e 365 dias. São limites para recebimento, não datas de
valorização automática. Se um resultado possível ultrapassa o horizonte, a rota fica
excluída nesse cenário. O comparador não modela recebimentos parciais ou estoques não vendidos.

Mostrar separadamente probabilidade de perder dinheiro adicional e de render menos
que RAW, sob a distribuição informada. A segunda pode existir mesmo com lucro de caixa.
O ranking aritmético usa ganho incremental em valor presente, sem convertê-lo em
aprovação de envio. Quando o custo de capital é zero, equivale ao ganho nominal.

Orçamento ausente gera `BUDGET_UNSET`. Orçamento informado testa apenas uma rota/cópia
isolada; não garante que o conjunto das cópias cabe no teto. Seleção de carteira, custos
compartilhados, mínimos de lote, tolerância de risco, evidência de mercado e pré-screen
continuam pendentes. Retenção deliberada não deve ser inferida de exclusão por prazo.
