from Movimentacao import Movimentacao


class Extrato:
    """Guarda o historico de uma conta e sabe se transformar em texto.

    O Extrato pertence a uma conta (composicao). Ele apenas *registra* e
    *formata*: nunca muda o saldo e nunca decide se uma operacao e valida.
    """

    def __init__(self, numero_conta):
        self.numero_conta = numero_conta
        self._movimentacoes = []

    @property
    def movimentacoes(self):
        # Devolvemos uma tupla: quem estiver fora nao consegue dar append
        # nem remover itens do historico por acidente.
        return tuple(self._movimentacoes)

    def registrar(self, movimentacao):
        if not isinstance(movimentacao, Movimentacao):
            raise TypeError("o extrato so aceita objetos Movimentacao")
        self._movimentacoes.append(movimentacao)

    def formatar(self):
        """Monta o texto do extrato sem alterar o historico."""
        linhas = [f"Extrato da conta {self.numero_conta}", "-" * 52]

        if not self._movimentacoes:
            linhas.append("(sem movimentacoes)")
        else:
            for movimentacao in self._movimentacoes:
                linhas.append(movimentacao.formatar())

        linhas.append("-" * 52)
        linhas.append(f"Total de movimentacoes: {len(self._movimentacoes)}")
        return "\n".join(linhas)

    def __len__(self):
        return len(self._movimentacoes)

    def __iter__(self):
        return iter(self._movimentacoes)
