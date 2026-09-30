Cenário:
Um nó de Edge Computing precisa selecionar um subconjunto de 15 microsserviços disponíveis para manter em memória.
Cada serviço possui um Valor de Negócio, um Consumo de RAM (GB) e um Consumo de CPU (Cores).
O objetivo é maximizar o Valor de Negócio acumulado respeitando as restrições simultâneas de capacidade: máximo de 16 GB de RAM e máximo de 8 cores de CPU.

Requisitos do Código:
- Implementar do zero um Algoritmo Genético Binário (1 = serviço carregado, 0 = não carregado).
- Criar e comparar duas estratégias de avaliação de fitness:
  1. Estratégia A (Penalidade Rígida): Indivíduos que violarem qualquer limite (RAM ou CPU) recebem fitness = 0.
  2. Estratégia B (Penalidade Proporcional): O fitness é reduzido proporcionalmente à quantidade de RAM/CPU excedida.
- Operadores de Seleção por Torneio, Crossover de Ponto Único e Mutação Binária.

Artefatos e Testes:
- Comparar a média e o desvio-padrão do fitness ao longo das gerações entre a Estratégia A e a Estratégia B.
- Demonstrar no relatório qual das duas estratégias preservou melhor a diversidade genética da população e qual encontrou a melhor combinação final de microsserviços.

"""
LAB 02 - Algoritmo Genético Binário para seleção de microsserviços.

Estratégias:
A) Penalidade rígida:
   qualquer violação => fitness = 0

B) Penalidade proporcional:
   reduz o valor proporcionalmente aos excessos de RAM e CPU.
"""

# ============================================================
# LAB 02 — ALGORITMO GENÉTICO BINÁRIO
# Seleção de Microsserviços em Edge Computing
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. DADOS DOS 15 MICROSSERVIÇOS
# ============================================================

# Cada serviço possui:
# - Valor de negócio
# - Consumo de RAM em GB
# - Consumo de CPU em cores

servicos = pd.DataFrame({

    "Servico": [
        "Servico_01",
        "Servico_02",
        "Servico_03",
        "Servico_04",
        "Servico_05",
        "Servico_06",
        "Servico_07",
        "Servico_08",
        "Servico_09",
        "Servico_10",
        "Servico_11",
        "Servico_12",
        "Servico_13",
        "Servico_14",
        "Servico_15"
    ],

    "Valor": [
        90, 70, 120, 60, 100,
        80, 110, 50, 95, 75,
        130, 65, 105, 85, 115
    ],

    "RAM": [
        4.0, 2.0, 5.0, 1.5, 3.0,
        2.5, 4.5, 1.0, 3.5, 2.0,
        5.5, 1.5, 4.0, 2.5, 3.0
    ],

    "CPU": [
        2.0, 1.0, 3.0, 1.0, 2.0,
        1.5, 2.5, 0.5, 2.0, 1.0,
        3.0, 1.0, 2.5, 1.5, 2.0
    ]
})


# ============================================================
# 2. RESTRIÇÕES DO PROBLEMA
# ============================================================

MAX_RAM = 16.0
MAX_CPU = 8.0

NUM_SERVICOS = 15


# ============================================================
# 3. PARÂMETROS DO ALGORITMO GENÉTICO
# ============================================================

POPULATION_SIZE = 50

NUM_GENERATIONS = 100

TOURNAMENT_SIZE = 3

CROSSOVER_RATE = 0.80

MUTATION_RATE = 0.05


# ============================================================
# 4. CLASSE DO ALGORITMO GENÉTICO
# ============================================================

