Cenário:
Redirecionamento dinâmico de tráfego web entre 6 zonas de disponibilidade (AZs).
O sistema deve encontrar o vetor de pesos contínuos W = [w1, w2, w3, w4, w5, w6] (com sum(wi) = 1.0) para minimizar a temperatura média ponderada dos racks, 
sabendo que cada AZ possui um coeficiente de aquecimento específico C = [42.0, 35.0, 58.0, 30.0, 50.0, 65.0] °C.

Requisitos do Código:
- Implementar do zero a classe/estrutura do PSO Contínuo (com atualização de velocidade, posição e histórico de P_best e G_best).
- Aplicar um operador de normalização no vetor de posições das partículas a cada iteração, garantindo obrigatoriamente sum(wi) = 1.0.
- Implementar função de penalidade externa caso a temperatura de alguma AZ ultrapasse o limite crítico de 75 °C.

Artefatos e Testes
- Executar e comparar a evolução do fitness para 3 tamanhos de população de partículas: 10, 30 e 50 partículas.
- Registrar a tabela com a melhor distribuição W encontrada para cada população e a validação da soma (sum(wi) = 1.0).


"""
LAB 01 - PSO Contínuo para Balanceamento Dinâmico de Carga em Datacenters

Objetivo:
Encontrar pesos W=[w1,...,w6], sum(W)=1, que minimizem a temperatura
média ponderada, considerando penalidade quando alguma temperatura
individual ultrapassar 75 °C.
"""

# ============================================================
# LAB 01 — PSO para Balanceamento Dinâmico de Carga
# Datacenter com 6 Zonas de Disponibilidade (AZs)
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. CONFIGURAÇÕES DO PROBLEMA
# ------------------------------------------------------------

# Coeficientes de aquecimento das 6 AZs
C = np.array([42.0, 35.0, 58.0, 30.0, 50.0, 65.0])

# Número de AZs
DIMENSION = 6

# Limite crítico de temperatura
TEMPERATURE_LIMIT = 75.0


# ------------------------------------------------------------
# 2. CLASSE PARTICLE
# ------------------------------------------------------------

class Particle:

    def __init__(self, dimension):
        """
        Cria uma partícula.

        position:
            Representa a distribuição de carga W.

        velocity:
            Velocidade usada pelo PSO para movimentar a partícula.

        best_position:
            Melhor posição encontrada pela própria partícula.

        best_fitness:
            Melhor fitness encontrado pela própria partícula.
        """

        # Gera posição aleatória
        self.position = np.random.rand(dimension)

        # Normaliza para garantir soma = 1
        self.position = self.position / np.sum(self.position)

        # Velocidade inicial aleatória
        self.velocity = np.random.uniform(
            -0.1,
            0.1,
            dimension
        )

        # Inicialmente, o melhor é a posição atual
        self.best_position = self.position.copy()

        # Como queremos minimizar, começamos com infinito
        self.best_fitness = float("inf")


# ------------------------------------------------------------
# 3. CLASSE PSO
# ------------------------------------------------------------

