# Trabalho 1 - Projeto e Analise de Algoritmos

Este projeto compara dois algoritmos de ordenacao:

- Comb Sort, tratado como algoritmo quadratico.
- Merge Sort Natural, tratado como algoritmo `O(n log n)`.

O codigo foi escrito de forma simples para facilitar a apresentacao e a explicacao em sala.

## Estrutura

- `src/sorting.py`: implementacao dos algoritmos e coleta de metricas.
- `tests.py`: testes simples de corretude.
- `benchmark.py`: execucao dos experimentos e geracao de CSVs para analise.

## Como executar os testes

```bash
python tests.py
```

Saida esperada:

```text
Todos os testes passaram.
```

## Como executar o benchmark

```bash
python benchmark.py
```

Por padrao, o script usa os tamanhos `100,500,1000,2000`, com `10` repeticoes por cenario.
Os resultados completos sao salvos em `resultados/resultados.csv`.

Tambem e possivel escolher os parametros:

```bash
python benchmark.py --sizes 100,500,1000,2000,5000 --repetitions 10 --seed 42
```

## Como gerar graficos em planilha

O benchmark nao depende de biblioteca de graficos. Alem do CSV completo, ele gera arquivos
separados por cenario em `resultados/planilha`:

- `tempo_aleatorio.csv`
- `tempo_inverso.csv`
- `tempo_ordenado.csv`

Cada arquivo ja fica em formato adequado para importar no LibreOffice Calc, Excel ou
Google Sheets. Para montar o grafico:

1. Importe um dos arquivos `tempo_*.csv`.
2. Selecione todas as colunas importadas.
3. Insira um grafico de linhas.
4. Use `tamanho` como eixo X e uma linha para cada algoritmo.

## Cenarios testados

- Vetor ordenado.
- Vetor inversamente ordenado.
- Vetor aleatorio.

Para garantir comparacao justa, o mesmo conjunto de entradas e usado para os dois algoritmos.

## Metricas coletadas

- Tempo medio de execucao.
- Numero medio de comparacoes.
- Numero medio de trocas.
- Numero medio de movimentacoes.

No Comb Sort, uma troca conta como 1 troca e 3 movimentacoes. No Merge Sort Natural,
as movimentacoes representam copias de elementos durante a formacao das sequencias naturais
e durante as intercalacoes.
