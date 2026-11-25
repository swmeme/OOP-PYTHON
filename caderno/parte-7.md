# Parte 7 — Testar o comportamento

> **Conceitos:** teste automatizado, `unittest`, padrão Arrange–Act–Assert,
> `setUp`, `subTest`, `assertRaises`.
> **Código:** pasta `testes/`.
> **Pré-requisito:** Partes 2, 5 e 6.

## 1. Objetivo

Verificar o comportamento esperado sem depender de conferir a tela à mão.
Cobrir depósito, saque, saldo insuficiente, transferência e histórico.

## 2. Conceito

Um teste automatizado é um programa que:

1. **prepara** um cenário (Arrange);
2. **executa** uma ação (Act);
3. **compara** o resultado com o esperado (Assert).

Se a comparação falhar, o teste falha e mostra o motivo. Você roda todos os
testes em segundos, sempre que muda o código.

`unittest` já vem no Python. A estrutura básica:

```python
import unittest

class TestConta(unittest.TestCase):
    def setUp(self):
        # roda antes de cada teste: cenário limpo
        self.conta = Conta(1, [Cliente("123", "Joao", "Rua 1")], 1000)

    def test_deposito_valido_atualiza_saldo(self):
        resultado = self.conta.depositar(500)      # Act
        self.assertTrue(resultado)                  # Assert
        self.assertEqual(self.conta.saldo, 1500)    # Assert
```

Por que `setUp`? Porque cada teste deve começar do mesmo estado. Se um teste
alterar a conta, o próximo não pode herdar a sujeira.

## 3. O que está coberto

| Arquivo | Foco |
| --- | --- |
| `testes/test_conta.py` | depósito, saque, validações, independência, saldo somente leitura |
| `testes/test_transferencia.py` | transferência válida, insuficiente, valor inválido, mesma conta |
| `testes/test_extrato.py` | movimentações, data, formatação sem alterar histórico |
| `testes/test_conta_com_limite.py` | herança e polimorfismo (opcional) |

Casos válidos **e** inválidos são testados. Um erro comum é testar só o
caminho feliz.

## 4. Exercício

1. Rode a suíte inteira.
2. Rode apenas um arquivo e apenas uma classe.
3. Escreva um teste novo: transferir R$ 100 de uma conta com R$ 50 deve
   devolver `motivo == "saldo_insuficiente"` e não mudar nenhum dos saldos.
4. **Desafio:** escreva um teste que prove que uma falha no meio da
   transferência não deixa histórico pela metade.
5. **Reflexão:** por que não testar via `print`?

## 5. Resolução

Item 3:

```python
def test_transferencia_sem_saldo_nao_muda_nada(self):
    antes_origem = len(self.origem.extrato)

    resultado = self.origem.transferir(self.destino, 100)

    self.assertFalse(resultado)
    self.assertEqual(resultado.motivo, "saldo_insuficiente")
    self.assertEqual(self.origem.saldo, self.saldo_inicial)
    self.assertEqual(self.destino.saldo, self.saldo_destino)
    self.assertEqual(len(self.origem.extrato), antes_origem)
```

Esse teste é mais forte que verificar só o retorno: ele confirma que **nada**
mudou.

Item 4: hoje a operação só debita depois de todas as validações, então o
histórico não fica pela metade. Um teste pode simular o cenário:

```python
def test_falha_no_credito_nao_deixa_debito_solto(self):
    class DestinoQuebrado(Conta):
        def _creditar(self, valor, tipo):
            return Resultado.falha("destino_quebrado")

    destino = DestinoQuebrado(2, [self.cliente], 0)

    with self.assertRaises(RuntimeError):
        self.origem.transferir(destino, 100)

    # Documenta o comportamento atual: o débito já aconteceu.
    self.assertEqual(self.origem.saldo, 900)
```

Esse teste mostra uma limitação real do desenho. O exercício seguinte seria
implementar o estorno e transformar o teste em "o saldo continua 1000".

## 6. Como executar

Todos os testes, a partir da raiz do projeto:

```bash
python -m unittest discover -s testes -t . -v
```

Um arquivo:

```bash
python -m unittest testes.test_conta -v
```

Uma classe:

```bash
python -m unittest testes.test_conta.TestConta -v
```

Um teste específico:

```bash
python -m unittest testes.test_conta.TestConta.test_saque_maior_que_saldo_e_recusado -v
```

Resultado esperado no final: `OK` (33 testes; 39 depois de acrescentar o
exercício opcional de herança).

## 7. Termina quando

- A suíte cobre os casos válidos e inválidos principais.
- Você consegue rodar tudo com um comando.
- Um teste falha de propósito quando você quebra uma regra (experimente trocar
  `>` por `>=` em `_debitar` e rode de novo).

## 8. Gabarito

<details>
<summary>Ver respostas</summary>

- **Por que não testar via `print`?** A saída é texto livre: muda de formato,
  depende do terminal e não diz *qual* regra falhou. `assertEqual` aponta
  exatamente o valor esperado e o obtido.
- **Testar implementação ou comportamento?** Comportamento: "saque acima do
  saldo é recusado e não altera nada". Assim você pode refatorar por dentro sem
  reescrever os testes.
- **O que é `subTest`?** Permite testar vários valores no mesmo teste, sem
  parar no primeiro erro. Veja `test_deposito_invalido_nao_altera_nada`.
- **Preciso de 100% de cobertura?** Não. Comece pelas regras de dinheiro e
  pelos casos de borda (zero, negativo, saldo exato, saldo + 1 centavo).

</details>
