lab03_aula09

# Definição do problema

Irrigação automática

A ideia será criar um sistema fuzzy que determine quanto tempo o sistema deve irrigar uma plantação, considerando duas entradas:

Umidade do solo (%)
Temperatura ambiente (°C)

E uma saída:

Tempo de irrigação (minutos)

É um ótimo problema para fuzzy porque não existe uma regra rígida do tipo "se umidade < 30%, irrigue exatamente 10 minutos". A decisão depende da combinação das condições. 
  
# tipo de variavel
| Tipo      | Variável             | Unidade |
| --------- | -------------------- | ------- |
| Entrada 1 | Umidade do solo      | %       |
| Entrada 2 | Temperatura ambiente | °C      |
| Saída     | Tempo de irrigação   | minutos |

# Modelagem Universo de discurso

Vamos trabalhar com os seguintes intervalos:
| Variável             | Intervalo | Unidade |
| -------------------- | --------: | ------- |
| Umidade do solo      |   0 a 100 | %       |
| Temperatura ambiente |   10 a 40 | °C      |
| Tempo de irrigação   |    0 a 30 | minutos |

A ideia é que o sistema possa trabalhar desde um solo completamente seco até um solo completamente úmido, temperaturas entre 10 °C e 40 °C e um tempo máximo de irrigação de 30 minutos.
#Termos linguísticos  
Umidade do solo

Teremos três termos:

Baixa
Média
Alta

Exemplo:

15% → principalmente baixa
50% → principalmente média
85% → principalmente alta

Mas a classificação não será rígida. Um valor de 45%, por exemplo, pode pertencer parcialmente a baixa e média.

🌡️ Temperatura

Também teremos três termos:

Baixa
Média
Alta

Exemplo:

15 °C → temperatura baixa
25 °C → temperatura média
35 °C → temperatura alta
💧 Tempo de irrigação

A saída terá quatro termos:

Nenhuma
Curta
Média
Longa
| Termo   | Interpretação                    |
| ------- | -------------------------------- |
| Nenhuma | praticamente não precisa irrigar |
| Curta   | pouca água                       |
| Média   | quantidade moderada              |
| Longa   | bastante água                    |

# Funções de pertinência

 vamos utilizar funções triangulares e trapezoidais.
# Base de regras
| Regra | Umidade | Temperatura | → Irrigação |
| ----- | ------- | ----------- | ----------- |
| 1     | Baixa   | Baixa       | Média       |
| 2     | Baixa   | Média       | Longa       |
| 3     | Baixa   | Alta        | Longa       |
| 4     | Média   | Baixa       | Curta       |
| 5     | Média   | Média       | Média       |
| 6     | Média   | Alta        | Longa       |
| 7     | Alta    | Baixa       | Nenhuma     |
| 8     | Alta    | Média       | Nenhuma     |
| 9     | Alta    | Alta        | Curta       |

# regras fuzzy
Regra 1

SE a umidade é baixa E a temperatura é baixa, ENTÃO o tempo de irrigação é médio.

Regra 2

SE a umidade é baixa E a temperatura é média, ENTÃO o tempo de irrigação é longo.

Regra 3

SE a umidade é baixa E a temperatura é alta, ENTÃO o tempo de irrigação é longo.

Regra 4

SE a umidade é média E a temperatura é baixa, ENTÃO o tempo de irrigação é curto.

Regra 5

SE a umidade é média E a temperatura é média, ENTÃO o tempo de irrigação é médio.

Regra 6

SE a umidade é média E a temperatura é alta, ENTÃO o tempo de irrigação é longo.

Regra 7

SE a umidade é alta E a temperatura é baixa, ENTÃO o tempo de irrigação é nenhuma.

Regra 8

SE a umidade é alta E a temperatura é média, ENTÃO o tempo de irrigação é nenhuma.

Regra 9

SE a umidade é alta OU a temperatura é baixa, ENTÃO o tempo de irrigação é curta.  

