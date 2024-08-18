'''
Here we begin our banking account, the variable names in this code will be partially in 
portuguese language, if you have any doubt about the meaning of the objects, variables, etc...
Google it!.. or ask any IA you wish...
'''
import datetime
from Extrato import Extrato
class Conta:
    def __init__(self, numeroConta, clientes, saldo):
        self.numeroConta = numeroConta
        self.clientes = clientes
        self.saldo = saldo
        self.sataabertura = datetime.datetime.today()
        self.extrato = Extrato()
        
    def depositar(self, valor):
        self.saldo+= valor
        self.extrato.transactions.append(['DEPOSITO: ', valor, 'DATA: ', datetime.datetime.today])
    
    def sacar(self, valor):
        if self.saldo < valor:
            print('Saldo insuficiente!')
            return False
        else:
            self.saldo -= valor
            return True        
    
    def gerar_extrato(self):
        print(f'CONTA: {self.numeroConta}\n SALDO: {self.saldo}')
        for cliente in self.clientes:
            print(f'CPF: {cliente.cpf}\n NOME: {cliente.nomeTitular}\n ENDEREÇO: {cliente.endereco}')
    
    def transferenciaDEvalor(self, contaDestino, valor):
        if self.saldo < valor:
            return('Saldo insuficiente.')
        else:
            contaDestino.depositar(valor)
            self.saldo -= valor
            self.extrato.transactions.append(['TRANSFERENCIA: ', valor, 'DATA: ', datetime.datetime.today()])
            return('Transferência realizada!')
    
    def gerar_saldo(self):
        print(f'Numero: {self.numeroConta} \n Saldo: {self.saldo}')
