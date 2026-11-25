"""Camada de apresentacao: transforma o Resultado da conta em texto.

A Conta nao conhece estas frases. Se amanha o banco tiver um aplicativo,
um site ou outro idioma, so esta camada muda.
"""

MENSAGENS = {
    "valor_invalido": "O valor precisa ser um numero maior que zero.",
    "saldo_insuficiente": "Saldo insuficiente para esta operacao.",
    "mesma_conta": "Nao e possivel transferir para a mesma conta.",
    "destino_invalido": "A conta de destino nao foi informada corretamente.",
}


def descrever(resultado):
    """Devolve uma frase pronta para mostrar a pessoa."""
    if resultado:
        return "Operacao realizada."
    return MENSAGENS.get(resultado.motivo, "Operacao nao realizada.")
