"""Parte 3 - Regras na Conta, mensagens na interface.

Execute na pasta do projeto:
    python -m exemplos.parte3_mensagens
"""
from Cliente import Cliente
from Conta import Conta
from mensagens import descrever

cliente = Cliente("123", "Joao", "Rua 1")
conta = Conta(1, [cliente], 100)


def tela_simples(rotulo, resultado):
    """Uma interface possivel: frases curtas em portugues."""
    if resultado:
        print(f"[tela] {rotulo}: feito")
    else:
        print(f"[tela] {rotulo}: {descrever(resultado)}")


def tela_tecnica(rotulo, resultado):
    """Outra interface possivel: mostra o codigo do motivo."""
    estado = "ok" if resultado else f"falhou ({resultado.motivo})"
    print(f"[log]   {rotulo}: {estado}")


print("Saldo inicial:", conta.saldo)
print()

for nome, funcao in (
    ("deposito 50", lambda: conta.depositar(50)),
    ("saque 500", lambda: conta.sacar(500)),
    ("saque -10", lambda: conta.sacar(-10)),
):
    resultado = funcao()
    tela_simples(nome, resultado)
    tela_tecnica(nome, resultado)

print("\nA Conta nao imprimiu nada: ela so devolveu Resultado(ok, motivo).")
print("Saldo final:", conta.saldo)
