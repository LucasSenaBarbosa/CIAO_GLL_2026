
=== LAB 01 - RESULTADOS ===

RESPOSTAS

======================================================================
EXECUÇÃO DO PSO
======================================================================

Executando PSO com 10 partículas...

Executando PSO com 30 partículas...

Executando PSO com 50 partículas...


======================================================================
RESULTADOS FINAIS
======================================================================

População: 10 partículas
Melhor distribuição W:
[0. 0. 0. 1. 0. 0.]
Soma dos pesos: 1.000000
Fitness: 30.000000
Temperaturas das AZs:
[ 0.  0.  0. 30.  0.  0.]

População: 30 partículas
Melhor distribuição W:
[0. 0. 0. 1. 0. 0.]
Soma dos pesos: 1.000000
Fitness: 30.000000
Temperaturas das AZs:
[ 0.  0.  0. 30.  0.  0.]

População: 50 partículas
Melhor distribuição W:
[0. 0. 0. 1. 0. 0.]
Soma dos pesos: 1.000000
Fitness: 30.000000
Temperaturas das AZs:
[ 0.  0.  0. 30.  0.  0.]


======================================================================
TABELA COMPARATIVA
======================================================================
Partículas	w1	w2	w3	w4	w5	w6	Soma	Fitness
0	10	0.0	0.0	0.0	1.0	0.0	0.0	1.0	30.0
1	30	0.0	0.0	0.0	1.0	0.0	0.0	1.0	30.0
2	50	0.0	0.0	0.0	1.0	0.0	0.0	1.0	30.0



======================================================================
VALIDAÇÃO DA SOMA DOS PESOS
======================================================================
10 partículas -> Soma = 1.000000000000 -> VÁLIDO
30 partículas -> Soma = 1.000000000000 -> VÁLIDO
50 partículas -> Soma = 1.000000000000 -> VÁLIDO

======================================================================
RESUMO
======================================================================

10 partículas:
  Fitness = 30.000000
  Soma(W) = 1.000000
  Melhor W = [0. 0. 0. 1. 0. 0.]

30 partículas:
  Fitness = 30.000000
  Soma(W) = 1.000000
  Melhor W = [0. 0. 0. 1. 0. 0.]

50 partículas:
  Fitness = 30.000000
  Soma(W) = 1.000000
  Melhor W = [0. 0. 0. 1. 0. 0.]

<img width="812" height="443" alt="image" src="https://github.com/user-attachments/assets/a16c6e40-4069-4c18-aa99-cfb66ed4ef6d" />
<img width="807" height="443" alt="image" src="https://github.com/user-attachments/assets/5b3f54a3-7101-4558-87e1-ad8b884bab95" />

-------------------------------------------------------------------------------------------------------------------------------------------------


=== LAB 02 ===

RESPOSTAS

======================================================================
ESTRATÉGIA A — PENALIDADE RÍGIDA
======================================================================


======================================================================
ESTRATÉGIA B — PENALIDADE PROPORCIONAL
======================================================================


======================================================================
ESTRATÉGIA A — PENALIDADE RÍGIDA
======================================================================

Cromossomo:
[0 1 0 1 0 0 0 1 0 1 0 1 0 1 1]

Serviços selecionados:
  Servico_02
  Servico_04
  Servico_08
  Servico_10
  Servico_12
  Servico_14
  Servico_15

Valor de negócio: 520.00
RAM utilizada: 13.50 GB
CPU utilizada: 8.00 cores
Fitness: 520.00

RAM <= 16 GB: OK
CPU <= 8 cores: OK


======================================================================
ESTRATÉGIA B — PENALIDADE PROPORCIONAL
======================================================================

Cromossomo:
[0 1 0 1 0 0 0 1 0 1 0 1 0 1 1]

Serviços selecionados:
  Servico_02
  Servico_04
  Servico_08
  Servico_10
  Servico_12
  Servico_14
  Servico_15

Valor de negócio: 520.00
RAM utilizada: 13.50 GB
CPU utilizada: 8.00 cores
Fitness: 520.00

RAM <= 16 GB: OK
CPU <= 8 cores: OK


