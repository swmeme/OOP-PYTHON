# Parte 4 — Como objetos se relacionam

> **Conceitos:** associação, composição, consistência de formato.
> **Código:** `Conta.py` (`_normalizar_clientes`, `self.extrato`), `Extrato.py`.
> **Exemplo:** `exemplos/parte4_composicao.py`.

## 1. Objetivo

Definir um formato único para os clientes de uma conta (sempre uma lista) e
manter um `Extrato` próprio dentro de cada conta.

## 2. Conceito

**Associação:** um objeto *aponta* para outro, mas não é dono dele.

```python
conta.clientes  # referências a objetos Cliente
```

O cliente existe fora da conta e pode estar em várias contas.

**Composição:** um objeto *contém* outro e cuida do seu ciclo de vida.

```python
self.extrato = Extrato(numero)   # criado junto com a conta
```

O extrato não é compartilhado: cada conta cria o seu no `__init__`. Se a conta
deixar de existir, aquele extrato também não tem uso.

O bug original era este:

```python
conta1 = Conta(1, [cliente1], 0)   # lista  -> funciona
conta2 = Conta(2, cliente2, 2000)  # objeto -> quebra ao iterar
```

A classe aceitava dois formatos e só descobria o problema depois, na hora de
usar. A correção é validar na entrada:

```python
@staticmethod
def _normalizar_clientes(clientes):
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
```

Repare em três decisões:

- recusar um `Cliente` solto **com uma mensagem que ensina o formato certo**;
- aceitar `tuple`, mas **copiar** para `list` (o estado interno não fica
  dependente da lista de quem chamou);
- validar todos os itens, não só o primeiro.

## 3. O extrato pertence à conta

```python
self.extrato = Extrato(numero)
```

Antes, o número da conta era passado na hora de imprimir
(`extrato.extrato(numero)`), o que permitia imprimir o extrato errado. Agora o
extrato já nasce sabendo de quem é.

## 4. Exercício

1. Crie duas contas: uma com um cliente, outra com dois. Gere o extrato das
   duas.
2. Tente criar uma conta passando um `Cliente` sem lista e copie a mensagem de
   erro.
3. Crie uma conta com uma `tuple` de clientes e verifique que
   `conta.clientes` é uma `list`.
4. **Desafio:** adicione um método `Conta.adicionar_cliente(cliente)` que
   valide o tipo e não permita CPF repetido.
5. Explique: `Conta` → `Cliente` é composição ou associação? E `Conta` →
   `Extrato`?

## 5. Resolução

Itens 1–3 estão em `exemplos/parte4_composicao.py`.

Item 4, uma solução possível:

```python
def adicionar_cliente(self, cliente):
    if not isinstance(cliente, Cliente):
        raise TypeError("adicionar_cliente espera um objeto Cliente")

    for existente in self.clientes:
        if existente.cpf == cliente.cpf:
            return Resultado.falha("cliente_repetido")

    self.clientes.append(cliente)
    return Resultado.sucesso()
```

E acrescente `"cliente_repetido"` ao dicionário de `mensagens.py`. Note que o
método devolve `Resultado`, mantendo o padrão da Parte 3.

Item 5: `Conta` → `Cliente` é **associação** (o cliente vive fora). `Conta` →
`Extrato` é **composição** (o extrato nasce e morre com a conta).

## 6. Como executar

```bash
python -m exemplos.parte4_composicao
```

Trecho esperado:

```text
conta 1 tem 0 movimentacoes
conta 2 tem 2 movimentacoes
TypeError: clientes deve ser uma lista, mesmo com um unico cliente: [cliente]
OK: um ou varios clientes funcionam igual, e os extratos sao independentes.
```

## 7. Termina quando

- Contas com um ou vários clientes funcionam do mesmo jeito.
- Cada conta mantém o próprio extrato.
- Passar o formato errado falha cedo, com mensagem clara.

## 8. Gabarito

<details>
<summary>Ver respostas</summary>

- **Por que copiar a lista?** Se `self.clientes = clientes` guardasse a mesma
  lista de fora, alguém poderia fazer `lista.append(...)` e mudar a conta sem
  passar por validação. `list(clientes)` cria uma lista própria.
- **Por que não aceitar um `Cliente` solto "por conveniência"?** Porque aí
  voltaríamos a ter dois formatos e todo método precisaria tratar os dois. Um
  formato só é mais simples de entender e testar.
- **O extrato poderia ser compartilhado?** Não faria sentido: o histórico é de
  uma conta específica.

</details>