class PSO:

    def __init__(
        self,
        num_particles,
        dimension,
        coefficients,
        max_iterations=100,
        inertia=0.7,
        c1=1.5,
        c2=1.5,
        seed=None
    ):

        # Permite repetir o experimento
        if seed is not None:
            np.random.seed(seed)

        self.num_particles = num_particles
        self.dimension = dimension

        # Coeficientes de aquecimento
        self.C = np.array(coefficients)

        # Número de iterações
        self.max_iterations = max_iterations

        # Parâmetros do PSO
        self.inertia = inertia
        self.c1 = c1
        self.c2 = c2

        # Criação das partículas
        self.particles = [
            Particle(dimension)
            for _ in range(num_particles)
        ]

        # Melhor solução global
        self.global_best_position = None

        # Melhor fitness global
        self.global_best_fitness = float("inf")

        # Histórico do melhor fitness
        self.history = []


    # --------------------------------------------------------
    # 4. NORMALIZAÇÃO DA POSIÇÃO
    # --------------------------------------------------------

    def normalize_position(self, position):
        """
        Garante:

            wi >= 0

        e:

            sum(wi) = 1
        """

        # Elimina valores negativos
        position = np.maximum(position, 0)

        # Soma dos pesos
        total = np.sum(position)

        # Caso extremo: todos os valores sejam zero
        if total == 0:

            position = (
                np.ones(self.dimension)
                / self.dimension
            )

        else:

            position = position / total

        return position


    # --------------------------------------------------------
    # 5. FUNÇÃO DE FITNESS
    # --------------------------------------------------------

    def calculate_fitness(self, position):
        """
        Calcula o fitness da solução.

        Temperatura de cada AZ:

            Ti = Ci * wi

        Temperatura ponderada:

            T = sum(Ci * wi)

        Penalidade:

            Se Ti > 75, adicionamos uma penalidade.
        """

        # Calcula a temperatura de cada AZ
        temperatures = self.C * position

        # Temperatura ponderada total
        weighted_temperature = np.sum(
            temperatures
        )

        # Penalidade inicial
        penalty = 0.0

        # Verifica cada AZ
        for temperature in temperatures:

            if temperature > TEMPERATURE_LIMIT:

                # Penalidade quadrática
                penalty += (
                    temperature
                    - TEMPERATURE_LIMIT
                ) ** 2

        # Fitness final
        fitness = (
            weighted_temperature
            + penalty
        )

        return fitness


    # --------------------------------------------------------
    # 6. EXECUÇÃO DO PSO
    # --------------------------------------------------------

    def run(self):

        for iteration in range(
            self.max_iterations
        ):

            # =================================================
            # ETAPA 1 — AVALIAÇÃO DAS PARTÍCULAS
            # =================================================

            for particle in self.particles:

                fitness = self.calculate_fitness(
                    particle.position
                )

                # ---------------------------------------------
                # Atualiza P_best
                # ---------------------------------------------

                if fitness < particle.best_fitness:

                    particle.best_fitness = fitness

                    particle.best_position = (
                        particle.position.copy()
                    )

                # ---------------------------------------------
                # Atualiza G_best
                # ---------------------------------------------

                if fitness < self.global_best_fitness:

                    self.global_best_fitness = fitness

                    self.global_best_position = (
                        particle.position.copy()
                    )

            # Guarda o melhor fitness da iteração
            self.history.append(
                self.global_best_fitness
            )


            # =================================================
            # ETAPA 2 — ATUALIZAÇÃO DAS PARTÍCULAS
            # =================================================

            for particle in self.particles:

                # Números aleatórios
                r1 = np.random.rand(
                    self.dimension
                )

                r2 = np.random.rand(
                    self.dimension
                )

                # ---------------------------------------------
                # Atualização da velocidade
                #
                # v(t+1) =
                #     w*v(t)
                #     + c1*r1*(Pbest-x)
                #     + c2*r2*(Gbest-x)
                # ---------------------------------------------

                particle.velocity = (

                    self.inertia
                    * particle.velocity

                    + self.c1
                    * r1
                    * (
                        particle.best_position
                        - particle.position
                    )

                    + self.c2
                    * r2
                    * (
                        self.global_best_position
                        - particle.position
                    )
                )

                # ---------------------------------------------
                # Atualização da posição
                # ---------------------------------------------

                particle.position = (
                    particle.position
                    + particle.velocity
                )

                # ---------------------------------------------
                # Normalização
                # ---------------------------------------------

                particle.position = (
                    self.normalize_position(
                        particle.position
                    )
                )


        # Retorna resultado final
        return (
            self.global_best_position,
            self.global_best_fitness,
            self.history
        )


# ============================================================
# 7. EXECUTAR OS EXPERIMENTOS
# ============================================================

# Populações solicitadas pelo exercício
populations = [10, 30, 50]

# Dicionário para guardar os resultados
results = {}

# Número de iterações
MAX_ITERATIONS = 100

print("=" * 70)
print("EXECUÇÃO DO PSO")
print("=" * 70)

