
# LAB 02 
output da execução


<img width="375" height="101" alt="image" src="https://github.com/user-attachments/assets/b8adbfc0-6fa1-43b3-9053-3a5cc9c81db5" />


Questões Técnicas — LAB 02

1 - Explique qual é o papel do operador de Mutação em um Algoritmo Genético e o que ocorre se a taxa de mutação for configurada em 100%.  

R: A mutação tem o papel de introduzir diversidade genética na população. Ela altera aleatoriamente alguns genes de um indivíduo, evitando que a população fique muito semelhante e ajudando o algoritmo a explorar novas soluções.

Se a taxa de mutação for configurada em 100%, todos os genes de todos os indivíduos serão invertidos a cada mutação. Isso gera uma alteração extremamente intensa na população, podendo dificultar a preservação de boas características encontradas pelo algoritmo e prejudicar a convergência. Portanto, uma taxa de mutação muito alta pode fazer o comportamento do algoritmo se aproximar de uma busca aleatória.

2 - Por que a penalização do fitness (atribuir 0 para indivíduos que estouram a capacidade) é fundamental para a convergência das restrições?

R: A penalização é fundamental porque impede que soluções que violam a restrição de capacidade sejam consideradas boas apenas por possuírem um valor total elevado.

No problema da mochila, quando total_weight > max_weight, o fitness recebe valor 0. Dessa forma, indivíduos inválidos perdem a vantagem na seleção por torneio e têm menor probabilidade de gerar descendentes.

Isso direciona a evolução para soluções que respeitam a restrição de peso e permite que o algoritmo procure boas soluções dentro do espaço viável.


# LAB 03
output da execução

<img width="656" height="49" alt="image" src="https://github.com/user-attachments/assets/46177267-7181-4b37-999a-e713c8e3a357" />


Questões Técnicas — LAB 03


1 - O que acontece com o comportamento das partículas se zerarmos a componente cognitiva (c_1 = 0)?  

R: Se c1 = 0, a componente cognitiva desaparece. Isso significa que as partículas deixam de considerar sua própria melhor posição histórica (pbest) para atualizar a velocidade.

Nesse caso, o movimento passa a depender principalmente da inércia e da componente social, que direciona as partículas para a melhor posição encontrada pelo enxame (gbest).

Isso reduz a exploração individual das partículas e aumenta a influência do comportamento coletivo.
2 - Qual a função do parâmetro de Inércia (w) na busca por mínimos globais?  

R: O parâmetro de inércia w controla quanto da velocidade anterior da partícula é mantido na próxima atualização.

Um valor maior de w tende a manter as partículas em movimento por mais tempo, favorecendo a exploração de diferentes regiões do espaço de busca.

Um valor menor de w reduz a influência da velocidade anterior, favorecendo movimentos mais controlados em direção às melhores posições encontradas.

Assim, w ajuda a controlar o equilíbrio entre exploração do espaço de busca e intensificação em regiões promissoras.

# LAB 04

<img width="552" height="115" alt="image" src="https://github.com/user-attachments/assets/6805d170-9162-4ff1-becd-e98421299466" />

1 - Por que a evaporação do feromônio é necessária no algoritmo ACO?
Ela impede a estagnação das rotas, ajuda no esquecimento de resultados obsoletos além de quando é reduzida a quantidade de feromônios faz com que sejam explorados outros caminhos e ela se adapta permitindo que o feromônio se adeque as melhores soluções que estão sendo descobertas.

2 - O que ocorreria em grafos complexos sem ela?Qual a relação matemática entre a latência de um enlace e sua atratividade inicial (eta) para as formigas?
O algoritmo se convergiria para uma solução sub ótima ou seja uma solução local e não global, a exploração de novas rotas seria mínima e sem a função limpar o algoritmo não conseguiria chegar nas melhores soluções facilmente além da incapacidade de se ajustar para achar um resultado melhor logo no inicio.


