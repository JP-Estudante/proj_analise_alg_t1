import argparse
import csv
import os
from random import Random
from statistics import mean

from src.sorting import comb_sort, is_sorted, natural_merge_sort


ALGORITHMS = [
    # Cada item guarda o nome do algoritmo e a funcao que sera executada.
    ("Comb Sort", comb_sort),
    ("Merge Sort Natural", natural_merge_sort),
]


def generate_inputs(size, scenario, repetitions, random_generator):
    # Gera entradas ordenadas para testar o melhor caso de alguns algoritmos.
    if scenario == "ordenado":
        return [list(range(size)) for _ in range(repetitions)]

    # Gera entradas inversas para observar um caso desfavoravel.
    if scenario == "inverso":
        return [list(range(size, 0, -1)) for _ in range(repetitions)]

    # Gera entradas aleatorias usando uma semente fixa para reproducibilidade.
    if scenario == "aleatorio":
        return [
            [random_generator.randint(0, size * 10) for _ in range(size)]
            for _ in range(repetitions)
        ]

    raise ValueError(f"Cenario desconhecido: {scenario}")


def run_single_experiment(algorithm_function, original_values):
    # Copia a entrada para garantir que o algoritmo nao altere o vetor original.
    values = original_values.copy()
    metrics = algorithm_function(values)

    # Verificacao de seguranca: todo resultado do benchmark precisa estar ordenado.
    if not is_sorted(values):
        raise RuntimeError("O algoritmo gerou uma lista fora de ordem.")

    return metrics


def average_metrics(metrics_list):
    # Consolida as repeticoes usando media aritmetica simples.
    return {
        "tempo_medio_seg": mean(metric.time_seconds for metric in metrics_list),
        "comparacoes_medias": mean(metric.comparisons for metric in metrics_list),
        "trocas_medias": mean(metric.swaps for metric in metrics_list),
        "movimentacoes_medias": mean(metric.movements for metric in metrics_list),
    }


def run_benchmark(sizes, repetitions, seed):
    # A semente fixa permite repetir o experimento e obter as mesmas entradas.
    random_generator = Random(seed)
    scenarios = ["ordenado", "inverso", "aleatorio"]
    rows = []

    for size in sizes:
        for scenario in scenarios:
            # As mesmas entradas sao usadas para todos os algoritmos.
            inputs = generate_inputs(size, scenario, repetitions, random_generator)

            for algorithm_name, algorithm_function in ALGORITHMS:
                # Executa todas as repeticoes para o algoritmo atual.
                metrics_list = [
                    run_single_experiment(algorithm_function, values)
                    for values in inputs
                ]
                averages = average_metrics(metrics_list)

                # Guarda uma linha consolidada para o CSV final.
                rows.append(
                    {
                        "algoritmo": algorithm_name,
                        "cenario": scenario,
                        "tamanho": size,
                        "repeticoes": repetitions,
                        **averages,
                    }
                )

                print(
                    f"{algorithm_name:20} | {scenario:9} | n={size:6} | "
                    f"tempo medio={averages['tempo_medio_seg']:.6f}s"
                )

    return rows


def save_csv(rows, output_path):
    # Cria a pasta de saida, se o caminho informado tiver uma pasta.
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    fieldnames = [
        "algoritmo",
        "cenario",
        "tamanho",
        "repeticoes",
        "tempo_medio_seg",
        "comparacoes_medias",
        "trocas_medias",
        "movimentacoes_medias",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        # DictWriter grava o CSV usando os nomes das colunas definidos acima.
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_spreadsheet_chart_csvs(rows, output_dir):
    # Gera arquivos CSV em formato largo, facilitando a importacao em planilhas.
    os.makedirs(output_dir, exist_ok=True)
    scenarios = sorted({row["cenario"] for row in rows})
    algorithms = sorted({row["algoritmo"] for row in rows})

    for scenario in scenarios:
        scenario_rows = [row for row in rows if row["cenario"] == scenario]
        sizes = sorted({row["tamanho"] for row in scenario_rows})
        output_path = os.path.join(output_dir, f"tempo_{scenario}.csv")

        with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
            fieldnames = ["tamanho", *algorithms]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for size in sizes:
                chart_row = {"tamanho": size}
                for algorithm in algorithms:
                    matching_rows = [
                        row
                        for row in scenario_rows
                        if row["tamanho"] == size and row["algoritmo"] == algorithm
                    ]
                    chart_row[algorithm] = (
                        matching_rows[0]["tempo_medio_seg"] if matching_rows else ""
                    )

                writer.writerow(chart_row)

    print(f"CSVs para graficos em planilha salvos em: {output_dir}")


def save_spreadsheet_instructions(output_dir):
    output_path = os.path.join(output_dir, "como_gerar_graficos.txt")
    with open(output_path, "w", encoding="utf-8") as instructions_file:
        instructions_file.write(
            "Como gerar os graficos em uma planilha:\n"
            "1. Abra LibreOffice Calc, Excel ou Google Sheets.\n"
            "2. Importe um dos arquivos tempo_*.csv desta pasta.\n"
            "3. Selecione todas as colunas importadas.\n"
            "4. Insira um grafico de linhas.\n"
            "5. Use a coluna tamanho como eixo X e uma linha para cada algoritmo.\n"
        )


def generate_spreadsheet_chart_files(rows, output_dir):
    save_spreadsheet_chart_csvs(rows, output_dir)
    save_spreadsheet_instructions(output_dir)


def parse_sizes(text):
    # Converte uma string como "100,500,1000" em uma lista de inteiros.
    return [int(value.strip()) for value in text.split(",") if value.strip()]


def main():
    # argparse permite mudar os parametros do benchmark pelo terminal.
    parser = argparse.ArgumentParser(description="Benchmark de algoritmos de ordenacao.")
    parser.add_argument(
        "--sizes",
        default="100,500,1000,2000",
        help="Tamanhos separados por virgula. Exemplo: 100,500,1000",
    )
    parser.add_argument(
        "--repetitions",
        type=int,
        default=10,
        help="Quantidade de repeticoes por tamanho e cenario.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Semente usada para tornar os testes aleatorios reproduziveis.",
    )
    parser.add_argument(
        "--output",
        default=os.path.join("resultados", "resultados.csv"),
        help="Caminho do arquivo CSV de saida.",
    )
    parser.add_argument(
        "--spreadsheet-dir",
        default=os.path.join("resultados", "planilha"),
        help="Pasta onde serao salvos os CSVs prontos para graficos em planilha.",
    )

    args = parser.parse_args()

    # Executa o fluxo principal: ler tamanhos, rodar benchmark, salvar resultados.
    sizes = parse_sizes(args.sizes)
    rows = run_benchmark(sizes, args.repetitions, args.seed)
    save_csv(rows, args.output)
    generate_spreadsheet_chart_files(rows, args.spreadsheet_dir)

    print(f"Resultados salvos em: {args.output}")


if __name__ == "__main__":
    main()
