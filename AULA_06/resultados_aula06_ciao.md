# lab01_aula06_ciao

<img width="787" height="457" alt="image" src="https://github.com/user-attachments/assets/80f724a2-6f45-4d92-93ea-574d22b1ff06" />
<img width="873" height="658" alt="image" src="https://github.com/user-attachments/assets/09c4c128-6c33-4420-a2fc-f864dc84c2ae" />
<img width="823" height="655" alt="image" src="https://github.com/user-attachments/assets/a0aea916-89fc-4157-a011-fcc94d5c8211" />

Depois responda às questões abaixo:

1. Por que o ACO utiliza várias formigas em vez de apenas uma formiga procurando a melhor rota? Explique qual é a importância de explorar diferentes caminhos.

RESPOSTA: 

Olhando para a aula de hoje ao entender sobre o ACO (OTIMIZAÇÃO DE COLÔNIA DE FORMIGAS), nós entendemos que este ACO utiliza várias formigas ao invés de uma, para otimizar a rota e subsequente a rota melhor que a colônia de formigas irá prosseguir, pois pelo Raciocínio que o professor nos passou se fosse somente uma formiga, está formiga devido sua limitação numérica (singular) poderia de uma forma mais fácil cair ou seguir uma rota ruim. Na nossa opinião como um Grupo (Luis/Gustavo/Lucas) entendemos que o ACO auxilia e assim tem como importância a otimização de rota, pois como estamos falando de colônias, ou seja vários seres vivos, a forma de análise de rota se expande e melhora a análise sendo mais assertiva para que todos os indivíduos da colônia tenham a conclusão da melhor rota, tanto em questão de distância como também em melhor custo para sair do ponto Origem e chegar ao ponto de destino.

2. Por que uma rota de menor custo recebe mais feromônio? Explique como essa regra influencia o comportamento das próximas formigas.

RESPOSTA: 

Muito interessante esta pergunta, nós entendemos que a rota maior ela recebe menos feromônio devido a rota maior ela ser menos favorável para e pior em otimização, com isso ela se torna um caminho ruim, por isso as formigas enviaram menos feromônio entre si, por que elas entenderam que a rota e ruim e que não valerá a pena a emissão de feromônio, pois o custo é ruim. Já em outro cenário que é da rota otimizada, ou seja, a que possui menor custo então essa rota receberá mais feromônio, por que a colônia de formigas irá identificar de forma mais otimização e correta esta melhor rota com o melhor custo e elevará a emissão do feromônio para que as demais formigas da colônia entendam que é mais vantajoso e atrativo a rota e assim siga conforme a colônia para esta rota de melhor custo, distância e etc.


3. O que poderia acontecer se não existisse evaporação do feromônio? Explique por que manter para sempre as primeiras informações encontradas poderia prejudicar a busca por soluções melhores.

RESPOSTA: 

Entendendo esta questão nós entramos na seguinte conclusão: que se o feromônio não fosse evaporado ele poderia influenciar de forma negativamente nas próximas analises da colônia de formigas, ou seja, o rastro dele poderia impactar de forma negativa o resultado final e a otimização ficaria influenciada em uma rota ruim e de custos elevados (não vantajosos para a colônia). Com isso entendemos que manter as primeiras informações encontradas poderia sim prejudicar a busca por soluções melhores, por que se o feromônio não evaporasse, ele poderia assim influenciar/atraindo a colônia para aquela rota antiga que não seria de melhor custo, distância e etc, ou seja, não traria benefícios para a colônia em um todo, pois ela poderia focar em uma só rota, ou na primeira rota analisada, colocando em xeque a análise. Até mesmo poderíamos falar que se o feromônio não evaporasse não haveria algoritmo, pois sempre esta rota estaria lincado/escolhida a uma rota antiga para sempre.

# lab02_aula06_ciao


# outputs

<img width="454" height="151" alt="image" src="https://github.com/user-attachments/assets/7ecef69a-b175-4ff2-a5ae-29f80c0d4e00" />
<img width="855" height="460" alt="image" src="https://github.com/user-attachments/assets/4b70ba83-27f5-4ebc-8d1a-e20c303cd340" />
<img width="843" height="464" alt="image" src="https://github.com/user-attachments/assets/4009b9f2-57b9-4c5f-a212-c293c8e3dee4" />

### Quando aumentamos o ALPHA, a influência da experiência acumulada pelas formigas aumenta ou diminui?

A influencia aumenta
### A pergunta principal é: O que acontece quando o algoritmo esquece rapidamente as experiências anteriores?

Perda da Memória Coletiva: O feromônio depositado pelas formigas nas iterações anteriores é destruído quase que imediatamente antes de ser reforçado. A colônia perde a capacidade de acumular aprendizado ao longo do tempo.Comportamento Quase Aleatório (Busca Cega): Sem a retenção do feromônio para orientar a preferência pelos caminhos mais promissores, as formigas voltam a escolher rotas baseando-se praticamente apenas na atratividade inicial (custo do enlace, controlado pelo $\beta$). O algoritmo passa a se comportar como uma sequência de buscas aleatórias independentes a cada iteração.Dificuldade de Convergência e Instabilidade: A curva de convergência se torna instável ou "estagna" precocemente em níveis subótimos, pois os caminhos bons não conseguem se destacar do restante do grafo. As formigas não entram em consenso sobre a rota ideal.

