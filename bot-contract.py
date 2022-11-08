from time import sleep
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
import json

import os
import sys

bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))

contract_address = 'sssssssssssssss'
my_address = 'aaaaaaaaaaaaaaaaaa'
denis_address = 'fffffffffffffffffffffffffff'
private_key = 'ddddddddddddddddddddddddddddddd'
private_key_my = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'


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
    
    print("Nonce: {}".format(nonce))

    token_tx = contract.functions.transfer(denis_address, amount).buildTransaction({
        'chainId': 56, 'gas':100000, 'gasPrice': web3.toWei('10','gwei'), 'nonce' : nonce})
    sign_txn = web3.eth.account.signTransaction(token_tx, private_key= private_key_my)
    web3.eth.sendRawTransaction(sign_txn.rawTransaction)

    print(f"[-]Transacao foi feita para {denis_address}")
    # nonce foi incrementado localmente +1 para evitar erro "nonce too low" devido a demora da rede.
    nonce+=1
    sleep(5) 