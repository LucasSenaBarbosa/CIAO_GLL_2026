"""
MISSÃO 3: OTIMIZAÇÃO LOGÍSTICA
Problema: Encontrar a localização de 5 centros de distribuição
que minimiza o custo de entrega para 50 clientes.
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import time

# ==================== CONFIGURAÇÕES ====================
NUM_CLIENTES = 50
NUM_CENTROS = 5
NUM_PARTICULAS = 30
ITERACOES = 100
W = 0.7
C1 = 1.8
C2 = 1.8
LIMITE = 10  # Coordenadas de 0 a 10

# ==================== GERAR DADOS ====================
np.random.seed(42)
clientes = np.random.rand(NUM_CLIENTES, 2) * LIMITE
demandas = np.random.randint(1, 100, NUM_CLIENTES)

print("=" * 60)
print(" OPTIMUS TECH - LOGÍSTICA INTELIGENTE")
print("=" * 60)
print(f"\n DADOS DO PROBLEMA:")
print(f"   - {NUM_CLIENTES} clientes")
print(f"   - {NUM_CENTROS} centros de distribuição")
print(f"   - Demanda média: {np.mean(demandas):.1f} unidades")

# ==================== FUNÇÃO OBJETIVO ====================
def fitness(posicoes_centros):
    """
    Calcula o custo total de entrega.

    posicoes_centros: array de 10 elementos
    [x1,y1,x2,y2,...,x5,y5]

    Retorna: -custo_total
    """

    # TODO 1: Converter para lista de centros
    centros = []

    for i in range(NUM_CENTROS):
        centros.append([
            posicoes_centros[2*i],
            posicoes_centros[2*i + 1]
        ])

    custo_total = 0

    # Para cada cliente
    for cliente, demanda in zip(clientes, demandas):

        # TODO 2: Encontrar o centro mais próximo
        distancias = []

        for centro in centros:
            distancia = np.sqrt(
                (centro[0] - cliente[0])**2 +
                (centro[1] - cliente[1])**2
            )
            distancias.append(distancia)

        centro_mais_proximo = np.argmin(distancias)

        # TODO 3: Calcular distância ao centro mais próximo
        distancia_minima = distancias[centro_mais_proximo]

        # TODO 4: Adicionar ao custo total
        custo_total += distancia_minima * demanda

    # Retornar negativo
    return -custo_total


# ==================== PSO COMPLETO ====================

# TODO 5: Criar uma partícula (10 dimensões)
def criar_particula():

    dimensao = NUM_CENTROS * 2

    posicao = np.random.uniform(
        0,
        LIMITE,
        dimensao
    )

    velocidade = np.random.uniform(
        -0.5,
        0.5,
        dimensao
    )

    fit = fitness(posicao)

    return {
        'posicao': posicao,
        'velocidade': velocidade,
        'fitness': fit,
        'pBest_pos': posicao.copy(),
        'pBest_fit': fit
    }


# TODO 6: Atualizar velocidade (10 dimensões)
def atualizar_velocidade(particula, gBest_pos):

    dimensao = NUM_CENTROS * 2

    r1 = np.random.random(dimensao)
    r2 = np.random.random(dimensao)

    velocidade_nova = (
        W * particula['velocidade']
        + C1 * r1 * (particula['pBest_pos'] - particula['posicao'])
        + C2 * r2 * (gBest_pos - particula['posicao'])
    )

    return velocidade_nova


# TODO 7: Atualizar posição (10 dimensões) com limites
def atualizar_posicao(particula):

    posicao_nova = (
        particula['posicao'] +
        particula['velocidade']
    )

    posicao_nova = np.clip(
        posicao_nova,
        0,
        LIMITE
    )

    return posicao_nova


# ==================== EXECUTAR ====================
def executar_pso():

    # Inicializar
    enxame = []

    for _ in range(NUM_PARTICULAS):
        enxame.append(criar_particula())

    # Encontrar gBest
    melhor = min(
        enxame,
        key=lambda p: p['fitness']
    )

    gBest_pos = melhor['posicao'].copy()
    gBest_fit = melhor['fitness']

    historico = [gBest_fit]

    print("\n OTIMIZANDO...")
    start_time = time.time()

    for iteracao in range(ITERACOES):

        for p in enxame:

            p['velocidade'] = atualizar_velocidade(
                p,
                gBest_pos
            )

            p['posicao'] = atualizar_posicao(p)

            p['fitness'] = fitness(
                p['posicao']
            )

            # Atualizar pBest
            if p['fitness'] < p['pBest_fit']:

                p['pBest_fit'] = p['fitness']

                p['pBest_pos'] = p['posicao'].copy()

            # Atualizar gBest
            if p['fitness'] < gBest_fit:

                gBest_fit = p['fitness']

                gBest_pos = p['posicao'].copy()

        historico.append(gBest_fit)

        if (iteracao + 1) % 20 == 0:

            print(
                f"  Iteração {iteracao+1:3d}: "
                f"Custo = {-gBest_fit:.2f}"
            )

    execution_time = time.time() - start_time

    return (
        gBest_pos,
        gBest_fit,
        historico,
        execution_time
    )


# ==================== RESULTADOS ====================
best_pos, best_fit, historico, exec_time = executar_pso()

# Converter melhor posição para centros
centros = []

for i in range(NUM_CENTROS):

    centros.append([
        best_pos[2*i],
        best_pos[2*i + 1]
    ])


print(f"\n RESULTADO FINAL:")
print(f"   Tempo de execução: {exec_time:.2f} segundos")
print(f"   Custo total: {abs(best_fit):.2f}")
print(f"   Melhor custo possível: 0.00")

print(f"   Centros de distribuição:")

for i, centro in enumerate(centros):

    print(
        f"      Centro {i+1}: "
        f"({centro[0]:.2f}, {centro[1]:.2f})"
    )


# ==================== VISUALIZAÇÃO ====================
fig, (ax1, ax2) = plt.subplots(
    1,
    2,
    figsize=(14, 5)
)

# Mapa de clientes e centros
ax1.scatter(
    clientes[:, 0],
    clientes[:, 1],
    c='blue',
    s=30,
    alpha=0.6,
    label='Clientes'
)

for i, centro in enumerate(centros):

    ax1.scatter(
        centro[0],
        centro[1],
        c='red',
        s=200,
        marker='s',
        label=f'Centro {i+1}' if i == 0 else ""
    )

    ax1.annotate(
        f'C{i+1}',
        (centro[0], centro[1]),
        fontsize=10,
        ha='center',
        va='bottom',
        weight='bold'
    )

ax1.set_xlabel('Coordenada X')
ax1.set_ylabel('Coordenada Y')
ax1.set_title('Clientes e Centros de Distribuição')
ax1.legend()
ax1.grid(True, alpha=0.3)


# Convergência
ax2.plot(
    [-x for x in historico],
    'b-',
    linewidth=2
)

ax2.set_xlabel('Iteração')
ax2.set_ylabel('Custo Total')
ax2.set_title('Convergência da Otimização')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