class GeneticAlgorithm:

    def __init__(
        self,
        strategy,
        population_size=50,
        generations=100,
        tournament_size=3,
        crossover_rate=0.80,
        mutation_rate=0.05,
        seed=42
    ):

        # ----------------------------------------------------
        # Configurações
        # ----------------------------------------------------

        self.strategy = strategy

        self.population_size = population_size

        self.generations = generations

        self.tournament_size = tournament_size

        self.crossover_rate = crossover_rate

        self.mutation_rate = mutation_rate

        # Semente para reprodução dos resultados
        self.seed = seed

        np.random.seed(seed)

        # ----------------------------------------------------
        # Histórico
        # ----------------------------------------------------

        self.history_mean = []

        self.history_std = []

        self.history_best = []

        self.history_diversity = []

        # Melhor indivíduo encontrado
        self.best_individual = None

        self.best_fitness = -np.inf


    # ========================================================
    # 5. CRIAÇÃO DA POPULAÇÃO INICIAL
    # ========================================================

    def create_population(self):

        """
        Cria uma população de indivíduos binários.

        Exemplo:

        [1, 0, 1, 1, 0, ...]

        1 = serviço selecionado
        0 = serviço não selecionado
        """

        population = np.random.randint(
            0,
            2,
            size=(
                self.population_size,
                NUM_SERVICOS
            )
        )

        return population


    # ========================================================
    # 6. AVALIAÇÃO DE UM INDIVÍDUO
    # ========================================================

    def evaluate_individual(self, individual):

        """
        Calcula:

        - Valor total
        - RAM total
        - CPU total
        - Fitness
        """

        # Serviços selecionados
        selected = individual == 1

        # Valor acumulado
        total_value = np.sum(
            servicos.loc[
                selected,
                "Valor"
            ]
        )

        # RAM acumulada
        total_ram = np.sum(
            servicos.loc[
                selected,
                "RAM"
            ]
        )

        # CPU acumulada
        total_cpu = np.sum(
            servicos.loc[
                selected,
                "CPU"
            ]
        )

        # ====================================================
        # ESTRATÉGIA A — PENALIDADE RÍGIDA
        # ====================================================

        if self.strategy == "rigida":

            # Se ultrapassar qualquer limite
            # o fitness será zero.

            if (
                total_ram > MAX_RAM
                or
                total_cpu > MAX_CPU
            ):

                fitness = 0.0

            else:

                fitness = total_value


        # ====================================================
        # ESTRATÉGIA B — PENALIDADE PROPORCIONAL
        # ====================================================

        elif self.strategy == "proporcional":

            # Quanto ultrapassou RAM?
            ram_excesso = max(
                0,
                total_ram - MAX_RAM
            )

            # Quanto ultrapassou CPU?
            cpu_excesso = max(
                0,
                total_cpu - MAX_CPU
            )

            # ------------------------------------------------
            # Penalidade proporcional
            #
            # A penalidade é calculada como uma fração
            # da capacidade ultrapassada.
            # ------------------------------------------------

            ram_ratio = (
                ram_excesso / MAX_RAM
            )

            cpu_ratio = (
                cpu_excesso / MAX_CPU
            )

            total_penalty = (
                ram_ratio
                +
                cpu_ratio
            )

            # Reduz o valor proporcionalmente
            fitness = (
                total_value
                *
                max(
                    0,
                    1 - total_penalty
                )
            )

        else:

            raise ValueError(
                "Estratégia inválida."
            )

        return (
            fitness,
            total_value,
            total_ram,
            total_cpu
        )


    # ========================================================
    # 7. AVALIAR TODA A POPULAÇÃO
    # ========================================================

    def evaluate_population(self, population):

        fitness = []

        values = []

        rams = []

        cpus = []

        for individual in population:

            result = (
                self.evaluate_individual(
                    individual
                )
            )

            fit, value, ram, cpu = result

            fitness.append(fit)

            values.append(value)

            rams.append(ram)

            cpus.append(cpu)

        return (
            np.array(fitness),
            np.array(values),
            np.array(rams),
            np.array(cpus)
        )


    # ========================================================
    # 8. SELEÇÃO POR TORNEIO
    # ========================================================

    def tournament_selection(
        self,
        population,
        fitness
    ):

        """
        Escolhe alguns indivíduos aleatoriamente
        e retorna o melhor deles.

        Exemplo:

        indivíduo A -> fitness 100
        indivíduo B -> fitness 150
        indivíduo C -> fitness 120

        Vencedor = B
        """

        # Escolhe índices aleatórios
        indices = np.random.choice(
            len(population),
            self.tournament_size,
            replace=False
        )

        # Fitness dos participantes
        tournament_fitness = fitness[
            indices
        ]

        # Índice do melhor
        winner_index = indices[
            np.argmax(
                tournament_fitness
            )
        ]

        # Retorna uma cópia
        return population[
            winner_index
        ].copy()


    # ========================================================
    # 9. CROSSOVER DE PONTO ÚNICO
    # ========================================================

    def single_point_crossover(
        self,
        parent1,
        parent2
    ):

        """
        Divide os cromossomos em um ponto.

        Exemplo:

        Pai 1:
        111 | 000111

        Pai 2:
        000 | 111000

        Filho 1:
        111 | 111000

        Filho 2:
        000 | 000111
        """

        # Decide se haverá crossover
        if (
            np.random.rand()
            >
            self.crossover_rate
        ):

            return (
                parent1.copy(),
                parent2.copy()
            )

        # Escolhe ponto de corte
        point = np.random.randint(
            1,
            NUM_SERVICOS
        )

        # Primeiro filho
        child1 = np.concatenate([
            parent1[:point],
            parent2[point:]
        ])

        # Segundo filho
        child2 = np.concatenate([
            parent2[:point],
            parent1[point:]
        ])

        return child1, child2


    # ========================================================
    # 10. MUTAÇÃO BINÁRIA
    # ========================================================

    def mutation(self, individual):

        """
        Cada gene possui uma probabilidade de sofrer mutação.

        0 -> 1
        1 -> 0
        """

        individual = individual.copy()

        for i in range(NUM_SERVICOS):

            if (
                np.random.rand()
                <
                self.mutation_rate
            ):

                # Inverte o bit
                individual[i] = (
                    1 - individual[i]
                )

        return individual


    # ========================================================
    # 11. DIVERSIDADE GENÉTICA
    # ========================================================

    def calculate_diversity(
        self,
        population
    ):

        """
        Mede a diversidade genética através
        da proporção de genes que são diferentes
        da frequência majoritária.

        Valor próximo de 0:
            população muito semelhante.

        Valor maior:
            população mais diversificada.
        """

        # Frequência média de cada gene
        frequencies = np.mean(
            population,
            axis=0
        )

        # Diversidade de cada gene
        gene_diversity = (
            2
            *
            frequencies
            *
            (1 - frequencies)
        )

        # Média da diversidade
        diversity = np.mean(
            gene_diversity
        )

        return diversity


    # ========================================================
    # 12. EXECUÇÃO DO ALGORITMO GENÉTICO
    # ========================================================

    def run(self):

        # Cria população inicial
        population = (
            self.create_population()
        )

        # ----------------------------------------------------
        # Loop das gerações
        # ----------------------------------------------------

        for generation in range(
            self.generations
        ):

            # ================================================
            # AVALIAÇÃO
            # ================================================

            (
                fitness,
                values,
                rams,
                cpus
            ) = self.evaluate_population(
                population
            )

            # ================================================
            # ESTATÍSTICAS
            # ================================================

            mean_fitness = np.mean(
                fitness
            )

            std_fitness = np.std(
                fitness
            )

            best_index = np.argmax(
                fitness
            )

            generation_best = fitness[
                best_index
            ]

            diversity = (
                self.calculate_diversity(
                    population
                )
            )

            # Guarda histórico
            self.history_mean.append(
                mean_fitness
            )

            self.history_std.append(
                std_fitness
            )

            self.history_best.append(
                generation_best
            )

            self.history_diversity.append(
                diversity
            )

            # ================================================
            # ATUALIZA MELHOR GLOBAL
            # ================================================

            if (
                generation_best
                >
                self.best_fitness
            ):

                self.best_fitness = (
                    generation_best
                )

                self.best_individual = (
                    population[
                        best_index
                    ].copy()
                )

            # ================================================
            # NOVA POPULAÇÃO
            # ================================================

            new_population = []

            while (
                len(new_population)
                <
                self.population_size
            ):

                # --------------------------------------------
                # Seleção
                # --------------------------------------------

                parent1 = (
                    self.tournament_selection(
                        population,
                        fitness
                    )
                )

                parent2 = (
                    self.tournament_selection(
                        population,
                        fitness
                    )
                )

                # --------------------------------------------
                # Crossover
                # --------------------------------------------

                child1, child2 = (
                    self.single_point_crossover(
                        parent1,
                        parent2
                    )
                )

                # --------------------------------------------
                # Mutação
                # --------------------------------------------

                child1 = self.mutation(
                    child1
                )

                child2 = self.mutation(
                    child2
                )

                # --------------------------------------------
                # Adiciona filhos
                # --------------------------------------------

                new_population.append(
                    child1
                )

                if (
                    len(new_population)
                    <
                    self.population_size
                ):

                    new_population.append(
                        child2
                    )

            # Atualiza população
            population = np.array(
                new_population
            )

        # ====================================================
        # AVALIAÇÃO FINAL
        # ====================================================

        final_result = (
            self.evaluate_individual(
                self.best_individual
            )
        )

        (
            final_fitness,
            final_value,
            final_ram,
            final_cpu
        ) = final_result

        return {
            "best_individual":
                self.best_individual,

            "best_fitness":
                final_fitness,

            "best_value":
                final_value,

            "best_ram":
                final_ram,

            "best_cpu":
                final_cpu,

            "history_mean":
                self.history_mean,

            "history_std":
                self.history_std,

            "history_best":
                self.history_best,

            "history_diversity":
                self.history_diversity
        }


