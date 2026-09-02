"""
MISSÃO 1 - A PARTÍCULA SOLITÁRIA

Objetivo: Entender como uma única partícula se move.
Descrição: código que simula uma única partícula em 1D (uma dimensão). Complete a função de atualização de posição.
"""
CÓDIGO ABAIXO 

# ============================================================
# MISSÃO 1 - PSO BÁSICO: UMA ÚNICA PARTÍCULA
# ============================================================

# -------------------------
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# -------------------------

import numpy as np                  # Trabalhar com números e arrays
import matplotlib.pyplot as plt     # Criar os gráficos
import random                       # Gerar números aleatórios
from IPython.display import clear_output  # Limpar a saída do Colab
import time                         # Criar pequenas pausas na animação


# -------------------------
# 2. CONFIGURAÇÕES DO PSO
# -------------------------

ITERACOES = 20       # Quantidade de vezes que a partícula irá se mover

W = 0.8              # Peso da inércia
C1 = 1.5             # Peso da experiência pessoal
C2 = 1.5             # Peso da experiência global

LIMITE = 10          # A partícula só pode ficar entre -10 e +10


# -------------------------
# 3. FUNÇÃO OBJETIVO
# -------------------------

def funcao(x):
    """
    Função que queremos minimizar.

    f(x) = x²

    O menor valor acontece quando x = 0.
    Nesse ponto:
    
    f(0) = 0
    """
    
    return x**2


# -------------------------
# 4. INICIALIZAÇÃO
# -------------------------

# Escolhe uma posição aleatória entre -10 e +10
posicao = random.uniform(-LIMITE, LIMITE)

# Escolhe uma velocidade inicial aleatória entre -1 e +1
velocidade = random.uniform(-1, 1)

# Calcula o fitness da posição inicial
fitness = funcao(posicao)


# -------------------------
# 5. pBEST
# -------------------------

# Inicialmente, o melhor lugar encontrado
# é a própria posição inicial.

pBest_pos = posicao
pBest_fit = fitness


# -------------------------
# 6. gBEST
# -------------------------

# Como temos apenas UMA partícula,
# o melhor global é igual ao melhor pessoal.

gBest_pos = posicao
gBest_fit = fitness


# -------------------------
# 7. HISTÓRICO
# -------------------------

# Vamos guardar todas as posições
# para podermos desenhar a trajetória.

historico_pos = [posicao]

# Vamos guardar também todos os valores de fitness.

historico_fit = [fitness]


# -------------------------
# 8. PREPARANDO O GRÁFICO
# -------------------------

# Criamos os valores de x que serão usados
# para desenhar a função inteira.

x_plot = np.linspace(-LIMITE, LIMITE, 1000)

# Calculamos f(x) para cada valor de x.

y_plot = funcao(x_plot)


# ============================================================
# 9. INÍCIO DA SIMULAÇÃO
# ============================================================

print("=" * 60)
print("PSO - PARTÍCULA SOLITÁRIA")
print("=" * 60)

print(f"\nPosição inicial: {posicao:.4f}")
print(f"Velocidade inicial: {velocidade:.4f}")
print(f"Fitness inicial: {fitness:.4f}")
print(f"pBest inicial: {pBest_pos:.4f}")
print(f"gBest inicial: {gBest_pos:.4f}")

print("\nIniciando animação...\n")


# ============================================================
# 10. LOOP PRINCIPAL DO PSO
# ============================================================

