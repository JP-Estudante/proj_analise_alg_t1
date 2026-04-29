from random import Random

from src.sorting import comb_sort, is_sorted, natural_merge_sort


def test_algorithm(sort_function):
    # Casos pequenos e variados para validar situacoes importantes.
    test_cases = [
        [],
        [1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 2, 3, 1],
        [-2, 5, 0, -10, 8],
    ]

    # Gera casos aleatorios fixos para que o teste seja reproduzivel.
    random_generator = Random(123)
    for _ in range(20):
        test_cases.append([random_generator.randint(-100, 100) for _ in range(30)])

    for original in test_cases:
        # Copia a lista para preservar o caso original usado na comparacao.
        values = original.copy()
        metrics = sort_function(values)

        # Compara com o sorted do Python, usado aqui como referencia confiavel.
        assert values == sorted(original)
        assert is_sorted(values)

        # As metricas nao devem assumir valores negativos.
        assert metrics.comparisons >= 0
        assert metrics.swaps >= 0
        assert metrics.movements >= 0
        assert metrics.time_seconds >= 0


def main():
    test_algorithm(comb_sort)
    test_algorithm(natural_merge_sort)
    print("Todos os testes passaram.")


if __name__ == "__main__":
    main()
