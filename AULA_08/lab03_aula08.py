Cenário:
Conectar 10 switches de rede em uma topologia em árvore geradora que minimize a latência total acumulada entre os pares mais críticos, respeitando a matriz de latências físicas de cabeamento D (10x10).

Requisitos do Código:
- Implementar do zero o algoritmo de Colônia de Formigas (ACO) adaptado para seleção de arestas em grafos.
- Incluir verificação de ciclos/conectividade ao longo da construção da rota das formigas para garantir que a solução final forme um grafo/árvore válido.
- Atualização da matriz de feromônio tau_ij com taxa de evaporação rho = 0.2 aplicada apenas às melhores topologias da iteração.

Artefatos e Testes:
- Imprimir a Matriz de Adjacência final (10x10) do grafo de rede otimizado pelo ACO.
- Apresentar o ganho percentual de redução de latência obtido pelo ACO em relação a uma topologia gerada de forma aleatória.

                                                                                                                                                                                                  import random
# ============================================================
# LAB 03 — ACO PARA PROJETO DE TOPOLOGIA DE REDE
# Baixa Latência entre 10 Switches
# ============================================================

import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. MATRIZ DE LATÊNCIAS
# ============================================================

# IMPORTANTE:
# Esta é uma matriz de exemplo.
#
# Se o professor forneceu uma matriz D 10x10 específica,
# substitua SOMENTE esta matriz pelos valores fornecidos.

D = np.array([

    [0,  4,  8,  15, 20, 12, 18, 25, 30, 22],

    [4,  0,  6,  11, 16, 10, 14, 21, 27, 19],

    [8,  6,  0,  7,  13,  9, 12, 18, 24, 16],

    [15, 11,  7,  0,  8,  6, 10, 15, 20, 13],

    [20, 16, 13,  8,  0,  5,  9, 14, 18, 11],

    [12, 10,  9,  6,  5,  0,  7, 12, 17, 10],

    [18, 14, 12, 10,  9,  7,  0,  8, 13,  6],

    [25, 21, 18, 15, 14, 12,  8,  0,  9,  7],

    [30, 27, 24, 20, 18, 17, 13,  9,  0, 11],

    [22, 19, 16, 13, 11, 10,  6,  7, 11,  0]

], dtype=float)


# ============================================================
# 2. CONFIGURAÇÕES DO ACO
# ============================================================

NUM_SWITCHES = 10

NUM_ANTS = 30

NUM_ITERATIONS = 100

# Importância do feromônio
ALPHA = 1.0

# Importância da informação heurística
BETA = 3.0

# Taxa de evaporação
RHO = 0.2

# Quantidade de feromônio depositada
Q = 100.0

# Número de melhores formigas que depositarão feromônio
NUM_ELITE_ANTS = 5

# Semente para resultados reproduzíveis
SEED = 42


# ============================================================
# 3. VALIDAÇÃO DA MATRIZ
# ============================================================

def validate_matrix(D):

    # Verifica tamanho
    if D.shape != (
        NUM_SWITCHES,
        NUM_SWITCHES
    ):

        raise ValueError(
            "A matriz D deve ser 10x10."
        )

    # Verifica simetria
    if not np.allclose(
        D,
        D.T
    ):

        raise ValueError(
            "A matriz D deve ser simétrica."
        )

    # Diagonal deve ser zero
    if not np.all(
        np.diag(D) == 0
    ):

        raise ValueError(
            "A diagonal da matriz D deve ser zero."
        )

    # Todas as latências devem ser >= 0
    if np.any(D < 0):

        raise ValueError(
            "Latências não podem ser negativas."
        )

    print(
        "Matriz D validada com sucesso."
    )


validate_matrix(D)


# ============================================================
# 4. UNION-FIND
# ============================================================

