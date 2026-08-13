Relatório **LAB01**

#PERGUNTAS:
# 1. Por que o total de soluções avaliadas e exatamente 32?
R: Por causa da quantidade de itens
2^N e como tem 5 itens ficaria 2^5
# 2. O que aconteceria se eu colocasse 15 itens?
Seria 2^15 e daria 32.768
# 3.Voces conseguem imaginar um problema da vida real que seja parecido com este?
Durante um internação num hospital por exemplo, podemos levar diversos itens como uma escova, cobertor, roupas, etc.

Relatório **LAB02**

# REFLEXÃO FINAL
# Tabela que as duplas/trio devem preencher
# Numero de cidades | Rotas avaliadas | Tempo (s) | Melhor custo
# 4                 |        6         |     0.000117      |  80
# 5                 |        24        |      0.000146     |  41
# 6                 |        120       |     0.000633      |  91

# Perguntas de reflexão (obrigatórias)
# 16.	O numero de rotas cresce de forma linear, quadrática ou muito mais rápido? Explique com as quantidades que você coletou.
Muito mais rápida, de forma fatorial igual a N-1, 4 - 1 que daria 3 e 3 fatorial é 6
# 17.	Com base no padrão observado, estime (mesmo que de forma grosseira) quanto tempo levaria para 10 cidades no mesmo computador.
Estimativa para 10 cidades:

Tempo = (Número de Rotas) * (Tempo por Rota) Tempo = 362.880 * 5.6775e-6 segundos/rota Tempo ≈ 2.059 segundos

Portanto, para 10 cidades, estimaria que levaria aproximadamente 2 a 3 segundos no mesmo computador.
# 18.	Por que dizemos que o TSP e um problema “difícil”? A resposta não e “porque e complicado de entender”, e sim por causa do crescimento do tempo.
Por que quanto maio a quantidade de resultados, maior o tempo e mais complexa vai ser a resposta

Relatório **LAB03**
Resposta:

# 19.	Codigo completo (com a funcao calcular_gap implementada e o loop funcionando).
# ============================================================
# Atividade 3 - Heurística Gulosa + Gap de Otimalidade
# ============================================================

import numpy as np
import itertools
import time


# ----------------------------------------------------------
# 1. Função que resolve a mochila por força-bruta (ótima)
# ----------------------------------------------------------

def mochila_otima(pesos, valores, capacidade):
    n = len(pesos)

    melhor = 0

    for comb in itertools.product([0, 1], repeat=n):

        peso = sum(
            pesos[i]
            for i in range(n)
            if comb[i] == 1
        )

        if peso <= capacidade:

            valor = sum(
                valores[i]
                for i in range(n)
                if comb[i] == 1
            )

            if valor > melhor:
                melhor = valor

    return melhor


# ----------------------------------------------------------
# 2. Heurística Gulosa
# ----------------------------------------------------------

def mochila_gulosa(pesos, valores, capacidade):

    n = len(pesos)

    # Calcula valor/peso de cada item
    densidade = [
        (valores[i] / pesos[i], i)
        for i in range(n)
    ]

    # Ordena da maior densidade para a menor
    densidade.sort(reverse=True)

    valor_total = 0
    peso_atual = 0

    for dens, i in densidade:

        if peso_atual + pesos[i] <= capacidade:

            peso_atual += pesos[i]
            valor_total += valores[i]

    return valor_total


# ----------------------------------------------------------
# 3. Função para calcular o gap
# ----------------------------------------------------------

def calcular_gap(valor_heuristica, valor_otimo):

    if valor_otimo == 0:
        return 0

    gap = (
        (valor_otimo - valor_heuristica)
        / valor_otimo
    ) * 100

    return gap


# ----------------------------------------------------------
# 4. Experimento: várias instâncias aleatórias
# ----------------------------------------------------------

np.random.seed(42)

n_itens = 12
capacidade = 30
n_instancias = 20

