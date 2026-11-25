"""
A conta bancaria do nosso banco didatico.

Regra de ouro: o saldo so muda dentro desta classe. Quem usa a conta pede
uma operacao (depositar, sacar, transferir) e recebe um Resultado.
Nenhuma mensagem para a pessoa e impressa aqui: isso e trabalho do script.
"""
import math
from datetime import datetime

from Cliente import Cliente
from Extrato import Extrato
from Movimentacao import Movimentacao
from Resultado import Resultado


class Conta:
    def __init__(self, numero, clientes, saldo_inicial=0):
        self.numero = numero
        self.clientes = self._normalizar_clientes(clientes)
        self.data_abertura = datetime.now()
        self.extrato = Extrato(numero)
        self._saldo = 0

        if not self._valor_valido(saldo_inicial, permitir_zero=True):
            raise ValueError("saldo_inicial precisa ser um numero maior ou igual a zero")

        if saldo_inicial > 0:
            self._saldo = round(saldo_inicial, 2)
            self.extrato.registrar(Movimentacao(Movimentacao.ABERTURA, saldo_inicial))

    # ------------------------------------------------------------------
    # Leitura do estado
    # ------------------------------------------------------------------
    @property
    def saldo(self):
        """O saldo pode ser lido, mas nao escrito de fora (sem setter)."""
        return self._saldo

    @property
    def saldo_disponivel(self):
        """Quanto a conta pode gastar agora.

        Na Conta comum e igual ao saldo. A ContaComLimite sobrescreve esta
        propriedade para somar o limite. Todo o resto do codigo continua igual.
        """
        return self._saldo

    def resumo(self):
        """Devolve os dados da conta em texto. Nao imprime nada."""
        linhas = [
            f"Conta: {self.numero}",
            f"Saldo: R$ {self.saldo:.2f}",
            f"Saldo disponivel: R$ {self.saldo_disponivel:.2f}",
            f"Abertura: {self.data_abertura:%d/%m/%Y %H:%M}",
        ]
        for cliente in self.clientes:
            linhas.append(cliente.formatar())
        return "\n".join(linhas)

    # ------------------------------------------------------------------
    # Operacoes publicas: a interface simples que o resto do sistema usa
    # ------------------------------------------------------------------
    def depositar(self, valor):
        return self._creditar(valor, Movimentacao.DEPOSITO)

    def sacar(self, valor):
        return self._debitar(valor, Movimentacao.SAQUE)

    def transferir(self, destino, valor):
        """Move dinheiro desta conta para outra, tudo ou nada."""
        if not isinstance(destino, Conta):
            return Resultado.falha("destino_invalido")
        if destino is self:
            return Resultado.falha("mesma_conta")

        retirada = self._debitar(valor, Movimentacao.TRANSFERENCIA_ENVIADA)
        if not retirada:
            return retirada

        # O valor ja foi validado em _debitar; creditar nao pode falhar.
        credito = destino._creditar(valor, Movimentacao.TRANSFERENCIA_RECEBIDA)
        if not credito.ok:  # protecao contra subclasses mal comportadas
            raise RuntimeError("falha inesperada ao creditar a conta de destino")

        return Resultado.sucesso()

    # ------------------------------------------------------------------
    # Regras internas: unico lugar que altera o saldo
    # ------------------------------------------------------------------
    def _creditar(self, valor, tipo):
        if not self._valor_valido(valor):
            return Resultado.falha("valor_invalido")

        self._saldo = round(self._saldo + valor, 2)
        self.extrato.registrar(Movimentacao(tipo, valor))
        return Resultado.sucesso()

    def _debitar(self, valor, tipo):
        if not self._valor_valido(valor):
            return Resultado.falha("valor_invalido")
        if valor > self.saldo_disponivel:
            return Resultado.falha("saldo_insuficiente")

        self._saldo = round(self._saldo - valor, 2)
        self.extrato.registrar(Movimentacao(tipo, valor))
        return Resultado.sucesso()

    # ------------------------------------------------------------------
    # Validacoes de entrada
    # ------------------------------------------------------------------
    @staticmethod
    def _normalizar_clientes(clientes):
        """Garante um formato unico: sempre uma lista com pelo menos 1 cliente."""
        if isinstance(clientes, Cliente):
            raise TypeError(
                "clientes deve ser uma lista, mesmo com um unico cliente: [cliente]"
            )
        if not isinstance(clientes, (list, tuple)) or len(clientes) == 0:
            raise TypeError("informe pelo menos um cliente dentro de uma lista")

        for cliente in clientes:
            if not isinstance(cliente, Cliente):
                raise TypeError("todos os itens de clientes precisam ser objetos Cliente")

        return list(clientes)

    @staticmethod
    def _valor_valido(valor, permitir_zero=False):
        """Aceita numeros de verdade (nao bool), finitos, positivos."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            return False
        if not math.isfinite(valor):
            return False
        return valor >= 0 if permitir_zero else valor > 0
