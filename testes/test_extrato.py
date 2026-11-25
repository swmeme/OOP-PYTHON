"""Testes do Extrato e das Movimentacoes (Partes 4 e 5)."""
import unittest
from datetime import datetime

from Cliente import Cliente
from Conta import Conta
from Movimentacao import Movimentacao


class TestExtrato(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente("123", "Joao", "Rua 1")
        self.conta = Conta(1, [self.cliente], 100)

    def test_conta_nova_tem_extrato_vazio(self):
        conta_nova = Conta(2, [self.cliente], 0)
        self.assertEqual(len(conta_nova.extrato), 0)

    def test_saldo_inicial_aparece_como_abertura(self):
        self.assertEqual(len(self.conta.extrato), 1)
        self.assertEqual(self.conta.extrato.movimentacoes[0].tipo, "ABERTURA")

    def test_cada_conta_tem_o_proprio_extrato(self):
        outra = Conta(2, [self.cliente], 0)

        self.conta.depositar(50)

        self.assertEqual(len(self.conta.extrato), 2)
        self.assertEqual(len(outra.extrato), 0)

    def test_formatar_nao_altera_o_historico(self):
        self.conta.depositar(50)
        antes = self.conta.extrato.movimentacoes

        self.conta.extrato.formatar()
        self.conta.extrato.formatar()

        self.assertEqual(self.conta.extrato.movimentacoes, antes)

    def test_historico_externo_e_somente_leitura(self):
        with self.assertRaises(AttributeError):
            self.conta.extrato.movimentacoes.append("inventado")

    def test_extrato_formatado_mostra_tipo_valor_e_data(self):
        texto = self.conta.extrato.formatar()

        self.assertIn("ABERTURA", texto)
        self.assertIn("100.00", texto)
        self.assertRegex(texto, r"\d{2}/\d{2}/\d{4}")


class TestMovimentacao(unittest.TestCase):
    def test_movimentacao_guarda_tipo_valor_e_data(self):
        data = datetime(2024, 5, 20, 14, 30)
        movimentacao = Movimentacao("DEPOSITO", 250, data)

        self.assertEqual(movimentacao.tipo, "DEPOSITO")
        self.assertEqual(movimentacao.valor, 250)
        self.assertEqual(movimentacao.data, data)

    def test_data_padrao_e_agora(self):
        antes = datetime.now()
        movimentacao = Movimentacao("SAQUE", 10)
        depois = datetime.now()

        self.assertGreaterEqual(movimentacao.data, antes)
        self.assertLessEqual(movimentacao.data, depois)

    def test_tipo_desconhecido_e_recusado(self):
        with self.assertRaises(ValueError):
            Movimentacao("PIX", 10)

    def test_valor_invalido_e_recusado(self):
        for valor in (0, -5, "10"):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    Movimentacao("DEPOSITO", valor)

    def test_formatar_mostra_data_formatada(self):
        movimentacao = Movimentacao("DEPOSITO", 50, datetime(2024, 1, 2, 3, 4))

        self.assertIn("02/01/2024", movimentacao.formatar())


if __name__ == "__main__":
    unittest.main()