class UnionFind:

    """
    Estrutura utilizada para verificar ciclos
    durante a construção da árvore.

    Cada switch pertence inicialmente a um conjunto.

    Quando adicionamos uma aresta entre dois switches,
    unimos os conjuntos.

    Se os dois switches já pertencem ao mesmo conjunto,
    adicionar essa aresta criaria um ciclo.
    """

    def __init__(self, n):

        self.parent = list(
            range(n)
        )

        self.rank = [
            0
            for _ in range(n)
        ]


    def find(self, x):

        # Procura o representante do conjunto
        if (
            self.parent[x]
            != x
        ):

            self.parent[x] = (
                self.find(
                    self.parent[x]
                )
            )

        return self.parent[x]


    def union(self, x, y):

        root_x = self.find(x)

        root_y = self.find(y)

        # Já pertencem ao mesmo conjunto
        if root_x == root_y:

            return False

        # União por rank
        if (
            self.rank[root_x]
            <
            self.rank[root_y]
        ):

            self.parent[root_x] = root_y

        elif (
            self.rank[root_x]
            >
            self.rank[root_y]
        ):

            self.parent[root_y] = root_x

        else:

            self.parent[root_y] = root_x

            self.rank[root_x] += 1

        return True


# ============================================================
# 5. ACO
# ============================================================

