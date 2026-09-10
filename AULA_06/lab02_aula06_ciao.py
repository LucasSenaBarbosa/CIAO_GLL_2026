import random
import matplotlib.pyplot as plt
import numpy as np

# Configuração fixa da rede (Grafo)
CUSTOS = np.array(
    [
        [0, 2, 4, np.inf, np.inf, np.inf],
        [2, 0, 1, 5, np.inf, np.inf],
        [4, 1, 0, 2, 3, np.inf],
        [np.inf, 5, 2, 0, 1, 4],
        [np.inf, np.inf, 3, 1, 0, 2],
        [np.inf, np.inf, np.inf, 4, 2, 0],
    ]
)

ORIGEM = 0
DESTINO = 4


def obter_vizinhos(no):
  return [
      p
      for p in range(len(CUSTOS))
      if CUSTOS[no][p] != np.inf and p != no
  ]


def escolher_proximo(no_atual, visitados, feromonio, alpha, beta):
  candidatos = [n for n in obter_vizinhos(no_atual) if n not in visitados]
  if not candidatos:
    return None

  atratividades = [
      (feromonio[no_atual][c] ** alpha) * ((1 / CUSTOS[no_atual][c]) ** beta)
      for c in candidatos
  ]
  soma = sum(atratividades)
  probabilidades = [a / soma for a in atratividades]

  return random.choices(candidatos, weights=probabilidades, k=1)[0]


def construir_rota(feromonio, alpha, beta):
  rota = [ORIGEM]
  atual = ORIGEM
  while atual != DESTINO:
    proximo = escolher_proximo(atual, rota, feromonio, alpha, beta)
    if proximo is None:
      return None
    rota.append(proximo)
    atual = proximo
  return rota


def calcular_custo(rota):
  return sum(
      CUSTOS[rota[i]][rota[i + 1]] for i in range(len(rota) - 1)
  )


def rodar_aco(
    num_formigas, num_iteracoes, alpha, beta, taxa_evaporacao, q=100
):
  feromonio = np.ones_like(CUSTOS, dtype=float)
  feromonio[CUSTOS == np.inf] = 0

  melhor_rota = None
  melhor_custo = float("inf")
  historico = []

  for _ in range(num_iteracoes):
    rotas = []
    for _ in range(num_formigas):
      rota = construir_rota(feromonio, alpha, beta)
      if rota:
        custo = calcular_custo(rota)
        rotas.append((rota, custo))
        if custo < melhor_custo:
          melhor_custo = custo
          melhor_rota = rota.copy()

    # Evaporação
    feromonio *= 1 - taxa_evaporacao
    feromonio[CUSTOS == np.inf] = 0

    # Depósito
    for r, c in rotas:
      deposito = q / c
      for i in range(len(r) - 1):
        feromonio[r[i]][r[i + 1]] += deposito

    historico.append(melhor_custo)

  return melhor_rota, melhor_custo, historico


# Lista dos 4 Experimentos com variações de parâmetros
experimentos = [
    # Experimento 1: Influência do ALPHA
    {
        "exp": "Exp 1 - ALPHA Baixo",
        "params": (20, 50, 0.1, 2.0, 0.5),
    },
    {
        "exp": "Exp 1 - ALPHA Alto",
        "params": (20, 50, 5.0, 2.0, 0.5),
    },
    # Experimento 2: Influência do BETA
    {
        "exp": "Exp 2 - BETA Baixo",
        "params": (20, 50, 1.0, 0.5, 0.5),
    },
    {
        "exp": "Exp 2 - BETA Alto",
        "params": (20, 50, 1.0, 5.0, 0.5),
    },
    # Experimento 3: Taxa de Evaporação
    {
        "exp": "Exp 3 - Evap Lenta",
        "params": (20, 50, 1.0, 2.0, 0.1),
    },
    {
        "exp": "Exp 3 - Evap Rápida",
        "params": (20, 50, 1.0, 2.0, 0.9),
    },
    # Experimento 4: Número de Formigas
    {
        "exp": "Exp 4 - 5 Formigas",
        "params": (5, 50, 1.0, 2.0, 0.5),
    },
    {
        "exp": "Exp 4 - 50 Formigas",
        "params": (50, 50, 1.0, 2.0, 0.5),
    },
]

# Execução e Exibição de Resultados
fig, axes = plt.subplots(4, 2, figsize=(12, 14))
axes = axes.flatten()

print("=" * 65)
print(f"{'EXPERIMENTO':<22} | {'FORM.':<5} | {'A/B':<7} | {'EVAP':<5} | {'CUSTO':<6} | ROTA")
print("=" * 65)

for idx, teste in enumerate(experimentos):
  n_f, n_it, a, b, evap = teste["params"]
  m_rota, m_custo, hist = rodar_aco(n_f, n_it, a, b, evap)

  print(
      f"{teste['exp']:<22} | {n_f:<5} | {a}/{b:<4} | {evap:<5} | {m_custo:<6} |"
      f" {m_rota}"
  )

  # Plotagem do gráfico para cada sub-teste
  axes[idx].plot(hist, color="blue", linewidth=1.8)
  axes[idx].set_title(
      f"{teste['exp']}\n(Formigas={n_f}, α={a}, β={b}, Evap={evap})", fontsize=10
  )
  axes[idx].set_xlabel("Iteração")
  axes[idx].set_ylabel("Melhor Custo")
  axes[idx].grid(True)

print("=" * 65)
plt.tight_layout()
plt.show()
