Centroide
<img width="998" height="498" alt="image" src="https://github.com/user-attachments/assets/ddd0983d-1bf1-4a7b-bd28-f4cf76887251" />

1. Por que o método do Centroide com triângulos não atinge matematicamente os extremos 0% e 100%?

Resposta: Porque esse método calcula o centro da massa, sendo assim ele impossibilita de calcular as extremidades exatas pois o foco dele é no meio do gráfico

2. O que acontece com o resultado final se alterarmos a função da Urgência Crítica para Trapézio (trapmf) na borda superior (Abordagem A)?

Resposta: Como ainda utilizamos o método do Centroide para defuzzificação, o cálculo ponderado da área acumulada do trapézio continua puxando o centro de massa ligeiramente para a esquerda

3. O que acontece se alterarmos o método de defuzzificação para 'MOM' (Mean of Maximum)? Qual abordagem é mais recomendável e por quê?

Resposta: O método MOM identifica o valor onde a função de pertinência agregada atinge o seu grau máximo absoluto de pertinência.

O que acontece: A Abordagem B com MOM consegue cravar exatamente 0.00% e 100.00% nos limites das regras extremas, pois ele ignora a distribuição geométrica da área e foca apenas no ponto de pico.