class ACO:

    def __init__(
        self,
        distance_matrix,
        num_ants=30,
        num_iterations=100,
        alpha=1.0,
        beta=3.0,
        rho=0.2,
        Q=100.0,
        elite_ants=5,
        seed=42
    ):

        # ----------------------------------------------------
        # Semente
        # ----------------------------------------------------

        np.random.seed(seed)

        random.seed(seed)

        # ----------------------------------------------------
        # Dados
        # ----------------------------------------------------

        self.D = distance_matrix

        self.n = len(
            distance_matrix
        )

        self.num_ants = num_ants

        self.num_iterations = (
            num_iterations
        )

        self.alpha = alpha

        self.beta = beta

        self.rho = rho

        self.Q = Q

        self.elite_ants = elite_ants

        # ----------------------------------------------------
        # Inicialização do feromônio
        # ----------------------------------------------------

        self.tau = np.ones(
            (
                self.n,
                self.n
            ),
            dtype=float
        )

        # Não utilizamos feromônio
        # em uma ligação de um switch
        # com ele mesmo.

        np.fill_diagonal(
            self.tau,
            0
        )

        # ----------------------------------------------------
        # Informação heurística
        # ----------------------------------------------------

        # Quanto menor a latência,
        # maior a atratividade.

        self.eta = np.zeros_like(
            self.D,
            dtype=float
        )

        for i in range(self.n):

            for j in range(self.n):

                if (
                    i != j
                    and
                    self.D[i, j] > 0
                ):

                    self.eta[i, j] = (
                        1.0
                        /
                        self.D[i, j]
                    )

        # ----------------------------------------------------
        # Melhor solução global
        # ----------------------------------------------------

        self.global_best_edges = None

        self.global_best_cost = (
            float("inf")
        )

        # Histórico
        self.history = []


    # ========================================================
    # 6. VERIFICAR SE UMA ARESTA CRIA CICLO
    # ========================================================

    def creates_cycle(
        self,
        edges,
        u,
        v
    ):

        """
        Retorna True se adicionar a aresta
        (u, v) criaria um ciclo.
        """

        uf = UnionFind(
            self.n
        )

        # Reconstrói os conjuntos
        # das arestas já existentes

        for a, b in edges:

            uf.union(
                a,
                b
            )

        # Se já estão conectados,
        # a nova aresta cria ciclo.

        if (
            uf.find(u)
            ==
            uf.find(v)
        ):

            return True

        return False


    # ========================================================
    # 7. VERIFICAR CONECTIVIDADE
    # ========================================================

    def is_connected(
        self,
        edges
    ):

        """
        Uma árvore com N vértices deve possuir N-1 arestas
        e ser conectada.
        """

        if len(edges) != (
            self.n - 1
        ):

            return False

        uf = UnionFind(
            self.n
        )

        for u, v in edges:

            if not uf.union(
                u,
                v
            ):

                # Criaria ciclo
                return False

        # Todos devem possuir
        # o mesmo representante.

        root = uf.find(0)

        for node in range(
            1,
            self.n
        ):

            if (
                uf.find(node)
                != root
            ):

                return False

        return True


    # ========================================================
    # 8. CALCULAR CUSTO DA TOPOLOGIA
    # ========================================================

    def calculate_cost(
        self,
        edges
    ):

        """
        Neste modelo, o custo da árvore é a soma
        das latências das arestas utilizadas.

        Exemplo:

        (0,1) = 4
        (1,2) = 6
        (2,3) = 7

        custo = 4 + 6 + 7
        """

        cost = 0.0

        for u, v in edges:

            cost += self.D[
                u,
                v
            ]

        return cost


    # ========================================================
    # 9. ESCOLHER PRÓXIMA ARESTA
    # ========================================================

    def choose_edge(
        self,
        edges
    ):

        """
        Escolhe uma nova aresta usando:

        probabilidade ∝
            feromônio^alpha
            *
            heurística^beta

        Apenas arestas que NÃO criam ciclos
        são consideradas.
        """

        candidates = []

        probabilities = []

        # Verifica todos os pares
        # possíveis de switches.

        for i in range(self.n):

            for j in range(
                i + 1,
                self.n
            ):

                # Ignora latência inexistente
                if self.D[i, j] <= 0:

                    continue

                # Ignora se já existe
                # a mesma aresta

                if (
                    (i, j) in edges
                    or
                    (j, i) in edges
                ):

                    continue

                # Não pode criar ciclo

                if self.creates_cycle(
                    edges,
                    i,
                    j
                ):

                    continue

                # ------------------------------------------------
                # Regra do ACO
                # ------------------------------------------------

                pheromone = (
                    self.tau[i, j]
                    **
                    self.alpha
                )

                heuristic = (
                    self.eta[i, j]
                    **
                    self.beta
                )

                probability = (
                    pheromone
                    *
                    heuristic
                )

                candidates.append(
                    (i, j)
                )

                probabilities.append(
                    probability
                )

        # Se não há candidatos,
        # não conseguimos continuar.

        if len(candidates) == 0:

            return None

        probabilities = np.array(
            probabilities
        )

        # Normalização das probabilidades

        total = np.sum(
            probabilities
        )

        if total <= 0:

            probabilities = (
                np.ones(
                    len(candidates)
                )
                /
                len(candidates)
            )

        else:

            probabilities /= total

        # Escolhe uma aresta
        # de acordo com a distribuição

        selected_index = np.random.choice(
            len(candidates),
            p=probabilities
        )

        return candidates[
            selected_index
        ]


    # ========================================================
    # 10. CONSTRUIR UMA ÁRVORE
    # ========================================================

    def construct_solution(self):

        """
        Constrói uma árvore com N-1 arestas.

        A cada passo:

        1. Seleciona uma aresta;
        2. verifica ciclo;
        3. adiciona a aresta;
        4. continua até conectar todos os switches.
        """

        edges = []

        # Uma árvore com N switches
        # possui N-1 arestas.

        while len(edges) < (
            self.n - 1
        ):

            edge = self.choose_edge(
                edges
            )

            if edge is None:

                return None

            edges.append(
                edge
            )

        # Validação final

        if not self.is_connected(
            edges
        ):

            return None

        return edges


    # ========================================================
    # 11. ATUALIZAÇÃO DOS FEROMÔNIOS
    # ========================================================

    def update_pheromone(
        self,
        solutions
    ):

        """
        Evaporação:

            tau = (1-rho) * tau

        Depois apenas as melhores formigas
        depositam feromônio.

        Isso atende ao requisito:

        "evaporação rho = 0.2 aplicada apenas
        às melhores topologias da iteração."
        """

        # ----------------------------------------------------
        # Ordena soluções pelo custo
        # menor custo = melhor
        # ----------------------------------------------------

        solutions.sort(
            key=lambda x: x[1]
        )

        # Melhores soluções da iteração

        elite = solutions[
            :self.elite_ants
        ]

        # ----------------------------------------------------
        # Evaporação
        # ----------------------------------------------------

        # Evapora apenas nas arestas
        # pertencentes às melhores topologias.

        for edges, cost in elite:

            for u, v in edges:

                self.tau[u, v] *= (
                    1 - self.rho
                )

                self.tau[v, u] = (
                    self.tau[u, v]
                )

        # ----------------------------------------------------
        # Depósito de feromônio
        # ----------------------------------------------------

        for edges, cost in elite:

            if cost <= 0:

                continue

            deposit = (
                self.Q / cost
            )

            for u, v in edges:

                self.tau[u, v] += (
                    deposit
                )

                self.tau[v, u] = (
                    self.tau[u, v]
                )


    # ========================================================
    # 12. EXECUTAR O ACO
    # ========================================================

    def run(self):

        for iteration in range(
            self.num_iterations
        ):

            solutions = []

            # ------------------------------------------------
            # Cada formiga constrói uma árvore
            # ------------------------------------------------

            for ant in range(
                self.num_ants
            ):

                edges = (
                    self.construct_solution()
                )

                # Caso a construção falhe
                if edges is None:

                    continue

                cost = (
                    self.calculate_cost(
                        edges
                    )
                )

                solutions.append(
                    (
                        edges,
                        cost
                    )
                )

                # ------------------------------------------------
                # Melhor solução global
                # ------------------------------------------------

                if cost < (
                    self.global_best_cost
                ):

                    self.global_best_cost = (
                        cost
                    )

                    self.global_best_edges = (
                        edges.copy()
                    )

            # ------------------------------------------------
            # Atualização dos feromônios
            # ------------------------------------------------

            if len(solutions) > 0:

                self.update_pheromone(
                    solutions
                )

            # Guarda histórico

            self.history.append(
                self.global_best_cost
            )

        return (
            self.global_best_edges,
            self.global_best_cost,
            self.history
        )