======================================================================
COMPARAÇÃO DAS ESTRATÉGIAS
======================================================================
Estratégia	Fitness Final	Valor de Negócio	RAM (GB)	CPU (Cores)	Diversidade Final
0	Penalidade Rígida	520.0	520	13.5	8.0	0.1114
1	Penalidade Proporcional	520.0	520	13.5	8.0	0.1205



======================================================================
SERVIÇOS — ESTRATÉGIA A
======================================================================
Servico	Valor	RAM	CPU
0	Servico_02	70	2.0	1.0
1	Servico_04	60	1.5	1.0
2	Servico_08	50	1.0	0.5
3	Servico_10	75	2.0	1.0
4	Servico_12	65	1.5	1.0
5	Servico_14	85	2.5	1.5
6	Servico_15	115	3.0	2.0


======================================================================
SERVIÇOS — ESTRATÉGIA B
======================================================================
Servico	Valor	RAM	CPU
0	Servico_02	70	2.0	1.0
1	Servico_04	60	1.5	1.0
2	Servico_08	50	1.0	0.5
3	Servico_10	75	2.0	1.0
4	Servico_12	65	1.5	1.0
5	Servico_14	85	2.5	1.5
6	Servico_15	115	3.0	2.0

<img width="860" height="465" alt="image" src="https://github.com/user-attachments/assets/cce99b36-38ae-4377-b826-fd1d3647b94f" />
<img width="864" height="471" alt="image" src="https://github.com/user-attachments/assets/5dd06c6e-27fb-4d16-9df4-a59fdce65dc6" />
<img width="852" height="474" alt="image" src="https://github.com/user-attachments/assets/67349cc2-6aae-4221-9fba-6344ec4786ae" />
<img width="850" height="480" alt="image" src="https://github.com/user-attachments/assets/014250bf-59f6-4ee5-9453-8dcdcba1a85e" />

======================================================================
EVOLUÇÃO DAS ESTRATÉGIAS
======================================================================
Geração	Média - Rígida	Desvio - Rígida	Melhor - Rígida	Diversidade - Rígida	Média - Proporcional	Desvio - Proporcional	Melhor - Proporcional	Diversidade - Proporcional
0	1	30.1	103.3029	445.0	0.4929	100.6219	152.8826	473.4375	0.4929
1	2	63.0	136.5833	430.0	0.4746	205.1938	163.8066	492.1875	0.4721
2	3	155.6	179.1554	440.0	0.4175	301.5281	117.3282	492.1875	0.4003
3	4	190.6	186.7823	460.0	0.3851	343.8094	131.9795	465.0000	0.3887
4	5	190.8	182.5469	480.0	0.3459	354.2625	114.8067	470.0000	0.3620
...	...	...	...	...	...	...	...	...	...
95	96	307.6	226.5287	520.0	0.1361	438.5531	85.7880	520.0000	0.1463
96	97	331.8	223.6241	520.0	0.1263	432.7844	119.6393	520.0000	0.1415
97	98	280.8	242.9164	520.0	0.1311	418.9562	138.7353	520.0000	0.1462
98	99	291.9	242.1918	520.0	0.1259	426.8938	109.0378	520.0000	0.1314
99	100	300.9	238.7817	520.0	0.1114	422.9250	128.9385	520.0000	0.1205
100 rows × 9 columns



======================================================================
RESUMO FINAL
======================================================================

ESTRATÉGIA A — PENALIDADE RÍGIDA
Fitness final: 520.00
Valor de negócio: 520.00
RAM: 13.50 GB
CPU: 8.00 cores
Diversidade final: 0.1114

ESTRATÉGIA B — PENALIDADE PROPORCIONAL
Fitness final: 520.00
Valor de negócio: 520.00
RAM: 13.50 GB
CPU: 8.00 cores
Diversidade final: 0.1205


======================================================================
EXECUÇÃO CONCLUÍDA

-------------------------------------------------------------------------------------------------------------------------------------------------------------

=== LAB 03 === 

RESPOSTAS: 

Matriz D validada com sucesso.


======================================================================
EXECUTANDO ACO
======================================================================


======================================================================
VALIDAÇÃO DA SOLUÇÃO ACO
======================================================================
Número de switches: 10
Número de arestas: 9
Esperado para árvore: 9
Árvore válida: SIM


