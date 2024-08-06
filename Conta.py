'''
Here we begin our banking account, the variable names in this code will be partially in 
portuguese language, if you have any doubt about the meaning of the objects, variables, etc... google it!
'''
class Conta:
    def __init__(self, numero, cpf, nomeTitular, saldo):
        self.numero = numero
        self.cpf = cpf
        self.nomeTitular = nomeTitular
        self.saldo = saldo
    
    def depositar(self, valor):
        self.saldo+= valor
    def sacar(self, valor):
        self.saldo-= valor
    def gerar_extrato(self):
        print(f'CONTA: {self.numero}\n CPF: {self.cpf}\n SALDO: {self.saldo}')
