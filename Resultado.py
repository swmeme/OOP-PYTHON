class Resultado:
    """Resposta de uma operacao da conta.

    A conta informa *se* deu certo e, quando nao deu, *por que* nao deu.
    O texto mostrado a pessoa nao fica aqui: fica na camada de mensagens
    (mensagens.py). Assim, a regra de negocio nao depende da interface.
    """

    def __init__(self, ok, motivo=None):
        self.ok = ok
        self.motivo = motivo

    @classmethod
    def sucesso(cls):
        return cls(True)

    @classmethod
    def falha(cls, motivo):
        return cls(False, motivo)

    def __bool__(self):
        # Permite escrever: if conta.depositar(100): ...
        return self.ok

    def __repr__(self):
        return f"Resultado(ok={self.ok!r}, motivo={self.motivo!r})"