# ============================================================
# 13. CONVERTER ARESTAS PARA MATRIZ DE ADJACÊNCIA
# ============================================================

def edges_to_adjacency(
    edges,
    n
):

    adjacency = np.zeros(
        (
            n,
            n
        ),
        dtype=int
    )

    for u, v in edges:

        adjacency[u, v] = 1

        adjacency[v, u] = 1

    return adjacency


# ============================================================
# 14. TOPOLOGIA ALEATÓRIA
# ============================================================

def random_tree(
    n,
    D
):

    """
    Gera uma árvore aleatória válida.

    A árvore é construída escolhendo arestas aleatórias
    que não criam ciclos.
    """

    edges = []

    uf = UnionFind(
        n
    )

    # Todas as arestas possíveis

    possible_edges = []

    for i in range(n):

        for j in range(
            i + 1,
            n
        ):

            if D[i, j] > 0:

                possible_edges.append(
                    (i, j)
                )

    # Embaralha
    random.shuffle(
        possible_edges
    )

    # Adiciona arestas enquanto
    # não formar ciclo

    for u, v in possible_edges:

        if uf.union(
            u,
            v
        ):

            edges.append(
                (u, v)
            )

        if len(edges) == (
            n - 1
        ):

            break

    return edges


# ============================================================
# 15. EXECUTAR O ACO
# ============================================================

print("\n")
print("=" * 70)
print("EXECUTANDO ACO")
print("=" * 70)

aco = ACO(
    distance_matrix=D,
    num_ants=NUM_ANTS,
    num_iterations=NUM_ITERATIONS,
    alpha=ALPHA,
    beta=BETA,
    rho=RHO,
    Q=Q,
    elite_ants=NUM_ELITE_ANTS,
    seed=SEED
)

(
    best_edges,
    best_cost,
    history
) = aco.run()


# ============================================================
# 16. VALIDAR A ÁRVORE FINAL
# ============================================================

valid_tree = (
    aco.is_connected(
        best_edges
    )
)


print("\n")
print("=" * 70)
print("VALIDAÇÃO DA SOLUÇÃO ACO")
print("=" * 70)

print(
    f"Número de switches: "
    f"{NUM_SWITCHES}"
)

print(
    f"Número de arestas: "
    f"{len(best_edges)}"
)

print(
    f"Esperado para árvore: "
    f"{NUM_SWITCHES - 1}"
)

print(
    f"Árvore válida: "
    f"{'SIM' if valid_tree else 'NÃO'}"
)


# ============================================================
# 17. MOSTRAR ARESTAS DA MELHOR TOPOLOGIA
# ============================================================

print("\n")
print("=" * 70)
print("MELHOR TOPOLOGIA ENCONTRADA PELO ACO")
print("=" * 70)

for u, v in best_edges:

    print(
        f"Switch {u + 1} "
        f"<--> "
        f"Switch {v + 1} "
        f"| Latência = "
        f"{D[u, v]:.2f}"
    )