for i in range(ITERACOES):

    # --------------------------------------------------------
    # 10.1 GERAR NÚMEROS ALEATÓRIOS
    # --------------------------------------------------------

    r1 = random.random()
    r2 = random.random()


    # --------------------------------------------------------
    # 10.2 ATUALIZAR A VELOCIDADE
    # --------------------------------------------------------

    velocidade_nova = (
        W * velocidade
        + C1 * r1 * (pBest_pos - posicao)
        + C2 * r2 * (gBest_pos - posicao)
    )


    # --------------------------------------------------------
    # 10.3 ATUALIZAR A POSIÇÃO
    # --------------------------------------------------------

    posicao_nova = posicao + velocidade_nova


    # --------------------------------------------------------
    # 10.4 GARANTIR QUE A POSIÇÃO NÃO SAIA DOS LIMITES
    # --------------------------------------------------------

    posicao_nova = np.clip(
        posicao_nova,
        -LIMITE,
        LIMITE
    )


    # --------------------------------------------------------
    # 10.5 CALCULAR O NOVO FITNESS
    # --------------------------------------------------------

    fitness_novo = funcao(posicao_nova)


    # --------------------------------------------------------
    # 10.6 ATUALIZAR POSIÇÃO, VELOCIDADE E FITNESS
    # --------------------------------------------------------

    posicao = posicao_nova
    velocidade = velocidade_nova
    fitness = fitness_novo


    # --------------------------------------------------------
    # 10.7 VERIFICAR SE ENCONTRAMOS UM NOVO pBEST
    # --------------------------------------------------------

    if fitness < pBest_fit:

        pBest_fit = fitness
        pBest_pos = posicao


    # --------------------------------------------------------
    # 10.8 VERIFICAR SE ENCONTRAMOS UM NOVO gBEST
    # --------------------------------------------------------

    if fitness < gBest_fit:

        gBest_fit = fitness
        gBest_pos = posicao


    # --------------------------------------------------------
    # 10.9 GUARDAR HISTÓRICO
    # --------------------------------------------------------

    historico_pos.append(posicao)
    historico_fit.append(fitness)


    # ========================================================
    # 11. MOSTRAR INFORMAÇÕES DA ITERAÇÃO
    # ========================================================

    clear_output(wait=True)

    print("=" * 60)
    print("PSO - PARTÍCULA SOLITÁRIA")
    print("=" * 60)

    print(f"\nIteração: {i + 1}/{ITERACOES}")

    print(f"r1:             {r1:.4f}")
    print(f"r2:             {r2:.4f}")

    print(f"\nPosição:         {posicao:.6f}")
    print(f"Velocidade:      {velocidade:.6f}")
    print(f"Fitness:         {fitness:.6f}")

    print(f"\npBest posição:   {pBest_pos:.6f}")
    print(f"pBest fitness:   {pBest_fit:.6f}")

    print(f"\ngBest posição:   {gBest_pos:.6f}")
    print(f"gBest fitness:   {gBest_fit:.6f}")


    # ========================================================
    # 12. CRIAR O GRÁFICO
    # ========================================================

    plt.figure(figsize=(14, 5))


    # --------------------------------------------------------
    # GRÁFICO 1 - FUNÇÃO E PARTÍCULA
    # --------------------------------------------------------

    plt.subplot(1, 2, 1)

    # Desenha a função f(x) = x²
    plt.plot(
        x_plot,
        y_plot,
        color="blue",
        linewidth=2,
        label="f(x) = x²"
    )

    # Desenha a trajetória da partícula
    plt.plot(
        historico_pos,
        [funcao(p) for p in historico_pos],
        color="orange",
        linestyle="--",
        marker="o",
        markersize=5,
        label="Trajetória"
    )

    # Desenha a posição atual
    plt.scatter(
        posicao,
        fitness,
        color="red",
        s=200,
        marker="*",
        label="Partícula"
    )

    # Desenha o pBest
    plt.scatter(
        pBest_pos,
        pBest_fit,
        color="green",
        s=100,
        marker="X",
        label="pBest"
    )

    # Linha vertical indicando o ótimo global x=0
    plt.axvline(
        x=0,
        color="purple",
        linestyle=":",
        linewidth=2,
        label="Ótimo global x=0"
    )

    plt.xlabel("Posição x")
    plt.ylabel("Fitness f(x)")

    plt.title(
        f"Movimento da Partícula - Iteração {i + 1}"
    )

    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.xlim(-LIMITE, LIMITE)
    plt.ylim(0, LIMITE**2)


    # --------------------------------------------------------
    # GRÁFICO 2 - CONVERGÊNCIA
    # --------------------------------------------------------

    plt.subplot(1, 2, 2)

    # Mostra a evolução do fitness
    plt.plot(
        range(len(historico_fit)),
        historico_fit,
        color="red",
        marker="o",
        linewidth=2
    )

    # Linha indicando o fitness ótimo
    plt.axhline(
        y=0,
        color="green",
        linestyle="--",
        label="Fitness ótimo = 0"
    )

    plt.xlabel("Iteração")
    plt.ylabel("Fitness")

    plt.title("Convergência do PSO")

    plt.grid(True, alpha=0.3)

    plt.legend()

    plt.ylim(0, LIMITE**2)


    # Ajusta os gráficos
    plt.tight_layout()

    # Mostra o gráfico
    plt.show()


    # Pequena pausa para enxergarmos a animação
    time.sleep(0.5)


