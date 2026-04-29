from dataclasses import dataclass
from time import perf_counter


@dataclass
class SortMetrics:
    # Estrutura simples para guardar as metricas medidas em cada execucao.
    comparisons: int = 0
    swaps: int = 0
    movements: int = 0
    time_seconds: float = 0.0


def comb_sort(values):
    """Ordena a lista usando Comb Sort e retorna as metricas coletadas."""
    # Inicia as metricas e marca o tempo inicial do algoritmo.
    metrics = SortMetrics()
    start_time = perf_counter()

    # O gap comeca no tamanho da lista e diminui a cada passada.
    n = len(values)
    gap = n
    shrink = 1.3

    # swapped indica se houve alguma troca na ultima passada.
    swapped = True

    # O algoritmo termina quando gap e 1 e nenhuma troca foi feita.
    while gap > 1 or swapped:
        # Reduz o gap usando o fator classico do Comb Sort.
        gap = int(gap / shrink)
        if gap < 1:
            gap = 1

        swapped = False

        # Compara elementos separados pela distancia gap.
        for i in range(0, n - gap):
            metrics.comparisons += 1

            # Se os elementos estiverem fora de ordem, troca os dois.
            if values[i] > values[i + gap]:
                values[i], values[i + gap] = values[i + gap], values[i]
                metrics.swaps += 1

                # Uma troca simples pode ser vista como tres movimentacoes.
                metrics.movements += 3
                swapped = True

    # Registra o tempo total gasto pelo algoritmo.
    metrics.time_seconds = perf_counter() - start_time
    return metrics


def natural_merge_sort(values):
    """Ordena a lista usando Merge Sort Natural e retorna as metricas coletadas."""
    # Inicia as metricas e marca o tempo inicial do algoritmo.
    metrics = SortMetrics()
    start_time = perf_counter()

    # Listas vazias ou com um elemento ja estao ordenadas.
    if len(values) <= 1:
        metrics.time_seconds = perf_counter() - start_time
        return metrics

    # Primeiro passo: encontrar trechos que ja estao em ordem crescente.
    runs = _find_natural_runs(values, metrics)

    # Enquanto existir mais de uma run, intercala pares de runs.
    while len(runs) > 1:
        merged_runs = []

        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                # Junta duas runs ordenadas em uma nova run ordenada.
                merged_runs.append(_merge(runs[i], runs[i + 1], metrics))
            else:
                # Se sobrar uma run sem par, ela passa para a proxima rodada.
                merged_runs.append(runs[i])

        runs = merged_runs

    # Copia o resultado final de volta para a lista original.
    values[:] = runs[0]
    metrics.movements += len(values)

    # Registra o tempo total gasto pelo algoritmo.
    metrics.time_seconds = perf_counter() - start_time
    return metrics


def _find_natural_runs(values, metrics):
    """Separa a lista em sequencias que ja estao em ordem crescente."""
    runs = []

    # A primeira run sempre comeca com o primeiro elemento da lista.
    current_run = [values[0]]
    metrics.movements += 1

    for i in range(1, len(values)):
        # Compara o elemento atual com o anterior para saber se a run continua.
        metrics.comparisons += 1

        if values[i - 1] <= values[i]:
            # Se continua crescente, adiciona o elemento na run atual.
            current_run.append(values[i])
        else:
            # Se quebrou a ordem, fecha a run atual e inicia outra.
            runs.append(current_run)
            current_run = [values[i]]

        metrics.movements += 1

    # Adiciona a ultima run encontrada.
    runs.append(current_run)
    return runs


def _merge(left, right, metrics):
    """Intercala duas listas ordenadas."""
    result = []

    # i percorre a lista da esquerda; j percorre a lista da direita.
    i = 0
    j = 0

    # Enquanto as duas listas possuem elementos, escolhe o menor da frente.
    while i < len(left) and j < len(right):
        metrics.comparisons += 1

        if left[i] <= right[j]:
            # O menor elemento da esquerda e copiado para o resultado.
            result.append(left[i])
            i += 1
        else:
            # O menor elemento da direita e copiado para o resultado.
            result.append(right[j])
            j += 1

        metrics.movements += 1

    # Copia o restante da esquerda, caso ainda exista.
    while i < len(left):
        result.append(left[i])
        i += 1
        metrics.movements += 1

    # Copia o restante da direita, caso ainda exista.
    while j < len(right):
        result.append(right[j])
        j += 1
        metrics.movements += 1

    return result


def is_sorted(values):
    """Retorna True se a lista estiver em ordem crescente."""
    for i in range(1, len(values)):
        # Se algum par vizinho estiver invertido, a lista nao esta ordenada.
        if values[i - 1] > values[i]:
            return False
    return True
