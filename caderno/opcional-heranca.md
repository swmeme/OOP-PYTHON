# Exercício opcional — Herança e polimorfismo

> **Conceitos:** herança, sobrescrita, polimorfismo, princípio da substituição
> de Liskov.
> **Código:** `ContaComLimite.py`.
> **Exemplo:** `exemplos/opcional_polimorfismo.py`.

## 1. Por que este exercício vem depois

Herança é fácil de usar no lugar errado. Primeiro consolide objetos, métodos,
encapsulamento e composição. Só depois use herança quando existir uma relação
"é um tipo de" de verdade.

`ContaComLimite` **é um tipo de** `Conta`: aceita as mesmas operações públicas
e pode ser usada em qualquer lugar onde uma conta é esperada. Isso é
polimorfismo.

## 2. Como a extensão foi feita

```python
class ContaComLimite(Conta):
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
```

A subclasse **não reescreveu** `sacar` nem `transferir`. Ela só mudou a resposta
de `saldo_disponivel`. A conta mãe já usava essa propriedade na regra de débito.

Esse é o ponto-chave: a Parte 2 deixou um **gancho** (`saldo_disponivel`) e a
Parte opcional o preencheu. Herança funciona melhor quando a classe base foi
desenhada para isso.

## 3. Polimorfismo na prática

```python
def pagar(conta, valor):
    return conta.sacar(valor)

pagar(Conta(...), 100)
pagar(ContaComLimite(...), 140)
```

`pagar` não pergunta o tipo. Ela confia no contrato: "toda conta sabe sacar".
Quem decide *como* é o objeto.

## 4. Liskov

Uma subclasse deve poder substituir a classe base sem surpresas. Se
`ContaComLimite.sacar` recusasse um valor que `Conta.sacar` aceitaria, ou
imprimisse mensagens diferentes, o código que usa `Conta` quebraria.

Teste que verifica isso:

```python
def test_codigo_que_usa_conta_funciona_com_os_dois_tipos(self):
    def tentar_pagar(conta, valor):
        return conta.sacar(valor)

    comum = Conta(30, [self.cliente], 100)
    com_limite = ContaComLimite(31, [self.cliente], 100, limite=50)

    self.assertTrue(tentar_pagar(comum, 100))
    self.assertFalse(tentar_pagar(comum, 101))
    self.assertTrue(tentar_pagar(com_limite, 140))
```

## 5. Exercício

1. Rode o exemplo e compare as duas contas.
2. Crie `ContaPoupanca(Conta)` com um método `render(juros)` que credita
   `saldo * juros`.
3. Faça `render` usar `_creditar` com um tipo novo `RENDIMENTO`.
4. Escreva um teste que aplique `render(0.01)` em R$ 1000 e espere R$ 1010.
5. **Reflexão:** `ContaPoupanca` deveria sobrescrever `sacar`? Por quê?
6. **Reflexão:** quando composição seria melhor que herança aqui?

## 6. Resolução

Item 2–4:

```python
# ContaPoupanca.py
from Conta import Conta
from Movimentacao import Movimentacao

class ContaPoupanca(Conta):
    def render(self, juros):
        if not 0 < juros < 1:
            raise ValueError("juros deve estar entre 0 e 1")
        rendimento = round(self.saldo * juros, 2)
        return self._creditar(rendimento, Movimentacao.RENDIMENTO)
```

```python
# testes/test_conta_poupanca.py
def test_render_credita_juros(self):
    conta = ContaPoupanca(1, [self.cliente], 1000)
    self.assertTrue(conta.render(0.01))
    self.assertEqual(conta.saldo, 1010)
```

Não esqueça de adicionar `RENDIMENTO` em `Movimentacao.tipos_validos()`.

Itens 5–6: a poupança não deve mudar a regra de saque; se mudasse (por
exemplo, "só pode sacar no aniversário"), ela deixaria de ser substituível sem
surpresas e o código genérico quebraria. Nesse caso, talvez fosse melhor um
objeto de regra separado (composição) em vez de herança.

## 7. Como executar

```bash
python -m exemplos.opcional_polimorfismo
python -m unittest testes.test_conta_com_limite -v
```

## 8. Termina quando

- O mesmo código atende `Conta` e `ContaComLimite`.
- A subclasse não duplica a regra de saque.
- Você sabe explicar quando **não** usar herança.
