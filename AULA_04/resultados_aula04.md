**LAB01**

<img width="1203" height="776" alt="image" src="https://github.com/user-attachments/assets/a5f265e8-1f9d-4398-962d-b3597445d340" />

**LAB02**

<img width="1751" height="655" alt="image" src="https://github.com/user-attachments/assets/bc82bede-bc50-4914-9aab-8aec06b49a4d" />

**LAB03**

<img width="579" height="301" alt="image" src="https://github.com/user-attachments/assets/28597404-717c-466c-a57d-9d050dca1a12" />

**LAB04**

Relatório Técnico: Seleção de Rota Otimizada
1. Objetivo:

O objetivo deste estudo foi determinar a rota de menor custo entre um nó de origem fixo (Nó 0) e um nó de destino fixo (Nó 11) em uma topologia de 12 roteadores, utilizando um algoritmo genético. A função de fitness foi projetada para otimizar a rota com base em múltiplos parâmetros de enlace: latência, taxa de perda de pacotes e reputação de segurança, com penalizações específicas para violações de limites de serviço (SLA) e para o uso de nós considerados não confiáveis.

2. Parâmetros do Algoritmo Genético:

Número de Nós (N_NOS): 12
Origem Fixa (ORIGEM_NO): 0
Destino Fixo (DESTINO_NO): 11
Semente Aleatória: 2026
Pesos da Função de Fitness: W1 (Latência) = 0.5, W2 (Perda de Pacotes) = 0.5
Penalização de Segurança (P_SEGURANCA_VALOR): 5000 (aplicada se qualquer nó na rota tiver reputação < 50)
Limite de Latência (LIMITE_ENLACE): 50.0 ms
Penalidade por Violação de Latência (PENALIDADE): 1000.0
3. Rota Otimizada Selecionada:

Após 150 gerações, o algoritmo genético convergiu para a seguinte melhor rota:

Melhor Rota Encontrada: [0, 10, 7, 9, 4, 1, 8, 5, 3, 6, 2, 11]

4. Análise de Fitness da Rota Otimizada:

Latência Total da rota: 237.95 ms
Perda de Pacotes Total da rota: 37.86 %
Penalidade SLA de Latência: 0.00 (indicando que nenhum enlace na rota excede o LIMITE_ENLACE de 50ms para latência)
Penalidade de Segurança: 5000.00
Fitness Final: 5137.91
5. Justificativa para o Desvio em Relação aos Nós Penalizados:

A penalidade de segurança de 5000.00 no fitness final indica que, embora a rota seja a melhor encontrada pelo algoritmo genético, ela ainda inclui pelo menos um nó com reputação de segurança inferior a 50. Para entender o porquê o algoritmo optou por incluir um nó penalizado, devemos considerar a natureza do algoritmo genético e a função de fitness:

Comprometimento (Trade-off): A função de fitness é uma combinação ponderada de latência, perda de pacotes e a penalidade de segurança. É provável que as rotas alternativas que evitariam completamente nós não confiáveis tivessem um custo total de latência ou perda de pacotes significativamente maior, resultando em um fitness geral ainda pior (ou seja, um valor mais alto, que é menos desejável). O algoritmo busca o mínimo global de fitness, e isso pode significar aceitar uma penalidade de segurança para obter um desempenho muito melhor nas outras métricas.

Conectividade e Topologia: A topologia da rede e a distribuição dos nós confiáveis/não confiáveis podem limitar as opções. Se não houver uma rota viável entre a origem e o destino que consista apenas em nós confiáveis, ou se tais rotas forem excessivamente longas ou de alta latência/perda, o algoritmo será forçado a utilizar nós com reputação de segurança mais baixa para manter a conectividade ou otimizar as outras métricas.

Valor da Penalidade: A penalidade de segurança (5000) é um valor fixo e considerável. No entanto, se o custo de desviar de um nó não confiável (por exemplo, adicionando muitos nós extras ou enlaces de alta latência/perda) for maior que 5000, o algoritmo priorizará a rota que inclui o nó não confiável, mas que é globalmente mais eficiente.

Para esta execução específica, a presença da Penalidade de Segurança: 5000.00 no resultado final significa que a melhor rota encontrada contém pelo menos um nó (reputacao_seguranca_nos[no] < 50). Por exemplo, olhando a lista de reputações de segurança dos nós: [9, 82, 10, 53, 3, 20, 7, 32, 91, 27, 17, 0], podemos ver que os nós 0, 2, 4, 5, 6, 7, 9, 10 e 11 são considerados não confiáveis. Como o nó de origem (0) e de destino (11) são ambos considerados não confiáveis (reputação < 50), a penalidade de 5000 é inevitável neste cenário, pois ambos estão presentes em qualquer rota válida.

6. Conclusão:

O algoritmo genético forneceu uma rota otimizada que balanceia as métricas de latência e perda de pacotes, ao mesmo tempo em que considera as penalizações de SLA e segurança. A rota encontrada é a que minimiza o valor da função de fitness, mesmo que isso inclua a aceitação da penalidade de segurança. Para evitar completamente nós não confiáveis, seria necessário reavaliar a topologia da rede, a disponibilidade de nós confiáveis ou ajustar os pesos e valores das penalizações para refletir uma prioridade maior na segurança em detrimento de outras métricas.

Desta forma, nesta aplicação sendo aplicado na integra como aprendemos em sala de aula com o professor, vimos a analise do algoritmo para achar a melhor rota obedecendo a risca as restrições embosta pelo desafio, otimizando e automatizando a rota colocando sempre na pauta a melhor rota possível e correta para chegar com o grau de elitismo em auto nível de confiabilidade.

<img width="720" height="233" alt="image" src="https://github.com/user-attachments/assets/462d3cf3-2255-4f53-af6a-6839f515300c" />

<img width="1037" height="570" alt="image" src="https://github.com/user-attachments/assets/a239823a-f3a0-444c-aa3e-63b345d20f6b" />