for population in populations:

    print(
        f"\nExecutando PSO com "
        f"{population} partículas..."
    )

    # Cria o PSO
    pso = PSO(
        num_particles=population,
        dimension=DIMENSION,
        coefficients=C,
        max_iterations=MAX_ITERATIONS,
        inertia=0.7,
        c1=1.5,
        c2=1.5,
        seed=42
    )

    # Executa
    best_position, best_fitness, history = (
        pso.run()
    )

    # Guarda resultado
    results[population] = {
        "position": best_position,
        "fitness": best_fitness,
        "history": history
    }


# ============================================================
# 8. MOSTRAR RESULTADOS
# ============================================================

print("\n")
print("=" * 70)
print("RESULTADOS FINAIS")
print("=" * 70)

for population in populations:

    result = results[population]

    position = result["position"]

    fitness = result["fitness"]

    total = np.sum(position)

    temperatures = C * position

    print(
        f"\nPopulação: {population} partículas"
    )

    print(
        "Melhor distribuição W:"
    )

    print(
        np.round(position, 6)
    )

    print(
        f"Soma dos pesos: {total:.6f}"
    )

    print(
        f"Fitness: {fitness:.6f}"
    )

    print(
        "Temperaturas das AZs:"
    )

    print(
        np.round(temperatures, 6)
    )


# ============================================================
# 9. CRIAR TABELA FINAL
# ============================================================

table_data = []

for population in populations:

    result = results[population]

    position = result["position"]

    fitness = result["fitness"]

    total = np.sum(position)

    row = {
        "Partículas": population,
        "w1": position[0],
        "w2": position[1],
        "w3": position[2],
        "w4": position[3],
        "w5": position[4],
        "w6": position[5],
        "Soma": total,
        "Fitness": fitness
    }

    table_data.append(row)


results_table = pd.DataFrame(
    table_data
)

print("\n")
print("=" * 70)
print("TABELA COMPARATIVA")
print("=" * 70)

display(
    results_table.round(6)
)


# ============================================================
# 10. VERIFICAÇÃO DA RESTRIÇÃO
# ============================================================

print("\n")
print("=" * 70)
print("VALIDAÇÃO DA SOMA DOS PESOS")
print("=" * 70)

for population in populations:

    position = results[population]["position"]

    total = np.sum(position)

    valid = np.isclose(
        total,
        1.0,
        atol=1e-10
    )

    print(
        f"{population} partículas -> "
        f"Soma = {total:.12f} -> "
        f"{'VÁLIDO' if valid else 'INVÁLIDO'}"
    )


# ============================================================
# 11. GRÁFICO DA EVOLUÇÃO DO FITNESS
# ============================================================

plt.figure(
    figsize=(10, 6)
)

for population in populations:

    history = results[population]["history"]

    plt.plot(
        range(1, MAX_ITERATIONS + 1),
        history,
        label=f"{population} partículas"
    )

plt.xlabel(
    "Iteração"
)

plt.ylabel(
    "Melhor Fitness (G_best)"
)

plt.title(
    "Evolução do Fitness do PSO"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.show()


# ============================================================
# 12. GRÁFICO DA DISTRIBUIÇÃO FINAL
# ============================================================

plt.figure(
    figsize=(10, 6)
)

x = np.arange(DIMENSION)

width = 0.25

for index, population in enumerate(populations):

    position = results[population]["position"]

    plt.bar(
        x + index * width,
        position,
        width,
        label=f"{population} partículas"
    )

plt.xticks(
    x + width,
    [
        "AZ1",
        "AZ2",
        "AZ3",
        "AZ4",
        "AZ5",
        "AZ6"
    ]
)

plt.xlabel(
    "Zona de Disponibilidade"
)

plt.ylabel(
    "Peso de tráfego"
)

plt.title(
    "Melhor Distribuição de Carga Encontrada"
)

plt.legend()

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.show()


# ============================================================
# 13. RESUMO FINAL
# ============================================================

print("\n")
print("=" * 70)
print("RESUMO")
print("=" * 70)

for population in populations:

    result = results[population]

    position = result["position"]

    fitness = result["fitness"]

    print(
        f"\n{population} partículas:"
    )

    print(
        f"  Fitness = {fitness:.6f}"
    )

    print(
        f"  Soma(W) = {np.sum(position):.6f}"
    )

    print(
        f"  Melhor W = {np.round(position, 6)}"
    )
