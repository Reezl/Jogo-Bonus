# Jogo-Bonus

Protocolo: **UDP**<br>
Arquitetura: **Cliente-Servidor**<br>

<br>
O jogo(protótipo) foi desenvolvido em UDP para uma melhor qualidade do streaming. Apesar de 
que usando TCP em uma conexão local, não faria tanta diferença.<br>

#### Como funciona? -<br>
Bom, cada cliente manda para o servidor(main) uma string informando qual cliente é, por exemplo, o cliente 1
manda uma string dizendo 'Cliente 1'. Assim o servidor irá reconhece-lo como cliente 1. O mesmo acontece para o
cliente 2.<br>
Após já configurado ambos clientes, os clientes irão mandar a todo o tempo sua localização na screen(tela do jogo).
O servidor já sabendo quais os ip's de cada cliente, envia para um cliente a localização do outro, exemplo: 
Cliente 1 [(x,y)] <-- Posições do Cliente 1 acabou de chegar, então envie para Cliente 2 [(x,y)] <-- Pertecentes ao Cliente 1.
