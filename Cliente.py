class Cliente:
    """Representa uma pessoa que pode ser titular de uma conta.

    Esta classe so guarda dados. Quem decide o que fazer com eles e o
    restante do sistema (Conta, Extrato, script de demonstracao).
    """

    def __init__(self, cpf, nome_titular, endereco):
        self.cpf = cpf
        self.nome_titular = nome_titular
        self.endereco = endereco

    def formatar(self):
        """Devolve os dados do cliente em uma linha de texto."""
        return f"CPF: {self.cpf} | NOME: {self.nome_titular} | ENDERECO: {self.endereco}"

    def __repr__(self):
        return f"Cliente(cpf={self.cpf!r}, nome_titular={self.nome_titular!r})"
