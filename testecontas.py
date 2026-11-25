"""Demonstracao principal do banco didatico.

Execute na pasta do projeto:
    python testecontas.py
"""
from Cliente import Cliente
from Conta import Conta
from mensagens import descrever

joao = Cliente("123", "Joao", "Rua 1")
maria = Cliente("345", "Maria", "Rua 2")

conta1 = Conta(1, [joao, maria], 0)
conta2 = Conta(2, [maria], 500)

print("=== Situacao inicial ===")
print(conta1.resumo())
print()

print("=== Operacoes ===")
print("Deposito de 1500 na conta 1:", descrever(conta1.depositar(1500)))
print("Saque de 500 na conta 1:", descrever(conta1.sacar(500)))
print("Saque de 99999 na conta 1:", descrever(conta1.sacar(99999)))
print("Deposito de -10 na conta 1:", descrever(conta1.depositar(-10)))
print("Transferencia de 300 da conta 1 para a conta 2:", descrever(conta1.transferir(conta2, 300)))
print()

print("=== Extrato da conta 1 ===")
print(conta1.extrato.formatar())
print()

print("=== Extrato da conta 2 ===")
print(conta2.extrato.formatar())
