# Dados de entrada

Coloque exports pessoais do Collectr em `data/private/`.

Exemplo:

```text
data/private/export.csv
```

Essa pasta é ignorada pelo Git porque pode revelar inventário, quantidades, preços de
aquisição e valor de mercado. O programa deve aceitar o arquivo por caminho; não codifique
dados pessoais no código ou nos testes.
