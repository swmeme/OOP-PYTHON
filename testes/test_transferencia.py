"""Testes da transferencia entre contas (Parte 7)."""
import unittest

from Cliente import Cliente
from Conta import Conta


class TestTransferencia(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente("123", "Joao", "Rua 1")
        self.origem = Conta(1, [self.cliente], 1000)
        self.destino = Conta(2, [self.cliente], 200)

    def test_transferencia_valida_move_o_dinheiro(self):
        resultado = self.origem.transferir(self.destino, 300)

        self.assertTrue(resultado)
        self.assertEqual(self.origem.saldo, 700)
        self.assertEqual(self.destino.saldo, 500)

    def test_transferencia_registra_uma_movimentacao_em_cada_conta(self):
        antes_origem = len(self.origem.extrato)
        antes_destino = len(self.destino.extrato)

        self.origem.transferir(self.destino, 300)

        self.assertEqual(len(self.origem.extrato), antes_origem + 1)
        self.assertEqual(len(self.destino.extrato), antes_destino + 1)

        saida = self.origem.extrato.movimentacoes[-1]
        entrada = self.destino.extrato.movimentacoes[-1]

        self.assertEqual(saida.tipo, "TRANSFERENCIA_ENVIADA")
        self.assertEqual(entrada.tipo, "TRANSFERENCIA_RECEBIDA")
        self.assertEqual(saida.valor, entrada.valor)

    def test_transferencia_sem_saldo_nao_muda_nada(self):
        self.assertFalse(self.origem.transferir(self.destino, 1000.01))

        self.assertEqual(self.origem.saldo, 1000)
        self.assertEqual(self.destino.saldo, 200)

    def test_transferencia_com_valor_invalido_nao_muda_nada(self):
        for valor in (0, -100, "300"):
            with self.subTest(valor=valor):
                resultado = self.origem.transferir(self.destino, valor)

                self.assertFalse(resultado)
                self.assertEqual(resultado.motivo, "valor_invalido")
                self.assertEqual(self.origem.saldo, 1000)
                self.assertEqual(self.destino.saldo, 200)

    def test_transferencia_para_a_mesma_conta_e_recusada(self):
        resultado = self.origem.transferir(self.origem, 100)

        self.assertFalse(resultado)
        self.assertEqual(resultado.motivo, "mesma_conta")
        self.assertEqual(self.origem.saldo, 1000)

    def test_transferencia_para_destino_invalido_e_recusada(self):
        resultado = self.origem.transferir("conta 2", 100)

        self.assertFalse(resultado)
        self.assertEqual(resultado.motivo, "destino_invalido")
        self.assertEqual(self.origem.saldo, 1000)

    def test_transferir_o_saldo_inteiro_para_outra_conta(self):
        self.assertTrue(self.origem.transferir(self.destino, 1000))
        self.assertEqual(self.origem.saldo, 0)
        self.assertEqual(self.destino.saldo, 1200)


if __name__ == "__main__":
    unittest.main()
