# -*- coding: utf-8 -*-
"""
AULA 10 - Motor de Inferência Mamdani e Superfície 3D (Sprint 2 da AC-3)
Disciplina: Inteligência Computacional

Versão com scikit-fuzzy (skfuzzy.control). Feita para rodar no Google Colab:
cole tudo numa célula e execute. A primeira parte instala as bibliotecas se faltarem.

Sistema: Impacto (0-100 %) x Explorabilidade (0-10) -> Urgência (0-100 %)
"""

# ----------------------------------------------------------------------------
# 0) Instalação automática das bibliotecas (funciona em .py e em célula do Colab)
# ----------------------------------------------------------------------------
import subprocess
import sys

def instalar_se_necessario():
    pacotes = {"skfuzzy": "scikit-fuzzy", "numpy": "numpy", "matplotlib": "matplotlib"}
    for modulo, pacote in pacotes.items():
        try:
            __import__(modulo)
        except ImportError:
            print(f"Instalando {pacote} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pacote])

instalar_se_necessario()

import os
import numpy as np
import matplotlib
try:
    get_ipython()            # Colab/Jupyter: mostra os gráficos na célula
    EM_NOTEBOOK = True
except NameError:
    matplotlib.use("Agg")    # fora do notebook: apenas salva os arquivos
    EM_NOTEBOOK = False
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import skfuzzy as fuzz
from skfuzzy import control as ctrl

SAIDA = "AULA_10"
os.makedirs(SAIDA, exist_ok=True)


def mostrar():
    if EM_NOTEBOOK:
        plt.show()


# ----------------------------------------------------------------------------
# 1) Sistema Mamdani (função fábrica: gera o sistema para cada configuração)
# ----------------------------------------------------------------------------
def criar_sistema(critica="trimf", defuzz="centroid"):
    """
    critica: 'trimf'  -> Urgência Crítica triangular        (base)
             'trapmf' -> Urgência Crítica trapezoidal        (Abordagem A)
    defuzz:  'centroid' ou 'mom'                             (Abordagem B = 'mom')
    """
    # Universos
    impacto = ctrl.Antecedent(np.arange(0, 100.01, 0.5), "impacto")
    explor = ctrl.Antecedent(np.arange(0, 10.001, 0.05), "explorabilidade")
    urgencia = ctrl.Consequent(np.arange(0, 100.01, 0.5), "urgencia", defuzzify_method=defuzz)

    # Entradas (conforme a matriz da aula)
    impacto["baixo"] = fuzz.trimf(impacto.universe, [0, 0, 40])
    impacto["medio"] = fuzz.trimf(impacto.universe, [20, 50, 80])
    impacto["alto"] = fuzz.trimf(impacto.universe, [60, 100, 100])

    explor["baixa"] = fuzz.trimf(explor.universe, [0, 0, 4])
    explor["moderada"] = fuzz.trimf(explor.universe, [2, 5, 8])
    explor["alta"] = fuzz.trimf(explor.universe, [6, 10, 10])

    # Saída (o enunciado não fixa os conjuntos de Urgência; estes são os escolhidos)
    urgencia["baixa"] = fuzz.trimf(urgencia.universe, [0, 0, 30])
    urgencia["media"] = fuzz.trimf(urgencia.universe, [15, 40, 65])
    urgencia["alta"] = fuzz.trimf(urgencia.universe, [50, 75, 100])
    if critica == "trapmf":
        urgencia["critica"] = fuzz.trapmf(urgencia.universe, [70, 90, 100, 100])
    else:
        urgencia["critica"] = fuzz.trimf(urgencia.universe, [70, 100, 100])

    # Matriz de regras 3x3 (9 regras, sem lacunas de cobertura)
    regras = [
        ctrl.Rule(impacto["baixo"] & explor["baixa"],    urgencia["baixa"]),
        ctrl.Rule(impacto["baixo"] & explor["moderada"], urgencia["baixa"]),
        ctrl.Rule(impacto["baixo"] & explor["alta"],     urgencia["media"]),

        ctrl.Rule(impacto["medio"] & explor["baixa"],    urgencia["media"]),
        ctrl.Rule(impacto["medio"] & explor["moderada"], urgencia["alta"]),
        ctrl.Rule(impacto["medio"] & explor["alta"],     urgencia["alta"]),

        ctrl.Rule(impacto["alto"] & explor["baixa"],     urgencia["critica"]),
        ctrl.Rule(impacto["alto"] & explor["moderada"],  urgencia["critica"]),
        ctrl.Rule(impacto["alto"] & explor["alta"],      urgencia["critica"]),
    ]
    sistema = ctrl.ControlSystem(regras)
    return ctrl.ControlSystemSimulation(sistema), urgencia


def calcular(sim, imp, exp):
    sim.input["impacto"] = float(imp)
    sim.input["explorabilidade"] = float(exp)
    sim.compute()
    return float(sim.output["urgencia"])


CONFIGS = {
    "Base: triângulos + centroid":         dict(critica="trimf", defuzz="centroid"),
    "Abord. A: trapmf crítica + centroid": dict(critica="trapmf", defuzz="centroid"),
    "Abord. B: triângulos + MOM":          dict(critica="trimf", defuzz="mom"),
}
SIMS = {nome: criar_sistema(**cfg) for nome, cfg in CONFIGS.items()}

# ----------------------------------------------------------------------------
# 2) Desafio dos Extremos
# ----------------------------------------------------------------------------
PONTOS = [(0, 0), (50, 5), (100, 10)]

print("=" * 78)
print("DESAFIO DOS EXTREMOS  (Impacto %, Explorabilidade) -> Urgência %")
print("=" * 78)
print(f"{'Configuração':<40}" + "".join(f"{str(p):>12}" for p in PONTOS))
for nome, (sim, _) in SIMS.items():
    vals = [calcular(sim, i, e) for i, e in PONTOS]
    print(f"{nome:<40}" + "".join(f"{v:>12.2f}" for v in vals))

# Gráfico de saída (centroid) nos dois extremos
sim_base, urg_base = SIMS["Base: triângulos + centroid"]
for (i, e), nome_arq in [((0, 0), "grafico_saida_0_0.png"), ((100, 10), "grafico_saida_100_10.png")]:
    v = calcular(sim_base, i, e)
    urg_base.view(sim=sim_base)
    plt.title(f"Entradas ({i}, {e}) -> centroide = {v:.2f}%")
    plt.savefig(os.path.join(SAIDA, nome_arq), dpi=150, bbox_inches="tight")
    mostrar()
    plt.close("all")

# ----------------------------------------------------------------------------
# 3) Superfície de decisão 3D
# ----------------------------------------------------------------------------
g_imp = np.linspace(0, 100, 31)
g_exp = np.linspace(0, 10, 31)
GI, GE = np.meshgrid(g_imp, g_exp)


def superficie(sim):
    return np.array([[calcular(sim, i, e) for i in g_imp] for e in g_exp])


def salto_max(Z):
    return max(np.abs(np.diff(Z, axis=0)).max(), np.abs(np.diff(Z, axis=1)).max())


def plot_surf(ax, Z, titulo):
    s = ax.plot_surface(GI, GE, Z, cmap="viridis", edgecolor="none")
    ax.set_xlabel("Impacto (%)")
    ax.set_ylabel("Explorabilidade")
    ax.set_zlabel("Urgência (%)")
    ax.set_zlim(0, 100)
    ax.set_title(titulo, fontsize=10)
    ax.view_init(elev=28, azim=-125)
    return s


print("\nCalculando superfícies (pode levar alguns segundos)...")
SUPS = {nome: superficie(sim) for nome, (sim, _) in SIMS.items()}

# Imagem exigida: superficie_decisao.png (centroid)
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")
s = plot_surf(ax, SUPS["Base: triângulos + centroid"], "Superfície de Decisão - Mamdani (centroid)")
fig.colorbar(s, shrink=0.6, label="Urgência (%)")
plt.tight_layout()
plt.savefig(os.path.join(SAIDA, "superficie_decisao.png"), dpi=150)
mostrar()
plt.close("all")

# Comparação lado a lado
fig = plt.figure(figsize=(16, 5))
for k, (nome, Z) in enumerate(SUPS.items(), 1):
    plot_surf(fig.add_subplot(1, 3, k, projection="3d"), Z, nome)
plt.tight_layout()
plt.savefig(os.path.join(SAIDA, "superficie_comparacao.png"), dpi=130)
mostrar()
plt.close("all")

print("\nSUAVIDADE (maior salto entre vizinhos da grade 31x31; menor = mais suave)")
for nome, Z in SUPS.items():
    print(f"{nome:<40} min={Z.min():6.2f}  max={Z.max():6.2f}  salto_max={salto_max(Z):6.2f}")

print("\nArquivos salvos em", os.path.abspath(SAIDA))

