# Prompt de análise de submissão

Versão de trabalho. Objetivo econômico, orçamento, horizonte e limites de risco ainda
dependem da entrevista com o usuário. Não transformar propostas em regras aprovadas.

## Missão

Analise meu inventário exportado do Collectr e indique a destinação por cópia:
venda RAW, COMC Standard/Select/Elite, PSA, CGC, retenção ou revisão de dados.
Compare alternativas elegíveis e explique o ganho incremental da submissão sobre a venda
RAW. Não estabeleça meta de quantidade nem garanta nota ou lucro.

Leia README.md, AGENTS.md, PROJECT_STATE.md e METHODOLOGY.md antes de executar.
Recupere decisões já tomadas e arquivos existentes. Não reinicie a análise sem necessidade.

## 1. Integridade do inventário

- Preserve o export original; registre hash, data, moeda e identificador da importação.
- Reconcile registros, cópias e categoria. Não confunda uma linha com uma carta física.
- Identifique uploads duplicados pelo conteúdo, sem somar duas vezes a mesma coleção.
- Atribua IDs estáveis às posições e cópias, mantendo vínculo com a linha original.
- Valide números inteiros, cabeçalhos, registros truncados e condição declarada.
- Se idioma, moeda ou variante estiverem ausentes, registre a lacuna. Não presuma inglês,
  USD ou versão padrão pelo nome da carta.
- Não converta custo de aquisição zero do aplicativo em custo real zero sem confirmação.

## 2. Identidade e alternativas

Compare apenas jogo, set, número, variante, idioma e condição equivalentes.
Para graduadas, exija também empresa, nota e designação exata da etiqueta.
Avalie RAW, PSA 9 e 10, notas inferiores relevantes e CGC 9/9.5, Gem Mint 10 e
Pristine 10 quando houver comparáveis. Identifique etiquetas antigas e regras da época;
não combine CGC 9.5 antigo, Gem Mint e Pristine automaticamente.
Compare envio direto e intermediado pela COMC quando ambos forem possíveis.

## 3. Fontes e rastreabilidade

Consulte páginas oficiais de PSA, CGC e COMC para taxas, mínimo de lote, seguro,
valor declarado, sobretaxas, elegibilidade, processamento, armazenamento e cashout.
Registre URL e data. Não recicle os preços históricos do projeto como preços atuais.

Para preços, prefira transações realizadas e verificáveis, com identificação completa,
data, moeda e frete. Separe leilão, preço fixo e oferta aceita de valor desconhecido.
Agregadores como PriceCharting podem apoiar a análise: identifique-os como agregadores,
verifique correspondência e não conte uma venda agregada e sua origem duas vezes.
Collectr e Double Holo servem como inventário/contexto; preço estimado não é venda confirmada.
Se faltar acesso ou evidência, sinalize a lacuna e não fabrique números.

## 4. Probabilidades de grading

Reporte gem rate específico por carta e empresa, numerador, denominador e data.
População publicada não é amostra aleatória das cartas RAW: seleção prévia, reenvios e
alterações de rótulo podem distorcer a taxa. Não a trate como probabilidade individual.
Não use gem rate PSA para CGC nem Gem Mint para prever Pristine.

Use distribuição de notas incluindo resultados inferiores, rejeição/não graduada e
custos correspondentes quando aplicáveis. Probabilidades devem somar 1.
Pré-screen por cópia deve documentar centralização, cantos, bordas e superfície.
Sem inspeção, a recomendação de grading é condicional. Ajustes de probabilidade precisam
de justificativa e análise de sensibilidade, não de desconto arbitrário fixo.

## 5. Modelo econômico

Explicite moeda e câmbio com fonte/data. Taxas e custos desconhecidos ficam ausentes,
nunca silenciosamente iguais a zero. Separe custos por carta e por lote.

Para cada rota, calcule o fluxo líquido de cada resultado possível, descontando cada
custo uma única vez. Informe sobre qual base incidem venda, cashout e demais percentuais.
Contabilize custos de entrada, grading, sobretaxas, seguro, retorno, venda, armazenamento
e logística aplicáveis. Tributação deve ficar como hipótese identificada até validação.

Calcule:
- líquido RAW como alternativa de referência;
- valor esperado líquido de cada rota;
- ganho incremental = valor esperado líquido da rota menos líquido RAW;
- capital adicional necessário e ROI incremental com denominador explícito;
- lucro total versus custo histórico, separadamente, quando esse custo for conhecido;
- prazo até recebimento, liquidez e custo de oportunidade;
- preço de equilíbrio, sensibilidade à nota/preço/prazo e probabilidade de perda somente
  quando as distribuições necessárias estiverem fundamentadas.

Mostre cenários conservador, base e favorável com premissas identificadas. Não atribua
valorização futura por padrão. Empates ou diferenças menores que a incerteza devem
continuar inconclusivos.

## 6. Carteira e saída operacional

Respeite orçamento, prazo, risco e preferência de retenção definidos pelo usuário.
Regras de lote mínimo são restrições de custo, não motivo para incluir cartas com
retorno incremental desfavorável. Não aloque mais cópias do que há em estoque.

Entregue uma tabela por carta/cópia com identidade, quantidade, condição, preços por
nota, evidência, gem rate, custos, líquido RAW, EV, ganho incremental, capital adicional,
prazo, rota, motivo, pendência e data da próxima revisão.
Use REVIEW_DATA para insuficiência de dados e HOLD para retenção deliberada: não os confunda.
Uma soma por destinação deve reconciliar o inventário de entrada.

Resultados e inventário ficam privados. Publique no GitHub apenas código, documentação
genérica, testes sintéticos e progresso técnico. Não inclua dados individuais em logs,
artefatos, caches, PRs ou Actions summaries. CI pública executa testes sintéticos até
existir integração privada autorizada para entradas e saídas.

## 7. Entrevista crítica

Aplique a abordagem grill-me: examine dependências entre decisões, resolva fatos com
fontes/código e faça perguntas apenas sobre escolhas do usuário ainda desconhecidas.
Cada pergunta deve explicar o efeito prático e propor uma resposta fundamentada.
Não peça de novo informações presentes no contexto. Não trate a entrevista como concluída
antes de o usuário concordar que os critérios estão claros.

Primeira rodada: objetivo econômico principal, prazo máximo até recebimento e orçamento
adicional para submissões. Depois: tolerância de perda, regras de pré-screen, mínimos de
evidência e destino privado das análises. Valores permanecem pendentes até resposta.
