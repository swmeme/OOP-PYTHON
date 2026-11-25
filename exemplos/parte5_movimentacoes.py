"""Parte 5 - Movimentacoes com tipo, valor e data.

Execute na pasta do projeto:
    python -m exemplos.parte5_movimentacoes
"""
from datetime import datetime

from Cliente import Cliente
from Conta import Conta
from Movimentacao import Movimentacao

cliente = Cliente("123", "Joao", "Rua 1")
conta = Conta(1, [cliente], 100)
destino = Conta(2, [cliente], 0)

conta.depositar(50)
conta.sacar(30)
conta.transferir(destino, 20)

print("== Historico da conta 1 ==")
for movimentacao in conta.extrato:
    print(repr(movimentacao))

print()
print("== Extrato formatado ==")
print(conta.extrato.formatar())

print()
print("== Uma data pode ser informada (util em testes) ==")
exemplo = Movimentacao("DEPOSITO", 10, datetime(2024, 3, 15, 9, 30))
print(exemplo.formatar())

print()
print("== Formatacao nao altera o historico ==")
antes = conta.extrato.movimentacoes
conta.extrato.formatar()
depois = conta.extrato.movimentacoes
print("mesmo historico?", antes == depois)

assert all(mov.data.year >= 2000 for mov in conta.extrato)
print("\nOK: cada operacao valida virou uma Movimentacao com data.")
