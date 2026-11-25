"""Testes da conta com limite (exercicio opcional de heranca)."""
import unittest

from Cliente import Cliente
from Conta import Conta
from ContaComLimite import ContaComLimite


class TestContaComLimite(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente("123", "Joao", "Rua 1")
        self.conta = ContaComLimite(10, [self.cliente], 100, limite=50)

    def test_saldo_disponivel_soma_saldo_e_limite(self):
        self.assertEqual(self.conta.saldo_disponivel, 150)

    def test_saque_dentro_do_limite_deixa_saldo_negativo(self):
        resultado = self.conta.sacar(140)

        self.assertTrue(resultado)
        self.assertEqual(self.conta.saldo, -40)
        self.assertEqual(self.conta.saldo_disponivel, 10)

    def test_saque_acima_do_limite_e_recusado(self):
        resultado = self.conta.sacar(150.01)

        self.assertFalse(resultado)
        self.assertEqual(resultado.motivo, "saldo_insuficiente")
        self.assertEqual(self.conta.saldo, 100)

    def test_transferencia_pode_usar_o_limite(self):
        destino = Conta(20, [self.cliente], 0)

        resultado = self.conta.transferir(destino, 120)

        self.assertTrue(resultado)
        self.assertEqual(self.conta.saldo, -20)
        self.assertEqual(destino.saldo, 120)

    def test_limite_negativo_e_recusado(self):
        with self.assertRaises(ValueError):
            ContaComLimite(11, [self.cliente], 0, limite=-1)

    def test_codigo_que_usa_conta_funciona_com_os_dois_tipos(self):
        """Polimorfismo: a mesma funcao serve para Conta e ContaComLimite."""

        def tentar_pagar(conta, valor):
            return conta.sacar(valor)

        comum = Conta(30, [self.cliente], 100)
        com_limite = ContaComLimite(31, [self.cliente], 100, limite=50)

        self.assertTrue(tentar_pagar(comum, 100))
        self.assertFalse(tentar_pagar(comum, 101))
        self.assertTrue(tentar_pagar(com_limite, 140))


if __name__ == "__main__":
    unittest.main()
