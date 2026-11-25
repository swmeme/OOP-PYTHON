"""Exercicio opcional - Heranca e polimorfismo.

Execute na pasta do projeto:
    python -m exemplos.opcional_polimorfismo
"""
from Cliente import Cliente
from Conta import Conta
from ContaComLimite import ContaComLimite

cliente = Cliente("123", "Joao", "Rua 1")


def pagar(conta, valor):
    """Esta funcao nao sabe (nem precisa saber) que tipo de conta recebeu."""
    resultado = conta.sacar(valor)
    situacao = "pago" if resultado else f"recusado ({resultado.motivo})"
    print(f"  conta {conta.numero}: pagar R$ {valor:.2f} -> {situacao}")
    return resultado


comum = Conta(1, [cliente], 100)
com_limite = ContaComLimite(2, [cliente], 100, limite=50)

print("== Mesma funcao, contas diferentes ==")
pagar(comum, 100)
pagar(comum, 101)
pagar(com_limite, 140)

print("\n== Estado final ==")
for conta in (comum, com_limite):
    print(f"  conta {conta.numero}: saldo R$ {conta.saldo:.2f} "
          f"| disponivel R$ {conta.saldo_disponivel:.2f}")

assert isinstance(com_limite, Conta)
assert comum.saldo == 0
assert com_limite.saldo == -40
print("\nOK: ContaComLimite e um tipo de Conta e respeita o mesmo contrato publico.")
