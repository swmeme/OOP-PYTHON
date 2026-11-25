"""Parte 1: duas contas, dois estados independentes.

Execute na pasta do projeto:
    python testecontas2.py
"""
from Cliente import Cliente
from Conta import Conta

joao = Cliente("123", "Joao", "Rua 1")
maria = Cliente("345", "Maria", "Rua 2")

conta1 = Conta(1, [joao], 0)
conta2 = Conta(2, [maria], 2000)

print(f"Antes -> conta 1: R$ {conta1.saldo:.2f} | conta 2: R$ {conta2.saldo:.2f}")

conta1.depositar(1500)

print(f"Depois -> conta 1: R$ {conta1.saldo:.2f} | conta 2: R$ {conta2.saldo:.2f}")

assert conta1.saldo == 1500, "a conta 1 deveria ter recebido o deposito"
assert conta2.saldo == 2000, "a conta 2 nao poderia ser afetada"

print("OK: cada objeto Conta guarda o proprio saldo.")
