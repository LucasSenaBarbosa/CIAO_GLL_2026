import random
import matplotlib.pyplot as plt
import numpy as np

# Requisito 1: Representar a rede utilizando uma matriz de custos
CUSTOS = np.array(
    [
    [0, 2, 4, np.inf, np.inf, np.inf, 6],
    [2, 0, 1, 5, 6,np.inf, np.inf],
    [4, 1, 0, 2, 3, 5, np.inf],
    [np.inf, 5, 2, 0, 1, 4, 6],
    [np.inf, np.inf, 3, 1, 0, 2, 4],
    [np.inf, np.inf, np.inf, 4, 2, 0, 3],
    [1, 0, np.inf, np.inf, np.inf, 4, 5]
    ]
)

ORIGEM = 0
DESTINO = 6

# Parâmetros mínimos
NUM_FORMIGAS = 40
NUM_ITERACOES = 80

ALPHA = 2
BETA = 3

TAXA_EVAPORACAO = 0.5
Q = 100

# Requisito 2: Criar uma matriz de feromônio
feromonio = np.ones_like(CUSTOS, dtype=float)
feromonio[CUSTOS == np.inf] = 0.0


def obter_vizinhos(no):
  vizinhos = []
  for proximo in range(len(CUSTOS)):
    if CUSTOS[no][proximo] != np.inf and proximo != no:
      vizinhos.append(proximo)
  return vizinhos


def escolher_proximo_no(no_atual, visitados):
  vizinhos = obter_vizinhos(no_atual)

  # Requisito 5: Impedir que uma formiga visite novamente um nó já visitado
  candidatos = [no for no in vizinhos if no not in visitados]

  if not candidatos:
    return None

  atratividades = []
  for proximo in candidatos:
    fer = feromonio[no_atual][proximo]
    custo = CUSTOS[no_atual][proximo]
    atratividade = (fer**ALPHA) * ((1.0 / custo) ** BETA)
    atratividades.append(atratividade)

  soma_atratividades = sum(atratividades)
  probabilidades = [a / soma_atratividades for a in atratividades]

  return random.choices(candidatos, weights=probabilidades, k=1)[0]


# Requisito 4: Fazer cada formiga construir uma rota
def construir_rota():
  rota = [ORIGEM]
  atual = ORIGEM

  while atual != DESTINO:
    proximo = escolher_proximo_no(atual, rota)
    if proximo is None:
      return None  # Caminho sem saída
    rota.append(proximo)
    atual = proximo

  return rota


# Requisito 6: Calcular o custo de cada rota
def calcular_custo(rota):
  custo_total = 0.0
  for i in range(len(rota) - 1):
    u = rota[i]
    v = rota[i + 1]
    custo_total += CUSTOS[u][v]
  return custo_total


# Requisito 7: Reforçar as melhores rotas com feromônio
def depositar_feromonio(rotas_e_custos):
  for rota, custo in rotas_e_custos:
    deposito = Q / custo
    for i in range(len(rota) - 1):
      u = rota[i]
      v = rota[i + 1]
      feromonio[u][v] += deposito


# Requisito 8: Aplicar evaporação
def evaporar_feromonio():
  global feromonio
  feromonio *= 1.0 - TAXA_EVAPORACAO
  feromonio[CUSTOS == np.inf] = 0.0


# Variáveis de controle de resultados
melhor_rota = None
melhor_custo = float("inf")
historico_melhor_custo = []

# Requisito 9: Repetir o processo por várias iterações
for iteracao in range(NUM_ITERACOES):
  rotas_validas = []

  # Requisito 3: Criar várias formigas
  for _ in range(NUM_FORMIGAS):
    rota = construir_rota()

    if rota is not None:
      custo = calcular_custo(rota)
      rotas_validas.append((rota, custo))

      if custo < melhor_custo:
        melhor_custo = custo
        melhor_rota = rota.copy()

  evaporar_feromonio()
  depositar_feromonio(rotas_validas)

  historico_melhor_custo.append(melhor_custo)

# Requisitos 10 e 11: Informar a melhor rota encontrada e seu custo
print("========== RESULTADO ==========")
print("\nMelhor rota encontrada:")
print(melhor_rota)
print("\nMelhor custo:")
print(melhor_custo)

# Requisito 12: Exibir um gráfico mostrando a evolução do melhor custo
plt.figure(figsize=(9, 5))
plt.plot(historico_melhor_custo, color="blue", linewidth=2)
plt.xlabel("Iteração")
plt.ylabel("Melhor Custo")
plt.title("Evolução do Melhor Custo (ACO do Zero)")
plt.grid(True)
plt.show()