# ============================================================
# 13. EXECUTAR ESTRATÉGIA A
# ============================================================

print("=" * 70)
print("ESTRATÉGIA A — PENALIDADE RÍGIDA")
print("=" * 70)

ga_rigida = GeneticAlgorithm(
    strategy="rigida",
    population_size=POPULATION_SIZE,
    generations=NUM_GENERATIONS,
    tournament_size=TOURNAMENT_SIZE,
    crossover_rate=CROSSOVER_RATE,
    mutation_rate=MUTATION_RATE,
    seed=42
)

result_rigida = ga_rigida.run()


# ============================================================
# 14. EXECUTAR ESTRATÉGIA B
# ============================================================

print("\n")
print("=" * 70)
print("ESTRATÉGIA B — PENALIDADE PROPORCIONAL")
print("=" * 70)

ga_proporcional = GeneticAlgorithm(
    strategy="proporcional",
    population_size=POPULATION_SIZE,
    generations=NUM_GENERATIONS,
    tournament_size=TOURNAMENT_SIZE,
    crossover_rate=CROSSOVER_RATE,
    mutation_rate=MUTATION_RATE,
    seed=42
)

result_proporcional = (
    ga_proporcional.run()
)


# ============================================================
# 15. FUNÇÃO PARA MOSTRAR RESULTADO
# ============================================================

