"""
AULA DE LÓGICA FUZZY - Código 2 (laboratório dos alunos)

Mesmo problema da gorjeta, agora com a biblioteca scikit-fuzzy.
Você vai: (1) rodar, (2) ver os gráficos, (3) fazer os experimentos no final.

Instalação:  pip install numpy matplotlib scikit-fuzzy
Execução:    python 02_laboratorio_skfuzzy.py
"""
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ---------- 1) Variáveis linguísticas (universos de discurso) ----------
servico = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "servico")   # nota 0-10
comida = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "comida")     # nota 0-10

# ---------- 2) Conjuntos fuzzy (funções de pertinência) ----------
servico["ruim"] = fuzz.trapmf(servico.universe, [0, 0, 3, 5])
servico["medio"] = fuzz.trapmf(servico.universe, [0, 3, 7, 10])
servico["bom"] = fuzz.trapmf(servico.universe, [5, 7, 10, 10])
servico["exelente"] = fuzz.gaussmf(servico.universe, 10, 1)

comida["ruim"] = fuzz.trimf(comida.universe, [0, 0, 5])
comida["medio"] = fuzz.trimf(comida.universe, [0, 5, 10])
comida["bom"] = fuzz.trimf(comida.universe, [5, 10, 10])

def criar_simulacao(metodo):
    gorjeta = ctrl.Consequent(
        np.arange(0, 25.01, 0.5),
        "gorjeta",
        defuzzify_method=metodo,
    )
    gorjeta["baixa"] = fuzz.trimf(gorjeta.universe, [0, 0, 13])
    gorjeta["media"] = fuzz.trimf(gorjeta.universe, [0, 13, 25])
    gorjeta["alta"] = fuzz.trimf(gorjeta.universe, [13, 25, 25])

    regras = [
        ctrl.Rule(servico["ruim"] | comida["ruim"], gorjeta["baixa"]),
        ctrl.Rule(servico["medio"] & comida["medio"], gorjeta["media"]),
        ctrl.Rule(servico["bom"] | comida["bom"], gorjeta["alta"]),
    ]
    sistema = ctrl.ControlSystem(regras)
    return gorjeta, ctrl.ControlSystemSimulation(sistema)


def pedir_nota(texto, padrao):
    """Lê uma nota de 0 a 10; se o aluno só apertar Enter, usa o padrão."""
    resposta = input(f"{texto} (0-10) [{padrao}]: ").strip()
    return float(resposta.replace(",", ".")) if resposta else padrao


nota_servico = pedir_nota("Nota do serviço", 7)
nota_comida = pedir_nota("Nota da comida", 3)

# ---------- 4) Simulação e comparação da defuzzificação ----------
resultados = {}
for metodo in ("centroid", "bisector", "mom"):
    gorjeta_metodo, sim_metodo = criar_simulacao(metodo)
    sim_metodo.input["servico"] = nota_servico
    sim_metodo.input["comida"] = nota_comida
    sim_metodo.compute()
    resultados[metodo] = sim_metodo.output["gorjeta"]

    if metodo == "centroid":
        gorjeta = gorjeta_metodo
        sim = sim_metodo

print("\nComparação dos métodos de defuzzificação:")
for metodo, valor in resultados.items():
    print(f"  {metodo}: {valor:.1f}%")

# ---------- 5) Gráficos ----------
servico.view()                 # funções de pertinência do serviço
comida.view()                  # funções de pertinência da comida
gorjeta.view(sim=sim)          # área agregada + linha do centroide (resultado)
plt.show()

# ======================= EXPERIMENTOS =======================
# 1) Troque a regra 2 por:  servico["medio"] & comida["medio"]
#    O que mudou no resultado para (7, 3)? Por quê?
#           Não mudou nada, pois a regra 2 não é ativada para (7, 3). 

# 2) Troque os triângulos de "servico" por trapézios (fuzz.trapmf) ou
#    gaussianas (fuzz.gaussmf, [media, desvio]). O resultado ficou mais suave?
#  Sim o formato do grafico mudou e ficou mais facil de entender.

# 3) Compare métodos de defuzzificação:
#      gorjeta = ctrl.Consequent(np.arange(0, 25.01, 0.5), "gorjeta",
#                                defuzzify_method="mom")   # "centroid", "bisector", "mom"...
# 4) Adicione um 4º conjunto "excelente" ao serviço e escreva a regra nova.

# 5) Teste (0, 0), (10, 10), (5, 5): o comportamento é o que você esperava?
# m, o comportamento é o esperado, pois (0, 0) resulta em gorjeta baixa, (10, 10) em gorjeta alta e (5, 5) em gorjeta média.