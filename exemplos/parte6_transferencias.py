"""Parte 6 - Transferencia: duas contas colaborando.

Execute na pasta do projeto:
    python -m exemplos.parte6_transferencias
"""
from Cliente import Cliente
from Conta import Conta
from mensagens import descrever

cliente = Cliente("123", "Joao", "Rua 1")
origem = Conta(1, [cliente], 500)
destino = Conta(2, [cliente], 100)


def mostrar_saldos():
    print(f"  origem: R$ {origem.saldo:.2f} | destino: R$ {destino.saldo:.2f}")


print("== Antes ==")
mostrar_saldos()

print("\n== Transferencia valida de 200 ==")
resultado = origem.transferir(destino, 200)
print(" ", descrever(resultado))
mostrar_saldos()

print("\n== Tentativas invalidas ==")
for rotulo, acao in (
    ("valor negativo", lambda: origem.transferir(destino, -50)),
    ("saldo insuficiente", lambda: origem.transferir(destino, 9999)),
    ("mesma conta", lambda: origem.transferir(origem, 10)),
):
    resultado = acao()
    print(f"  {rotulo}: {descrever(resultado)}")
    mostrar_saldos()

print("\n== Historico das duas contas ==")
print(origem.extrato.formatar())
print()
print(destino.extrato.formatar())

assert origem.saldo == 300
assert destino.saldo == 300
print("\nOK: o valor saiu de uma conta, chegou a outra e as duas registram o fato.")