======================================================================
MELHOR TOPOLOGIA ENCONTRADA PELO ACO
======================================================================
Switch 5 <--> Switch 6 | Latência = 5.00
Switch 1 <--> Switch 2 | Latência = 4.00
Switch 8 <--> Switch 10 | Latência = 7.00
Switch 7 <--> Switch 10 | Latência = 6.00
Switch 8 <--> Switch 9 | Latência = 9.00
Switch 4 <--> Switch 6 | Latência = 6.00
Switch 3 <--> Switch 4 | Latência = 7.00
Switch 2 <--> Switch 3 | Latência = 6.00
Switch 6 <--> Switch 7 | Latência = 7.00

Latência total ACO: 57.00


======================================================================
MATRIZ DE ADJACÊNCIA FINAL — ACO
======================================================================
[[0 1 0 0 0 0 0 0 0 0]
 [1 0 1 0 0 0 0 0 0 0]
 [0 1 0 1 0 0 0 0 0 0]
 [0 0 1 0 0 1 0 0 0 0]
 [0 0 0 0 0 1 0 0 0 0]
 [0 0 0 1 1 0 1 0 0 0]
 [0 0 0 0 0 1 0 0 0 1]
 [0 0 0 0 0 0 0 0 1 1]
 [0 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 0 1 1 0 0]]

Matriz de adjacência formatada:
S1	S2	S3	S4	S5	S6	S7	S8	S9	S10
S1	0	1	0	0	0	0	0	0	0	0
S2	1	0	1	0	0	0	0	0	0	0
S3	0	1	0	1	0	0	0	0	0	0
S4	0	0	1	0	0	1	0	0	0	0
S5	0	0	0	0	0	1	0	0	0	0
S6	0	0	0	1	1	0	1	0	0	0
S7	0	0	0	0	0	1	0	0	0	1
S8	0	0	0	0	0	0	0	0	1	1
S9	0	0	0	0	0	0	0	1	0	0
S10	0	0	0	0	0	0	1	1	0	0




======================================================================
COMPARAÇÃO ACO x TOPOLOGIA ALEATÓRIA
======================================================================
Latência da topologia aleatória: 125.00
Latência da topologia ACO: 57.00
Ganho percentual de redução: 54.40%


======================================================================
MATRIZ DE ADJACÊNCIA — TOPOLOGIA ALEATÓRIA
======================================================================
S1	S2	S3	S4	S5	S6	S7	S8	S9	S10
S1	0	0	0	0	1	0	0	0	0	0
S2	0	0	1	1	0	0	0	0	0	0
S3	0	1	0	0	1	0	0	1	0	1
S4	0	1	0	0	0	0	0	0	1	0
S5	1	0	1	0	0	0	1	0	0	0
S6	0	0	0	0	0	0	0	1	0	0
S7	0	0	0	0	1	0	0	0	0	0
S8	0	0	1	0	0	1	0	0	0	0
S9	0	0	0	1	0	0	0	0	0	0
S10	0	0	1	0	0	0	0	0	0	0

<img width="859" height="473" alt="image" src="https://github.com/user-attachments/assets/6be6570b-0b5b-41df-8e12-9feba91d065a" />

======================================================================
TABELA COMPARATIVA
======================================================================
Topologia	Número de Arestas	Latência Total
0	Aleatória	9	125.0
1	ACO	9	57.0


======================================================================
RESUMO FINAL DO LAB 03
======================================================================

Latência aleatória: 125.00
Latência ACO: 57.00
Redução obtida: 54.40%

Quantidade de arestas: 9
Árvore válida: SIM

Matriz de adjacência ACO:
[[0 1 0 0 0 0 0 0 0 0]
 [1 0 1 0 0 0 0 0 0 0]
 [0 1 0 1 0 0 0 0 0 0]
 [0 0 1 0 0 1 0 0 0 0]
 [0 0 0 0 0 1 0 0 0 0]
 [0 0 0 1 1 0 1 0 0 0]
 [0 0 0 0 0 1 0 0 0 1]
 [0 0 0 0 0 0 0 0 1 1]
 [0 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 0 1 1 0 0]]


======================================================================
EXECUÇÃO CONCLUÍDA