# Codigo
import numpy as np
import matplotlib.pyplot as plt
Funções de pertinência
def triangular(x, a, b, c):
    """
    Função de pertinência triangular.

    a = início
    b = ponto de maior pertinência
    c = fim
    """

    x = np.asarray(x)

    resultado = np.zeros_like(x, dtype=float)

    # Subida
    subida = (x >= a) & (x <= b)
    if b != a:
        resultado[subida] = (x[subida] - a) / (b - a)

    # Descida
    descida = (x >= b) & (x <= c)
    if c != b:
        resultado[descida] = (c - x[descida]) / (c - b)

    return np.clip(resultado, 0, 1)


def trapezoidal(x, a, b, c, d):
    """
    Função de pertinência trapezoidal.

    a = início
    b = início do topo
    c = fim do topo
    d = fim
    """

    x = np.asarray(x)

    resultado = np.zeros_like(x, dtype=float)

    # Subida
    subida = (x >= a) & (x < b)
    if b != a:
        resultado[subida] = (x[subida] - a) / (b - a)

    # Topo
    topo = (x >= b) & (x <= c)
    resultado[topo] = 1.0

    # Descida
    descida = (x > c) & (x <= d)
    if d != c:
        resultado[descida] = (d - x[descida]) / (d - c)

    return np.clip(resultado, 0, 1)
Funções de pertinência da umidade
# Universo da umidade
umidade = np.linspace(0, 100, 1001)

# Funções de pertinência
umidade_baixa = trapezoidal(umidade, 0, 0, 25, 50)
umidade_media = triangular(umidade, 25, 50, 75)
umidade_alta = trapezoidal(umidade, 50, 75, 100, 100)
Gráfico da umidade
plt.figure(figsize=(10, 5))

plt.plot(umidade, umidade_baixa, label="Baixa")
plt.plot(umidade, umidade_media, label="Média")
plt.plot(umidade, umidade_alta, label="Alta")

plt.title("Funções de Pertinência - Umidade do Solo")
plt.xlabel("Umidade (%)")
plt.ylabel("Grau de pertinência")
plt.ylim(0, 1.1)
plt.grid(True)
plt.legend()

plt.show()
Funções de pertinência da temperatura
# Universo da temperatura
temperatura = np.linspace(10, 40, 1001)

# Funções de pertinência
temperatura_baixa = trapezoidal(temperatura, 10, 10, 17.5, 25)
temperatura_media = triangular(temperatura, 17.5, 25, 32.5)
temperatura_alta = trapezoidal(temperatura, 25, 32.5, 40, 40)
Gráfico da temperatura
plt.figure(figsize=(10, 5))

plt.plot(temperatura, temperatura_baixa, label="Baixa")
plt.plot(temperatura, temperatura_media, label="Média")
plt.plot(temperatura, temperatura_alta, label="Alta")

plt.title("Funções de Pertinência - Temperatura")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Grau de pertinência")
plt.ylim(0, 1.1)
plt.grid(True)
plt.legend()

plt.show()
Funções de pertinência da saída
# Universo do tempo de irrigação
tempo = np.linspace(0, 30, 1001)

# Funções de pertinência da saída
irrigacao_nenhuma = trapezoidal(tempo, 0, 0, 2, 6)
irrigacao_curta = triangular(tempo, 3, 8, 13)
irrigacao_media = triangular(tempo, 10, 15, 20)
irrigacao_longa = trapezoidal(tempo, 17, 23, 30, 30)
Gráfico da saída
plt.figure(figsize=(10, 5))

plt.plot(tempo, irrigacao_nenhuma, label="Nenhuma")
plt.plot(tempo, irrigacao_curta, label="Curta")
plt.plot(tempo, irrigacao_media, label="Média")
plt.plot(tempo, irrigacao_longa, label="Longa")

plt.title("Funções de Pertinência - Tempo de Irrigação")
plt.xlabel("Tempo de irrigação (minutos)")
plt.ylabel("Grau de pertinência")
plt.ylim(0, 1.1)
plt.grid(True)
plt.legend()

plt.show()
Função para obter a pertinência de um valor
def pertinencias_umidade(valor):
    return {
        "baixa": float(trapezoidal(np.array([valor]), 0, 0, 25, 50)[0]),
        "media": float(triangular(np.array([valor]), 25, 50, 75)[0]),
        "alta": float(trapezoidal(np.array([valor]), 50, 75, 100, 100)[0])
    }