# ============================================================
# 13. RESULTADO FINAL
# ============================================================

print("\n" + "=" * 60)
print("RESULTADO FINAL")
print("=" * 60)

print(f"Posição final:  {posicao:.6f}")
print(f"Fitness final:  {fitness:.6f}")

print("\nMelhor posição encontrada:")
print(f"pBest = {pBest_pos:.6f}")

print(f"\nMelhor fitness encontrado:")
print(f"pBest fitness = {pBest_fit:.6f}")

print("\nÓtimo global conhecido:")
print("x = 0.000000")
print("f(x) = 0.000000")

print(f"\nErro em relação ao ótimo:")
print(f"{abs(pBest_pos):.6f}")

-------------------------------------------------------------------------------------------------------------------------------------------------

"" MISSÃO 2: O ENXAME DE PARTÍCULAS
Cenário: Enxame procurando o mínimo da função de Rosenbrock
f(x,y) = (1-x)² + 100*(y-x²)² ""

import numpy as np
import matplotlib.pyplot as plt
import random # Adicionado para criar_particula
from matplotlib.animation import FuncAnimation

# ==================== CONFIGURAÇÕES ====================
NUM_PARTICULAS = 20
ITERACOES = 50
W = 0.7
C1 = 1.8
C2 = 1.8
X_MIN, X_MAX = -2, 2
Y_MIN, Y_MAX = -1, 3

# ==================== FUNÇÃO OBJETIVO ====================
def rosenbrock(posicao):
    x, y = posicao
    return (1 - x)**2 + 100 * (y - x**2)**2

# ==================== FUNÇÕES A COMPLETAR ====================

# TODO 1: Inicializar uma partícula
def criar_particula():
    """
    Cria uma partícula com posição e velocidade aleatórias.

    Retorna um dicionário com:
    - posicao: array [x, y] aleatório dentro dos limites
    - velocidade: array [vx, vy] aleatório entre -0.5 e 0.5
    - fitness: fitness na posição atual
    - pBest_pos: cópia da posição inicial
    - pBest_fit: fitness inicial
    """
    posicao = np.array([
        random.uniform(X_MIN, X_MAX),
        random.uniform(Y_MIN, Y_MAX)
    ])
    # Limites de velocidade com base na descrição do problema
    velocidade = np.array([
        random.uniform(-0.5, 0.5),
        random.uniform(-0.5, 0.5)
    ])
    fitness = rosenbrock(posicao)

    return {
        'posicao': posicao,
        'velocidade': velocidade,
        'fitness': fitness,
        'pBest_pos': np.copy(posicao),
        'pBest_fit': fitness
    }

# TODO 2: Atualizar a velocidade de uma partícula
def atualizar_velocidade(particula, gBest_pos):
    """
    Atualiza a velocidade da partícula usando a fórmula do PSO.

    Parâmetros:
    - particula: dicionário da partícula
    - gBest_pos: melhor posição global

    Retorna: nova velocidade (array)
    """
    r1 = np.random.random(2)
    r2 = np.random.random(2)

    # Fórmula: v_novo = w*v + c1*r1*(pBest - pos) + c2*r2*(gBest - pos)
    termo_inercia = W * particula['velocidade']
    termo_cognitivo = C1 * r1 * (particula['pBest_pos'] - particula['posicao'])
    termo_social = C2 * r2 * (gBest_pos - particula['posicao'])

    nova_velocidade = termo_inercia + termo_cognitivo + termo_social

    # Limitar velocidade
    nova_velocidade = np.clip(nova_velocidade, -0.5, 0.5) # Valores de -0.5 a 0.5 como na inicialização

    return nova_velocidade

def atualizar_posicao(particula):
    """
    Atualiza a posição da partícula baseado na sua velocidade.
    Garante que a posição fique dentro dos limites.
    """
    particula['posicao'] = particula['posicao'] + particula['velocidade']

    # Manter as partículas dentro dos limites do mapa
    particula['posicao'][0] = np.clip(particula['posicao'][0], X_MIN, X_MAX)
    particula['posicao'][1] = np.clip(particula['posicao'][1], Y_MIN, Y_MAX)

