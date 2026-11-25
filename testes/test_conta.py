"""Testes de comportamento da Conta comum (Parte 7)."""
import unittest

from Cliente import Cliente
from Conta import Conta


class TestConta(unittest.TestCase):
    def setUp(self):
        self.joao = Cliente("123", "Joao", "Rua 1")
        self.maria = Cliente("345", "Maria", "Rua 2")
        self.conta = Conta(1, [self.joao, self.maria], 1000)

    # ---------------- deposito ----------------
    def test_deposito_valido_atualiza_saldo(self):
        resultado = self.conta.depositar(500)

        self.assertTrue(resultado)
        self.assertEqual(self.conta.saldo, 1500)

    def test_deposito_valido_registra_historico(self):
        self.conta.depositar(500)

        ultima = self.conta.extrato.movimentacoes[-1]
        self.assertEqual(ultima.tipo, "DEPOSITO")
        self.assertEqual(ultima.valor, 500)

    def test_deposito_invalido_nao_altera_nada(self):
        historico_antes = len(self.conta.extrato)

        for valor in (0, -10, "100", None, True):
            with self.subTest(valor=valor):
                resultado = self.conta.depositar(valor)

                self.assertFalse(resultado)
                self.assertEqual(resultado.motivo, "valor_invalido")
                self.assertEqual(self.conta.saldo, 1000)
                self.assertEqual(len(self.conta.extrato), historico_antes)

    # ---------------- saque ----------------
    def test_saque_valido_atualiza_saldo(self):
        resultado = self.conta.sacar(400)

        self.assertTrue(resultado)
        self.assertEqual(self.conta.saldo, 600)

    def test_saque_valido_registra_historico(self):
        self.conta.sacar(400)

        ultima = self.conta.extrato.movimentacoes[-1]
        self.assertEqual(ultima.tipo, "SAQUE")
        self.assertEqual(ultima.valor, 400)

    def test_saque_maior_que_saldo_e_recusado(self):
        resultado = self.conta.sacar(1000.01)

        self.assertFalse(resultado)
        self.assertEqual(resultado.motivo, "saldo_insuficiente")
        self.assertEqual(self.conta.saldo, 1000)

    def test_saque_do_saldo_inteiro_e_permitido(self):
        resultado = self.conta.sacar(1000)

        self.assertTrue(resultado)
        self.assertEqual(self.conta.saldo, 0)

    def test_saque_invalido_nao_altera_nada(self):
        for valor in (0, -50, "10"):
            with self.subTest(valor=valor):
                resultado = self.conta.sacar(valor)

                self.assertFalse(resultado)
                self.assertEqual(resultado.motivo, "valor_invalido")
                self.assertEqual(self.conta.saldo, 1000)

    # ---------------- estado do objeto ----------------
    def test_saldo_nao_pode_ser_escrito_de_fora(self):
        with self.assertRaises(AttributeError):
            self.conta.saldo = 999999

    def test_contas_diferentes_tem_saldos_independentes(self):
        outra = Conta(2, [self.maria], 50)

        self.conta.depositar(500)

        self.assertEqual(self.conta.saldo, 1500)
        self.assertEqual(outra.saldo, 50)

    def test_clientes_precisam_ser_lista(self):
        with self.assertRaises(TypeError):
            Conta(3, self.joao, 0)

    def test_clientes_nao_pode_ser_lista_vazia(self):
        with self.assertRaises(TypeError):
            Conta(3, [], 0)

    def test_todos_os_clientes_precisam_ser_cliente(self):
        with self.assertRaises(TypeError):
            Conta(3, [self.joao, "Maria"], 0)

    def test_saldo_inicial_negativo_e_recusado(self):
        with self.assertRaises(ValueError):
            Conta(3, [self.joao], -1)

    def test_resumo_traz_numero_e_saldo(self):
        texto = self.conta.resumo()

        self.assertIn("Conta: 1", texto)
        self.assertIn("1000.00", texto)
        self.assertIn("Joao", texto)


if __name__ == "__main__":
    unittest.main()