print(
    f"\nLatência total ACO: "
    f"{best_cost:.2f}"
)


# ============================================================
# 18. MATRIZ DE ADJACÊNCIA FINAL
# ============================================================

adjacency_aco = (
    edges_to_adjacency(
        best_edges,
        NUM_SWITCHES
    )
)

print("\n")
print("=" * 70)
print("MATRIZ DE ADJACÊNCIA FINAL — ACO")
print("=" * 70)

print(
    adjacency_aco
)


# Também apresenta como DataFrame
labels = [
    f"S{i + 1}"
    for i in range(
        NUM_SWITCHES
    )
]

adjacency_df = pd.DataFrame(
    adjacency_aco,
    index=labels,
    columns=labels
)

print("\nMatriz de adjacência formatada:")

display(
    adjacency_df
)


# ============================================================
# 19. GERAR TOPOLOGIA ALEATÓRIA
# ============================================================

random_edges = random_tree(
    NUM_SWITCHES,
    D
)

random_cost = 0.0

for u, v in random_edges:

    random_cost += D[u, v]


# ============================================================
# 20. MATRIZ DE ADJACÊNCIA DA TOPOLOGIA ALEATÓRIA
# ============================================================

adjacency_random = (
    edges_to_adjacency(
        random_edges,
        NUM_SWITCHES
    )
)


# ============================================================
# 21. CALCULAR GANHO PERCENTUAL
# ============================================================

gain_percentage = (
    (
        random_cost
        -
        best_cost
    )
    /
    random_cost
) * 100


# ============================================================
# 22. RESULTADO DA COMPARAÇÃO
# ============================================================

print("\n")
print("=" * 70)
print("COMPARAÇÃO ACO x TOPOLOGIA ALEATÓRIA")
print("=" * 70)

print(
    f"Latência da topologia aleatória: "
    f"{random_cost:.2f}"
)

print(
    f"Latência da topologia ACO: "
    f"{best_cost:.2f}"
)

print(
    f"Ganho percentual de redução: "
    f"{gain_percentage:.2f}%"
)


# ============================================================
# 23. MATRIZ DA TOPOLOGIA ALEATÓRIA
# ============================================================

print("\n")
print("=" * 70)
print("MATRIZ DE ADJACÊNCIA — TOPOLOGIA ALEATÓRIA")
print("=" * 70)

random_df = pd.DataFrame(
    adjacency_random,
    index=labels,
    columns=labels
)

display(
    random_df
)


# ============================================================
# 24. GRÁFICO DA CONVERGÊNCIA DO ACO
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    range(
        1,
        NUM_ITERATIONS + 1
    ),
    history,
    color="blue",
    linewidth=2
)

plt.xlabel(
    "Iteração"
)

plt.ylabel(
    "Melhor Latência"
)

plt.title(
    "Convergência do ACO"
)

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.show()


# ============================================================
# 25. TABELA DE COMPARAÇÃO
# ============================================================

comparison_table = pd.DataFrame({

    "Topologia": [
        "Aleatória",
        "ACO"
    ],

    "Número de Arestas": [
        len(random_edges),
        len(best_edges)
    ],

    "Latência Total": [
        random_cost,
        best_cost
    ]
})


print("\n")
print("=" * 70)
print("TABELA COMPARATIVA")
print("=" * 70)

display(
    comparison_table.round(4)
)


# ============================================================
# 26. RESUMO FINAL
# ============================================================

print("\n")
print("=" * 70)
print("RESUMO FINAL DO LAB 03")
print("=" * 70)

print(
    f"\nLatência aleatória: "
    f"{random_cost:.2f}"
)

print(
    f"Latência ACO: "
    f"{best_cost:.2f}"
)

print(
    f"Redução obtida: "
    f"{gain_percentage:.2f}%"
)

print(
    f"\nQuantidade de arestas: "
    f"{len(best_edges)}"
)

print(
    f"Árvore válida: "
    f"{('SIM' if valid_tree else 'NÃO')}"
)

print(
    "\nMatriz de adjacência ACO:"
)

print(
    adjacency_aco
)

print("\n")
print("=" * 70)
print("EXECUÇÃO CONCLUÍDA")
print("=" * 70)

if __name__ == "__main__":
    executar_experimento()
