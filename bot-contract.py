from time import sleep
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
import json

import os
import sys

bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))

contract_address = '0xF718BDAE5f1630eEfbD454a4c7aeaCA1D7C85Bdc'
my_address = '0x8D873Af746d58b3aE24E5D89228F2c297593c9E4'
denis_address = '0x308dC6D4671877ff4b4e5230121BBAF1c9ab03FA'
private_key = 'cfdbccf01dcd5e8d70fb82d49770547276734f7574f427c23dca71c49dc619aa'
private_key_my = 'fe766585aa66ca3a8b3eaeba7ba040b3152616c7c5ff54e6008b81a0c94aeacc'


abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balances","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')

contract = web3.eth.contract(address=contract_address, abi=abi)

total_supply = contract.functions.totalSupply().call()

#print(web3.fromWei(total_supply, 'ether'))
#print(contract.functions.name().call())
#print(contract.functions.symbol().call())

balanceOf = contract.functions.balanceOf(denis_address).call()
print(web3.fromWei(balanceOf, 'ether'))

send = 98989898
amount = web3.toWei(send, 'ether')
# necessário para evitar erro "nonce too low"
nonce = web3.eth.getTransactionCount(my_address)

while(True):
    """Quando executa transações muito rápido, é necessário salvar o nonce localmente
    pois a demora da rede pode causar o erro "nonce too low", visto que sempre que você
    faz uma transação na rede, o nonce deve aumentar em 1, porém a chamada da função
    'web3.eth.getTransactionCount(my_address)' depende da rede, caso a rede demore mais
    que 5 segundos (sleep(5)), o nonce da próxima transação atual será o mesmo da última
    transação executada pela carteira.
    EX: Nonce da minha carteira é 5, executo uma transação... assim que a rede confirmar
    esta transação, o nonce passará a ser 6. 
    Porém, se eu tentar fazer uma outra transação antes da rede confirmar a transação anterior
    vou me deparar com o erro "nonce too low", pois a rede ainda não incrementou meu nonce.
    Para resolver este caso, nós aumentamos o nonce localmente, assim não dependemos da rede.
    """
    print("Nonce: {}".format(nonce))

    token_tx = contract.functions.transfer(denis_address, amount).buildTransaction({
        'chainId': 56, 'gas':100000, 'gasPrice': web3.toWei('10','gwei'), 'nonce' : nonce})
    sign_txn = web3.eth.account.signTransaction(token_tx, private_key= private_key_my)
    web3.eth.sendRawTransaction(sign_txn.rawTransaction)

    print(f"[-]Transacao foi feita para {denis_address}")
    # nonce foi incrementado localmente +1 para evitar erro "nonce too low" devido a demora da rede.
    nonce+=1
    sleep(5) 