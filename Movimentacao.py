from datetime import datetime


class Movimentacao:
    """Um fato que aconteceu na conta: deposito, saque ou transferencia.

    Repare que ela nao e uma Conta nem um Cliente. E um registro historico:
    tipo + valor + data. Depois de criada, nao deve ser alterada.
    """

    ABERTURA = "ABERTURA"
    DEPOSITO = "DEPOSITO"
    SAQUE = "SAQUE"
    TRANSFERENCIA_ENVIADA = "TRANSFERENCIA_ENVIADA"
    TRANSFERENCIA_RECEBIDA = "TRANSFERENCIA_RECEBIDA"

    @classmethod
    def tipos_validos(cls):
        return (
            cls.ABERTURA,
            cls.DEPOSITO,
            cls.SAQUE,
            cls.TRANSFERENCIA_ENVIADA,
            cls.TRANSFERENCIA_RECEBIDA,
        )

    def __init__(self, tipo, valor, data=None):
        if tipo not in self.tipos_validos():
            raise ValueError(f"tipo de movimentacao desconhecido: {tipo!r}")
        if not isinstance(valor, (int, float)) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("o valor da movimentacao precisa ser maior que zero")
        if data is not None and not isinstance(data, datetime):
            raise TypeError("a data precisa ser um datetime")

        self.tipo = tipo
        self.valor = valor
        self.data = data if data is not None else datetime.now()

    def formatar(self):
        return f"{self.tipo:<22} R$ {self.valor:>10.2f}   {self.data:%d/%m/%Y %H:%M}"

    def __repr__(self):
        return f"Movimentacao(tipo={self.tipo!r}, valor={self.valor!r}, data={self.data!r})"