def mostrar_resultado(
    nome,
    resultado
):

    print("\n")
    print("=" * 70)
    print(nome)
    print("=" * 70)

    individual = (
        resultado["best_individual"]
    )

    print(
        "\nCromossomo:"
    )

    print(
        individual
    )

    print(
        "\nServiços selecionados:"
    )

    selected_indices = np.where(
        individual == 1
    )[0]

    for index in selected_indices:

        print(
            f"  {servicos.iloc[index]['Servico']}"
        )

    print(
        f"\nValor de negócio: "
        f"{resultado['best_value']:.2f}"
    )

    print(
        f"RAM utilizada: "
        f"{resultado['best_ram']:.2f} GB"
    )

    print(
        f"CPU utilizada: "
        f"{resultado['best_cpu']:.2f} cores"
    )

    print(
        f"Fitness: "
        f"{resultado['best_fitness']:.2f}"
    )

    # Verificação das restrições

    ram_ok = (
        resultado["best_ram"]
        <= MAX_RAM
    )

    cpu_ok = (
        resultado["best_cpu"]
        <= MAX_CPU
    )

    print(
        f"\nRAM <= 16 GB: "
        f"{'OK' if ram_ok else 'VIOLADA'}"
    )

    print(
        f"CPU <= 8 cores: "
        f"{'OK' if cpu_ok else 'VIOLADA'}"
    )


# ============================================================
# 16. MOSTRAR RESULTADOS
# ============================================================

mostrar_resultado(
    "ESTRATÉGIA A — PENALIDADE RÍGIDA",
    result_rigida
)

mostrar_resultado(
    "ESTRATÉGIA B — PENALIDADE PROPORCIONAL",
    result_proporcional
)


# ============================================================
# 17. COMPARAÇÃO FINAL
# ============================================================

comparison = pd.DataFrame({

    "Estratégia": [
        "Penalidade Rígida",
        "Penalidade Proporcional"
    ],

    "Fitness Final": [
        result_rigida[
            "best_fitness"
        ],

        result_proporcional[
            "best_fitness"
        ]
    ],

    "Valor de Negócio": [
        result_rigida[
            "best_value"
        ],

        result_proporcional[
            "best_value"
        ]
    ],

    "RAM (GB)": [
        result_rigida[
            "best_ram"
        ],

        result_proporcional[
            "best_ram"
        ]
    ],

    "CPU (Cores)": [
        result_rigida[
            "best_cpu"
        ],

        result_proporcional[
            "best_cpu"
        ]
    ],

    "Diversidade Final": [
        result_rigida[
            "history_diversity"
        ][-1],

        result_proporcional[
            "history_diversity"
        ][-1]
    ]
})


print("\n")
print("=" * 70)
print("COMPARAÇÃO DAS ESTRATÉGIAS")
print("=" * 70)

display(
    comparison.round(4)
)


# ============================================================
# 18. TABELA DOS SERVIÇOS SELECIONADOS
# ============================================================

def tabela_servicos_selecionados(
    individual
):

    indices = np.where(
        individual == 1
    )[0]

    tabela = servicos.iloc[
        indices
    ].copy()

    tabela.reset_index(
        drop=True,
        inplace=True
    )

    return tabela


print("\n")
print("=" * 70)
print("SERVIÇOS — ESTRATÉGIA A")
print("=" * 70)

display(
    tabela_servicos_selecionados(
        result_rigida[
            "best_individual"
        ]
    )
)


print("\n")
print("=" * 70)
print("SERVIÇOS — ESTRATÉGIA B")
print("=" * 70)

