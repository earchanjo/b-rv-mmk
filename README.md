# b-rv-mmk



Fala, Thauan. Sou o programador que entrou na equipe do tom.
Nunca mexi com web3 ou coisa parecida, então ja deixo minhas desculpas pelo "go horse" em partes do codigo :(
Eu fiz o bot para tirar a quantia exata (desde que seja possivel com o minimo de gas) da conta, dessa quantia tirada 5 gwei de gas e puxamos
o restante para uma conta laranja.

Como voce tinha visto no código anterior ele funcionava(ainda funciona) sequencialmente em um unico loop saindo as transações em seguida.
Coloquei condicoes de "se conta tiver mais que 0.0001 faça transacao", para garantir que ele só tiraria quando tivesse algo. (menos que 0.0001 nao tem fracao pra gas).
porém estamos com o seguinte problema:

1 - Dado que ele já esteja rodando, ele nao tira todo o saldo. Tira apenas uma parte.
1.1 - Ele só tira tudo na primeira run do código (assim que chama .py)
Com o audio que voce enviou no sabado, eu tive a ideia de fazer a transacao dar um get_transaction e wait_for_transaction_receipt para pegar
o status da transacao e o nonce. Com isso eu alteraria a variavel status e pegaria o nonce da transacao que aconteceu com sucesso. Assim evitaria de ficar incrementando
indefinidamente o nonce mesmo que nao tenha sido feita com sucesso.

Entretanto nao funcionou, se comportou da mesma maneira....

Aí estou com uma intuição que isso deva ser feito com async function, para fazer a transacao e aguardar que a corotina espera_resposta retorne com os valores de status e nonce. 

Porém nao tenho muita experiencia com concorrencia e paralelismo, e estou vendo ainda como implementar
tentei fazer de forma padrao mas, como pode ver ao rodar esse codigo, nao funcionou...

A funcao revenge é o bot da forma inicial, pode chamar ela que ele vai se comportar da maneira que especifiquei
Já deixo meu agradecimento pela ajuda anterior e dessa.


Atualização: Consegui fazer funcionar, mas as vezes dá problema de truncamento
caso algume transfira um valor na ordem de 10^-2, pode haver problema em que o calculo (balanço - gás) dê um valor que ao construir a transacao com essa diferença
não dá saldo suficiente.
Isso acontece pq la no final o pc deixa um numero de truncamento que somado com o gás, dá maior que o balanço inicial

exemplo:
foi depositado 0.14
o gás minimo para a rede de test é 10 gwei ou 0.000231 bnb
entao, queremos tirar 0.14 - 0.000231 = 0.13979, porém numericamente o computador está fazendo 0.13979000000000005 que quebra essa transação

Fiz uma pseudo aplicação das funcoes async o erro antigo foi resolvido, mas agora surge esse...

O código novo é async_bot.py
