"""Parte 2 - A conta cuida do proprio saldo.

Execute na pasta do projeto:
    python -m exemplos.parte2_encapsulamento
"""
from Cliente import Cliente
from Conta import Conta

cliente = Cliente("123", "Joao", "Rua 1")
conta = Conta(1, [cliente], 100)

print("saldo inicial:", conta.saldo)

print("\n-- deposito valido --")
print("resultado:", conta.depositar(50), "| saldo:", conta.saldo)

print("\n-- tentativas invalidas (nada deve mudar) --")
for valor in (0, -30, "100"):
    resultado = conta.depositar(valor)
    print(f"depositar({valor!r}) -> {resultado} | saldo: {conta.saldo}")

for valor in (0, -30, 10_000):
    resultado = conta.sacar(valor)
    print(f"sacar({valor!r}) -> {resultado} | motivo: {resultado.motivo} | saldo: {conta.saldo}")

print("\n-- o saldo nao pode ser escrito de fora --")
try:
    conta.saldo = 1_000_000
except AttributeError as erro:
    print("AttributeError:", erro)

print("\nsaldo final:", conta.saldo)

assert conta.saldo == 150
print("\nOK: so os metodos da Conta mudaram o saldo.")