# ==================== INICIALIZAÇÃO DO ENXAME ====================
enxame = [criar_particula() for _ in range(NUM_PARTICULAS)]

# Inicializar gBest (melhor global)
gbest_valor = float('inf')
gbest_posicao = np.array([0.0, 0.0]) # Placeholder, será atualizado no loop

for particula in enxame:
    if particula['pBest_fit'] < gbest_valor:
        gbest_valor = particula['pBest_fit']
        gbest_posicao = np.copy(particula['pBest_pos'])

# Lista para armazenar o histórico do melhor fitness global
historico_gbest_fitness = []

# ==================== CONFIGURAÇÃO DA ANIMAÇÃO ====================
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title("Otimização por Enxame de Partículas (PSO) - Rosenbrock")
ax.set_xlim(X_MIN, X_MAX)
ax.set_ylim(Y_MIN, Y_MAX)

# Desenhando o mapa de contorno da função de Rosenbrock
x_grid = np.linspace(X_MIN, X_MAX, 100)
y_grid = np.linspace(Y_MIN, Y_MAX, 100)
X_mesh, Y_mesh = np.meshgrid(x_grid, y_grid)
Z = rosenbrock([X_mesh, Y_mesh])
contour = ax.contourf(X_mesh, Y_mesh, Z, levels=50, cmap='viridis', alpha=0.6)
plt.colorbar(contour, ax=ax, label='Valor da Função (Menor é Melhor)')

# Elementos gráficos que serão atualizados
initial_positions_array = np.array([p['posicao'] for p in enxame])
scatter = ax.scatter(initial_positions_array[:, 0], initial_positions_array[:, 1], color='red', marker='o', edgecolors='white', s=50, label='Partículas')
gbest_marker, = ax.plot(gbest_posicao[0], gbest_posicao[1], marker='*', color='yellow', markersize=15, linestyle='None', label='Melhor do Bando')
ax.legend()

# ==================== O MOTOR DO ALGORITMO (ATUALIZAÇÃO) ====================
def atualizar(frame):
    global gbest_valor, gbest_posicao

    for i in range(NUM_PARTICULAS):
        particula = enxame[i]

        # 1. Atualizar Velocidade (usando a nova função)
        particula['velocidade'] = atualizar_velocidade(particula, gbest_posicao)

        # 2. Atualizar Posição
        atualizar_posicao(particula)

        # 3. Avaliar nova posição
        valor_atual = rosenbrock(particula['posicao'])
        particula['fitness'] = valor_atual # Atualizar fitness atual

        # Atualizar memória pessoal (pBest)
        if valor_atual < particula['pBest_fit']:
            particula['pBest_fit'] = valor_atual
            particula['pBest_pos'] = np.copy(particula['posicao'])

            # Atualizar memória do bando (gBest)
            if valor_atual < gbest_valor:
                gbest_valor = valor_atual
                gbest_posicao = np.copy(particula['posicao'])

    # Armazenar o melhor fitness global desta iteração
    historico_gbest_fitness.append(gbest_valor)

    # Atualizar o gráfico
    current_positions_array = np.array([p['posicao'] for p in enxame])
    scatter.set_offsets(current_positions_array)
    gbest_marker.set_data([gbest_posicao[0]], [gbest_posicao[1]])
    ax.set_title(f"PSO - Iteração: {frame+1}/{ITERACOES} | Melhor Valor: {gbest_valor:.4f}")

    return scatter, gbest_marker,

# Criar a animação
anim = FuncAnimation(fig, atualizar, frames=ITERACOES, interval=150, blit=False, repeat=False)

plt.show()

plt.figure(figsize=(10, 6))
plt.plot(historico_gbest_fitness, color='blue', linewidth=2)
plt.title('Evolução do Melhor Fitness Global (Rosenbrock Function)')
plt.xlabel('Iteração')
plt.ylabel('Melhor Fitness Global')
plt.grid(True)
plt.yscale('log') # Usar escala logarítmica para melhor visualização se os valores variarem muito
plt.show()


-------------------------------------------------------------------------------------------------------------------------------------------------


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