display(
    tabela_servicos_selecionados(
        result_proporcional[
            "best_individual"
        ]
    )
)


# ============================================================
# 19. GRÁFICO — MÉDIA DO FITNESS
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    result_rigida[
        "history_mean"
    ],
    label="Penalidade Rígida"
)

plt.plot(
    result_proporcional[
        "history_mean"
    ],
    label="Penalidade Proporcional"
)

plt.xlabel(
    "Geração"
)

plt.ylabel(
    "Fitness Médio"
)

plt.title(
    "Fitness Médio ao Longo das Gerações"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.show()


# ============================================================
# 20. GRÁFICO — DESVIO-PADRÃO
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    result_rigida[
        "history_std"
    ],
    label="Penalidade Rígida"
)

plt.plot(
    result_proporcional[
        "history_std"
    ],
    label="Penalidade Proporcional"
)

plt.xlabel(
    "Geração"
)

plt.ylabel(
    "Desvio-padrão do Fitness"
)

plt.title(
    "Desvio-padrão do Fitness ao Longo das Gerações"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.show()


# ============================================================
# 21. GRÁFICO — MELHOR FITNESS
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    result_rigida[
        "history_best"
    ],
    label="Penalidade Rígida"
)

plt.plot(
    result_proporcional[
        "history_best"
    ],
    label="Penalidade Proporcional"
)

plt.xlabel(
    "Geração"
)

plt.ylabel(
    "Melhor Fitness"
)

plt.title(
    "Melhor Fitness por Geração"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.show()


# ============================================================
# 22. GRÁFICO — DIVERSIDADE GENÉTICA
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    result_rigida[
        "history_diversity"
    ],
    label="Penalidade Rígida"
)

plt.plot(
    result_proporcional[
        "history_diversity"
    ],
    label="Penalidade Proporcional"
)

plt.xlabel(
    "Geração"
)

plt.ylabel(
    "Diversidade Genética"
)

plt.title(
    "Diversidade Genética ao Longo das Gerações"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.show()


# ============================================================
# 23. TABELA COMPLETA DE EVOLUÇÃO
# ============================================================

evolution_table = pd.DataFrame({

    "Geração": np.arange(
        1,
        NUM_GENERATIONS + 1
    ),

    "Média - Rígida":
        result_rigida[
            "history_mean"
        ],

    "Desvio - Rígida":
        result_rigida[
            "history_std"
        ],

    "Melhor - Rígida":
        result_rigida[
            "history_best"
        ],

    "Diversidade - Rígida":
        result_rigida[
            "history_diversity"
        ],

    "Média - Proporcional":
        result_proporcional[
            "history_mean"
        ],

    "Desvio - Proporcional":
        result_proporcional[
            "history_std"
        ],

    "Melhor - Proporcional":
        result_proporcional[
            "history_best"
        ],

    "Diversidade - Proporcional":
        result_proporcional[
            "history_diversity"
        ]
})


print("\n")
print("=" * 70)
print("EVOLUÇÃO DAS ESTRATÉGIAS")
print("=" * 70)

display(
    evolution_table.round(4)
)


# ============================================================
# 24. RESUMO AUTOMÁTICO
# ============================================================

print("\n")
print("=" * 70)
print("RESUMO FINAL")
print("=" * 70)

print(
    "\nESTRATÉGIA A — PENALIDADE RÍGIDA"
)

print(
    f"Fitness final: "
    f"{result_rigida['best_fitness']:.2f}"
)

print(
    f"Valor de negócio: "
    f"{result_rigida['best_value']:.2f}"
)

print(
    f"RAM: "
    f"{result_rigida['best_ram']:.2f} GB"
)

print(
    f"CPU: "
    f"{result_rigida['best_cpu']:.2f} cores"
)

print(
    f"Diversidade final: "
    f"{result_rigida['history_diversity'][-1]:.4f}"
)


print(
    "\nESTRATÉGIA B — PENALIDADE PROPORCIONAL"
)

print(
    f"Fitness final: "
    f"{result_proporcional['best_fitness']:.2f}"
)

print(
    f"Valor de negócio: "
    f"{result_proporcional['best_value']:.2f}"
)

print(
    f"RAM: "
    f"{result_proporcional['best_ram']:.2f} GB"
)

print(
    f"CPU: "
    f"{result_proporcional['best_cpu']:.2f} cores"
)

print(
    f"Diversidade final: "
    f"{result_proporcional['history_diversity'][-1]:.4f}"
)

print("\n")
print("=" * 70)
print("EXECUÇÃO CONCLUÍDA")
print("=" * 70)