def pertinencias_temperatura(valor):
    return {
        "baixa": float(trapezoidal(np.array([valor]), 10, 10, 17.5, 25)[0]),
        "media": float(triangular(np.array([valor]), 17.5, 25, 32.5)[0]),
        "alta": float(trapezoidal(np.array([valor]), 25, 32.5, 40, 40)[0])
    }
Regras fuzzy
def inferencia_fuzzy(valor_umidade, valor_temperatura):

    u = pertinencias_umidade(valor_umidade)
    t = pertinencias_temperatura(valor_temperatura)

    regras = []

    # Regra 1
    regras.append(("media", min(u["baixa"], t["baixa"])))

    # Regra 2
    regras.append(("longa", min(u["baixa"], t["media"])))

    # Regra 3
    regras.append(("longa", min(u["baixa"], t["alta"])))

    # Regra 4
    regras.append(("curta", min(u["media"], t["baixa"])))

    # Regra 5
    regras.append(("media", min(u["media"], t["media"])))

    # Regra 6
    regras.append(("longa", min(u["media"], t["alta"])))

    # Regra 7
    regras.append(("nenhuma", min(u["alta"], t["baixa"])))

    # Regra 8
    regras.append(("nenhuma", min(u["alta"], t["media"])))

    # Regra 9 - utiliza OU
    regras.append(("curta", max(u["alta"], t["baixa"])))

    return u, t, regras
Agregação das regras
def agregar_regras(regras):

    saida_nenhuma = np.zeros_like(tempo)
    saida_curta = np.zeros_like(tempo)
    saida_media = np.zeros_like(tempo)
    saida_longa = np.zeros_like(tempo)

    for termo, ativacao in regras:

        if termo == "nenhuma":
            saida_nenhuma = np.maximum(
                saida_nenhuma,
                np.minimum(ativacao, irrigacao_nenhuma)
            )

        elif termo == "curta":
            saida_curta = np.maximum(
                saida_curta,
                np.minimum(ativacao, irrigacao_curta)
            )

        elif termo == "media":
            saida_media = np.maximum(
                saida_media,
                np.minimum(ativacao, irrigacao_media)
            )

        elif termo == "longa":
            saida_longa = np.maximum(
                saida_longa,
                np.minimum(ativacao, irrigacao_longa)
            )

    agregada = np.maximum.reduce([
        saida_nenhuma,
        saida_curta,
        saida_media,
        saida_longa
    ])

    return agregada
Defuzzificação
def defuzzificacao(saida_agregada):

    soma = np.sum(saida_agregada)

    if soma == 0:
        return 0

    return np.sum(tempo * saida_agregada) / soma
Função completa do sistema
def sistema_irrigacao(umidade_valor, temperatura_valor):

    u, t, regras = inferencia_fuzzy(
        umidade_valor,
        temperatura_valor
    )

    saida_agregada = agregar_regras(regras)

    tempo_irrigacao = defuzzificacao(saida_agregada)

    return tempo_irrigacao, u, t, regras, saida_agregada
Primeiro teste
umidade_teste = 80
temperatura_teste = 35

resultado, u, t, regras, saida = sistema_irrigacao(
    umidade_teste,
    temperatura_teste
)

print(f"Umidade: {umidade_teste}%")
print(f"Temperatura: {temperatura_teste} °C")
print(f"Tempo de irrigação: {resultado:.2f} minutos")
Visualizar a decisão
plt.figure(figsize=(10, 5))

plt.plot(
    tempo,
    saida,
    label="Saída agregada"
)

plt.axvline(
    resultado,
    linestyle="--",
    label=f"Resultado = {resultado:.2f} min"
)

plt.title("Resultado da Inferência Fuzzy")
plt.xlabel("Tempo de irrigação (minutos)")
plt.ylabel("Grau de pertinência")
plt.ylim(0, 1.1)
plt.grid(True)
plt.legend()

