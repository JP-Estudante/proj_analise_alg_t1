# Trabalho 1 - Projeto e Analise de Algoritmos

Este projeto compara dois algoritmos de ordenacao:

- Comb Sort, tratado como algoritmo quadratico.
- Merge Sort Natural, tratado como algoritmo `O(n log n)`.

O codigo foi escrito de forma simples para facilitar a apresentacao e a explicacao em sala.

## Estrutura

- `src/sorting.py`: implementacao dos algoritmos e coleta de metricas.
- `tests.py`: testes simples de corretude.
- `benchmark.py`: execucao dos experimentos e geracao de CSV/graficos.
- `docs/relatorio_base.md`: texto base para o relatorio tecnico.

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
Os resultados sao salvos em `resultados/resultados.csv`.

Tambem e possivel escolher os parametros:

```bash
python benchmark.py --sizes 100,500,1000,2000,5000 --repetitions 10 --seed 42
```

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
