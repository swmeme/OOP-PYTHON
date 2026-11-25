"""Parte 4 - Composicao e associacao.

Execute na pasta do projeto:
    python -m exemplos.parte4_composicao
"""
from Cliente import Cliente
from Conta import Conta

joao = Cliente("123", "Joao", "Rua 1")
maria = Cliente("345", "Maria", "Rua 2")

conta_individual = Conta(1, [joao], 0)
conta_conjunta = Conta(2, [joao, maria], 100)

print("== Uma conta, um cliente ==")
print("\n".join(c.formatar() for c in conta_individual.clientes))
print()

print("== Uma conta, dois clientes ==")
print("\n".join(c.formatar() for c in conta_conjunta.clientes))
print()

conta_conjunta.depositar(50)

print("== Cada conta tem o proprio extrato ==")
print("conta 1 tem", len(conta_individual.extrato), "movimentacoes")
print("conta 2 tem", len(conta_conjunta.extrato), "movimentacoes")
print()

print("== O formato e sempre lista ==")
try:
    Conta(3, maria, 0)
except TypeError as erro:
    print("TypeError:", erro)

print("\nExtrato da conta 2:")
print(conta_conjunta.extrato.formatar())

assert len(conta_individual.extrato) == 0
assert len(conta_conjunta.extrato) == 2
print("\nOK: um ou varios clientes funcionam igual, e os extratos sao independentes.")