======================================================================================================================================

**LAB 03**

<img width="737" height="418" alt="image" src="https://github.com/user-attachments/assets/f565943c-2bc1-4b44-a829-11baf43579f2" />

<img width="965" height="464" alt="image" src="https://github.com/user-attachments/assets/30ed4a99-a067-42fb-a664-78fa16cc3fa8" />

<img width="680" height="521" alt="image" src="https://github.com/user-attachments/assets/af8ddf23-5437-48a6-a8c4-84aeb43802b7" />


1 - Por que a fórmula da atratividade utiliza 1 / custo em vez de utilizar diretamente o custo?

RESPOSTA: 

Por que utilizamos o 1 na atratividade para deixa os caminhos menores ou mais baratos mais atrativos em vez de deixar um caminho que seria longo mais atrativo sendo que não é o que queremos e sim o oposto por exemplo m caminho com custo de 2 tem uma atratividade de 0.5 e Um caminho com custo de 1 tem uma atratividade de 1.0.

2 - O que acontece com a atratividade quando uma rota recebe mais feromônio?

RESPOSTA: 

Quando a rota recebe mais feromônios a atratividade aumenta sendo assim, quanto mais feromônios mais a rota fica atrativa para as formigas e assim tem mais chances de serem escolhidas.

3 - Por que a função construir_rota() precisa impedir que a formiga visite novamente um nó que já está na rota?


RESPOSTA: 

Pois evita ciclos infinitos e possibilita que as formigas percorram todas as rotas e escolha a melhor rota além de ajudar na eficiência do código e ajudar a ter resposta simples.

#LAB 04

<img width="768" height="544" alt="image" src="https://github.com/user-attachments/assets/e7e1a934-1186-415e-a939-ecab711640d0" />

Questões finais:

1 - Explique, com suas palavras, como o feromônio ajuda o ACO a aprender quais caminhos são melhores.

RESPOSTA: 

Em nosso raciocínio o feromônio ajuda a atrair as formigas da colônia para um caminho/rota, ou seja o feromônio pode atuar como se fosse uma memória que fica sempre pronta a mostrar o melhor caminho e faz com que as demais formigas consigam ser atraídas/envolvidas nesta rota otimizada pelo algoritmo com o melhor custo e distância. Com isso este feromônio ajuda a ACO a aprender as melhores rotas por que ele só será emitido na melhor rota analisada pela colônia, e as rotas ruim logo serão evaporadas, para que não fique na memória e não prejudique a colônia de formigas a tomarem a pior decisão.

2 - Qual é a diferença entre explorar novos caminhos e aproveitar caminhos que já demonstraram ser bons?

RESPOSTA:

Em nosso raciocínio explorar novos caminhos significa tentar alternativas que ainda não foram muito utilizadas, buscando descobrir uma solução melhor, com melhor custo, melhor distância e etc. Aproveitar caminhos já conhecidos significa dar preferência às rotas que já apresentaram bons resultados e possuem maior quantidade de feromônio, pois assim ficará guardado na memória e assim, a colônia sempre identificará pela concentração maior de feromônio neste caminho já conhecido. Com isso concluímos que o "ACO" precisa equilibrar essas duas estratégias, pois explorar permite encontrar novas soluções analisando sempre o que melhor para a colônia, enquanto aproveitar permite utilizar as soluções que já demonstraram ser boas, que ficaram na memória através do seu feromônio que estará envolvendo as formigas.

3 - Se você precisasse melhorar o desempenho desse ACO para uma rede muito maior, qual parâmetro ou parte do algoritmo você investigaria primeiro? Justifique.

RESPOSTA:

Entramo na conclusão que usaríamos o parâmetro de rede muito maior, nós investigaríamos primeiro o número de formigas (NUM_FORMIGAS). Isso porque uma rede maior possui muito mais possibilidades de caminhos, e também otimizaria a análise de forma mais eficiente com mais rotas e custos analisados, já em outro cenário se colocássemos como parâmetro com poucas formigas, o algoritmo poderia não explorar uma quantidade suficiente de alternativas, ou seja, poderia ser levado a um chute de rota melhor, ou então não teria tanta informação necessária para orientar e tomar a melhor decisão. Por tanto nós concluímos que aumentar o número de formigas pode melhorar a exploração da rede (pluralidade) e aumentar a chance de encontrar boas rotas. Porém, também seria necessário observar o tempo de execução, pois mais formigas significam mais cálculos e ai neste caso teríamos que otimizar e levar em consideração a melhor rota/distância, melhor custo e melhor tempo para um melhor trajeto do ponto de origem até o ponto de destino/chegada.
