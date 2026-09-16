import numpy as np

# Problema da Mochila (Blindagem de Ativos)
weights = np.array([12, 2, 1, 4, 1])
values = np.array([4, 2, 1, 10, 2])
max_weight = 15

pop_size = 10
num_genes = len(weights)
generations = 10
mutation_rate = 0.1

# Inicialização da População
population = np.random.randint(
    0, 2,
    size=(pop_size, num_genes)
)


def calculate_fitness(ind):
    total_weight = np.sum(ind * weights)
    total_value = np.sum(ind * values)

    # Penalização dos indivíduos que ultrapassam a capacidade
    if total_weight > max_weight:
        return 0

    return total_value


def tournament_selection(pop, fitnesses):
    # Seleciona 2 indivíduos aleatoriamente
    indices = np.random.choice(
        len(pop),
        2,
        replace=False
    )

    # Escolhe o indivíduo com maior fitness
    winner = indices[np.argmax(fitnesses[indices])]

    return pop[winner].copy()


def crossover(parent1, parent2):
    point = np.random.randint(1, num_genes)

    child1 = np.concatenate([
        parent1[:point],
        parent2[point:]
    ])

    child2 = np.concatenate([
        parent2[:point],
        parent1[point:]
    ])

    return child1, child2


def mutate(ind):
    for i in range(num_genes):
        if np.random.rand() < mutation_rate:
            ind[i] = 1 - ind[i]

    return ind


# Loop Evolutivo
for g in range(generations):

    fitnesses = np.array([
        calculate_fitness(ind)
        for ind in population
    ])

    new_population = []

    for _ in range(pop_size // 2):

        p1 = tournament_selection(
            population,
            fitnesses
        )

        p2 = tournament_selection(
            population,
            fitnesses
        )

        c1, c2 = crossover(p1, p2)

        new_population.extend([
            mutate(c1),
            mutate(c2)
        ])

    population = np.array(new_population)

# Avaliação final
fitnesses = np.array([
    calculate_fitness(ind)
    for ind in population
])

best_index = np.argmax(fitnesses)
best_individual = population[best_index]

best_weight = np.sum(
    best_individual * weights
)

best_value = np.sum(
    best_individual * values
)

print("[LAB 02] Melhor indivíduo:", best_individual)
print("[LAB 02] Peso:", best_weight)
print("[LAB 02] Valor:", best_value)
print("[LAB 02] Fitness:", fitnesses[best_index])
