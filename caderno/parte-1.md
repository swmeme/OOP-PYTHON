# Parte 1 — Criar e comparar objetos

> **Conceitos:** instância, estado independente, identidade.
> **Código de apoio:** `testecontas2.py`.
> **Pré-requisito:** Parte 0.

## 1. Objetivo

Criar duas contas diferentes, fazer um depósito em uma e provar que a outra
não mudou.

## 2. Conceito

Um objeto é uma **instância** de uma classe. A classe descreve *quais* dados
existem; cada objeto guarda *os seus*. É como a planta de uma casa (classe) e
duas casas construídas com ela (objetos): mudar a cor da porta de uma casa não
pinta a outra.

Em Python, `conta1 is conta2` é `False` e `id(conta1) != id(conta2)`. Mesmo
assim, os dois podem ser do mesmo tipo:

```python
isinstance(conta1, Conta)  # True
isinstance(conta2, Conta)  # True
```

## 3. Exercício

Antes de rodar qualquer coisa, tente escrever sozinho:

1. Crie dois clientes fictícios com CPFs diferentes.
2. Crie `conta1` (número 1, cliente 1, saldo 0) e `conta2` (número 2, cliente 2,
   saldo 2000).
3. Imprima os saldos.
4. Deposite 1500 na `conta1`.
5. Imprima os saldos de novo.
6. Use `assert` para garantir que `conta2.saldo` continua 2000.

Critério de aceite: a saída mostra `conta1` com 1500 e `conta2` com 2000.

## 4. Resolução

O arquivo `testecontas2.py` já está pronto para executar:

```python
from Cliente import Cliente
from Conta import Conta

joao = Cliente("123", "Joao", "Rua 1")
maria = Cliente("345", "Maria", "Rua 2")

conta1 = Conta(1, [joao], 0)
conta2 = Conta(2, [maria], 2000)

print(f"Antes -> conta 1: R$ {conta1.saldo:.2f} | conta 2: R$ {conta2.saldo:.2f}")

conta1.depositar(1500)

print(f"Depois -> conta 1: R$ {conta1.saldo:.2f} | conta 2: R$ {conta2.saldo:.2f}")

assert conta1.saldo == 1500, "a conta 1 deveria ter recebido o depósito"
assert conta2.saldo == 2000, "a conta 2 não poderia ser afetada"
```

Pontos para observar:

- `conta1` e `conta2` são criados com a **mesma classe**, mas recebem dados
  diferentes no `__init__`.
- Cada `__init__` cria um `self.extrato` novo. Ou seja: além do saldo, o
  histórico também é independente.
- `assert` é uma verificação barata: se a frase seguinte for falsa, o programa
  para com erro. Na Parte 7 isso vira teste automatizado de verdade.

## 5. Como executar

```bash
python testecontas2.py
```

Saída esperada:

```text
Antes -> conta 1: R$ 0.00 | conta 2: R$ 2000.00
Depois -> conta 1: R$ 1500.00 | conta 2: R$ 2000.00
OK: cada objeto Conta guarda o proprio saldo.
```

## 6. Variação do exercício

Troque a ordem: deposite 500 na `conta2` e confira que `conta1` continua 1500.
Depois crie `conta3` reaproveitando o mesmo objeto `joao`:

```python
conta3 = Conta(3, [joao], 0)
```

Pergunta: `joao` é o mesmo objeto nas três contas? O que isso significa?

## 7. Termina quando

- Você mostra, com números na tela, que duas instâncias de `Conta` têm estados
  diferentes.
- Você explica por que `conta1.depositar(...)` não altera `conta2`.

## 8. Gabarito

<details>
<summary>Ver respostas</summary>

- `joao` é o **mesmo** objeto `Cliente` referenciado por várias contas. Isso é
  uma **associação**: a conta aponta para um cliente, mas não o copia. Se o
  endereço de `joao` mudar, todas as contas que apontam para ele enxergam o
  novo endereço. Nesta parte ainda é só uma lista de referências; na Parte 4
  vamos padronizar esse formato.
- O saldo não é compartilhado porque `_saldo` (ou `saldo`, no código original)
  é um atributo de instância, criado dentro de `__init__` com `self`.

</details>
