**LAB01**

<img width="1203" height="776" alt="image" src="https://github.com/user-attachments/assets/a5f265e8-1f9d-4398-962d-b3597445d340" />

**LAB02**

<img width="1751" height="655" alt="image" src="https://github.com/user-attachments/assets/bc82bede-bc50-4914-9aab-8aec06b49a4d" />

**LAB03**

<img width="579" height="301" alt="image" src="https://github.com/user-attachments/assets/28597404-717c-466c-a57d-9d050dca1a12" />

**LAB04**

O objetivo principal deste projeto foi desenvolver e aplicar um algoritmo genético para a seleção da rota de menor custo entre o Nó 0 (origem) e o Nó 11 (destino) em uma topologia de rede com 12 roteadores. A função de fitness foi construída para otimizar a rota considerando múltiplos atributos de enlace e nó: Latência (`ms`), Taxa de Perda de Pacotes (`%`) e Reputação de Segurança dos Roteadores. Penalizações foram incorporadas para desvios de SLA e para o uso de nós com reputação de segurança inadequada.

Este relatório mostra a aplicação de um algoritmo genético para encontrar a rota de menor custo entre o Nó 0 e o Nó 11 em uma rede de 12 roteadores. A função de fitness foi otimizada para minimizar a latência e a perda de pacotes, enquanto penaliza rotas que utilizam roteadores com reputação de segurança inferior a 50. A melhor rota encontrada foi [0, 2, 4, 7, 10, 11], com uma latência de 148.37 ms, perda de pacotes de 14.35%, e um fitness final de 5291.84. A rota inclui roteadores não confiáveis (Nó 0 e Nó 4), resultando em uma penalização de segurança de 5000.00. A inclusão desses nós é justificada por um trade-off necessário para alcançar o menor fitness global, dadas as métricas de latência e perda dos enlaces, e a conectividade da rede.

Desta forma, nesta aplicação sendo aplicado na integra como aprendemos em sala de aula com o professor, vimos a analise do algoritmo para achar a melhor rota obedecendo a risca as restrições embosta pelo desafio, otimizando e automatizando a rota colocando sempre na pauta a melhor rota possível e correta para chegar com o grau de elitismo em auto nível de confiabilidade.

<img width="720" height="233" alt="image" src="https://github.com/user-attachments/assets/462d3cf3-2255-4f53-af6a-6839f515300c" />

<img width="1037" height="570" alt="image" src="https://github.com/user-attachments/assets/a239823a-f3a0-444c-aa3e-63b345d20f6b" />


