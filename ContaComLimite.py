from Conta import Conta


class ContaComLimite(Conta):
    """Conta com um limite adicional de credito.

    A unica regra nova e: o saldo disponivel inclui o limite. Como a Conta
    mae ja usa `saldo_disponivel` em `_debitar`, o saque e a transferencia
    passam a aceitar o limite sem precisar ser reescritos.
    """

    def __init__(self, numero, clientes, saldo_inicial=0, limite=500):
        if not isinstance(limite, (int, float)) or isinstance(limite, bool) or limite < 0:
            raise ValueError("o limite precisa ser um numero maior ou igual a zero")

        self._limite = limite
        super().__init__(numero, clientes, saldo_inicial)

    @property
    def limite(self):
        return self._limite

    @property
    def saldo_disponivel(self):
        return round(self.saldo + self._limite, 2)