gaps = []

print("Rodando", n_instancias, "instâncias...")

for k in range(n_instancias):

    # Gera pesos aleatórios
    pesos = np.random.randint(
        1,
        15,
        size=n_itens
    )

    # Gera valores aleatórios
    valores = np.random.randint(
        10,
        50,
        size=n_itens
    )

    # Calcula solução ótima
    otimo = mochila_otima(
        pesos,
        valores,
        capacidade
    )

    # Calcula solução gulosa
    heur = mochila_gulosa(
        pesos,
        valores,
        capacidade
    )

    # Calcula o gap
    gap = calcular_gap(
        heur,
        otimo
    )

    # Guarda o gap
    gaps.append(gap)

    print(
        f"Instância {k+1:2d} | "
        f"Ótimo: {otimo:4d} | "
        f"Gulosa: {heur:4d} | "
        f"Gap: {gap:5.1f}%"
    )


# ----------------------------------------------------------
# 5. Estatísticas finais
# ----------------------------------------------------------

print("\n===== RESUMO =====")

print(
    f"Gap médio     : {np.mean(gaps):.2f}%"
)

print(
    f"Gap mínimo    : {np.min(gaps):.2f}%"
)

print(
    f"Gap máximo    : {np.max(gaps):.2f}%"
)

print(
    f"Desvio padrão : {np.std(gaps):.2f}%"
)

# 20.	Valor do gap medio obtido.

===== RESUMO =====
Gap médio     : 0.39%
Gap mínimo    : 0.00%
Gap máximo    : 4.19%
Desvio padrão : 1.03%

# 21.	Resposta: “A heuristica gulosa e boa o suficiente para este problema? Em quais situacoes voce usaria ela e em quais preferiria gastar mais tempo para achar o otimo?”
Neste cenário acima a heuristica gulosa, poderia não ser boa suficiente para este problema, pois neste cenário ela iria focar no item que tem mais valor e com isso ela poderia cometer um erro, ou seja, por ela ter escolhido o item de mais valor, ela poderia perder a chance de fazer uma combinação de itens, que seria melhor, pois heuristica gulosa ela é mais rápida porém ela não garante eficiência 100%. Já o ótimo seria o mais ideal por mais que houvesse mais tempo na análise, porém ele varia várias combinações sendo mais assertivo e podendo até mesmo colocando mais itens de forma otimizada.

Relatório **LAB04**

Atividade 4 - Problema: Lista de Compras com Orçamento Limitado
1. Descrição clara do problema em linguagem natural
O objetivo é montar uma lista de compras para o mês, selecionando itens disponíveis em um supermercado, de forma a não exceder um orçamento total pré-definido. Cada item tem um custo e uma 'utilidade' associada (que representa o quão desejável ou necessário o item é para o comprador). O problema consiste em escolher quais itens comprar para maximizar a utilidade total, respeitando o limite do orçamento.

2. Modelagem Formal
O que é uma solução (como você representa uma solução candidata)?
Uma solução candidata pode ser representada como um vetor binário  X=(x1,x2,...,xn) , onde  n  é o número total de itens disponíveis para compra. Cada  xi  é 1 se o item  i  for incluído na lista de compras e 0 caso contrário.

3. Classificação: você considera este problema “fácil” ou “difícil”? Justifique.
Este problema é considerado difícil (NP-difícil). Ele é uma variação do famoso Problema da Mochila (Knapsack Problem). Embora existam algoritmos pseudo-polinomiais para o Problema da Mochila (como programação dinâmica), a complexidade desses algoritmos depende do tamanho do orçamento, e não do número de itens, o que os torna intratáveis para orçamentos muito grandes. Para instâncias gerais com muitos itens e orçamentos significativos, a busca exaustiva é impraticável, e encontrar a solução ótima requer algoritmos mais complexos ou heurísticas para soluções aproximadas.