plt.show()
Testes
| Teste | Umidade | Temperatura | Expectativa                      |
| ----- | ------: | ----------: | -------------------------------- |
| 1     |     80% |       20 °C | Nenhuma ou irrigação muito baixa |
| 2     |     50% |       25 °C | Irrigação média                  |
| 3     |     25% |       22 °C | Irrigação longa                  |
| 4     |     20% |       35 °C | Irrigação longa                  |

Executar os quatro testes
testes = [
    {
        "nome": "Teste 1",
        "umidade": 80,
        "temperatura": 20,
        "esperado": "Nenhuma ou muito baixa"
    },
    {
        "nome": "Teste 2",
        "umidade": 50,
        "temperatura": 25,
        "esperado": "Média"
    },
    {
        "nome": "Teste 3",
        "umidade": 25,
        "temperatura": 22,
        "esperado": "Longa"
    },
    {
        "nome": "Teste 4",
        "umidade": 20,
        "temperatura": 35,
        "esperado": "Longa"
    }
]

resultados = []

for teste in testes:

    resultado, u, t, regras, saida = sistema_irrigacao(
        teste["umidade"],
        teste["temperatura"]
    )

    resultados.append({
        "Teste": teste["nome"],
        "Umidade (%)": teste["umidade"],
        "Temperatura (°C)": teste["temperatura"],
        "Saída (min)": resultado,
        "Resposta esperada": teste["esperado"]
    })

    print(f"{teste['nome']}")
    print(f"  Umidade: {teste['umidade']}%")
    print(f"  Temperatura: {teste['temperatura']} °C")
    print(f"  Tempo calculado: {resultado:.2f} minutos")
    print(f"  Esperado: {teste['esperado']}")
    print("-" * 50)
Mostrar os resultados em tabela
import pandas as pd

tabela_resultados = pd.DataFrame(resultados)

tabela_resultados
Mostrar a ativação das regras
for teste in testes:

    resultado, u, t, regras, saida = sistema_irrigacao(
        teste["umidade"],
        teste["temperatura"]
    )

    print(f"\n{teste['nome']}")
    print(f"Umidade: {teste['umidade']}%")
    print(f"Temperatura: {teste['temperatura']} °C")
    print(f"Resultado: {resultado:.2f} minutos")

    print("\nPertinência da umidade:")
    for termo, valor in u.items():
        print(f"  {termo}: {valor:.2f}")

    print("\nPertinência da temperatura:")
    for termo, valor in t.items():
        print(f"  {termo}: {valor:.2f}")

    print("\nRegras ativadas:")

    for numero, (termo, ativacao) in enumerate(regras, start=1):
        if ativacao > 0:
            print(
                f"  Regra {numero}: "
                f"{termo} → ativação {ativacao:.2f}"
            )
Gráfico dos quatro resultados
fig, eixos = plt.subplots(2, 2, figsize=(12, 8))

for eixo, teste in zip(eixos.flatten(), testes):

    resultado, u, t, regras, saida = sistema_irrigacao(
        teste["umidade"],
        teste["temperatura"]
    )

    eixo.plot(tempo, saida)

    eixo.axvline(
        resultado,
        linestyle="--",
        label=f"{resultado:.2f} min"
    )

    eixo.set_title(
        f"{teste['nome']} - "
        f"Umidade: {teste['umidade']}% | "
        f"Temp.: {teste['temperatura']}°C"
    )

    eixo.set_xlabel("Tempo de irrigação (min)")
    eixo.set_ylabel("Pertinência")
    eixo.set_ylim(0, 1.1)
    eixo.grid(True)
    eixo.legend()

plt.tight_layout()
plt.show()

# prints
<img width="508" height="445" alt="image" src="https://github.com/user-attachments/assets/5a9d8267-4cb9-4b7b-bab8-292245bd7493" />
<img width="701" height="164" alt="image" src="https://github.com/user-attachments/assets/896a48b0-00be-4a02-8df9-20b15d19a8df" />
<img width="1177" height="717" alt="image" src="https://github.com/user-attachments/assets/5c195ac9-1c29-440c-8804-360d6e5d2dc1" />
