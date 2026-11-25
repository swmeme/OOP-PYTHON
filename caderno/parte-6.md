# Parte 6 — Transferências entre objetos

> **Conceitos:** colaboração entre objetos, operação "tudo ou nada",
> consistência de histórico.
> **Código:** `Conta.transferir`, `_debitar`, `_creditar`.
> **Exemplo:** `exemplos/parte6_transferencias.py`.

## 1. Objetivo

Mover dinheiro de uma conta para outra de forma coerente: o valor sai de uma,
chega à outra e as duas registram o fato.

## 2. Conceito

Transferir é uma **colaboração**: uma conta não mexe no saldo da outra. Ela
pede que a outra se credite.

```python
def transferir(self, destino, valor):
    if not isinstance(destino, Conta):
        return Resultado.falha("destino_invalido")
    if destino is self:
        return Resultado.falha("mesma_conta")

    retirada = self._debitar(valor, Movimentacao.TRANSFERENCIA_ENVIADA)
    if not retirada:
        return retirada

    credito = destino._creditar(valor, Movimentacao.TRANSFERENCIA_RECEBIDA)
    if not credito.ok:
        raise RuntimeError("falha inesperada ao creditar a conta de destino")

    return Resultado.sucesso()
```

Por que `_debitar`/`_creditar` e não `sacar`/`depositar`?

- `sacar` registraria um `SAQUE` **e** a transferência registraria outro item:
  o histórico ficaria duplicado.
- `_debitar`/`_creditar` são os métodos que realmente mudam o saldo; recebem o
  **tipo** da movimentação. Assim cada fato gera exatamente um registro.

A conta de destino continua sendo quem altera o próprio saldo: a origem só
chama o método interno dela. Nenhuma conta escreve `outra._saldo`.

## 3. Ordem das verificações

1. destino é uma conta?
2. é a mesma conta?
3. o valor é válido?
4. há saldo disponível?

As três primeiras não mudam nada. A quarta está dentro de `_debitar`. Se
qualquer uma falhar, **nenhum** saldo e **nenhum** histórico mudam. Isso é o
que se chama de operação atômica ("tudo ou nada").

## 4. Exercício

1. Rode o exemplo e confira os dois extratos.
2. Transfira o saldo inteiro e veja o resultado.
3. Tente transferir para a própria conta.
4. **Desafio:** registre também uma taxa de R$ 2,00 por transferência, saindo
   da origem. Onde essa regra deve morar?
5. **Reflexão:** o que aconteceria se `_creditar` do destino falhasse depois do
   débito? Como você tornaria a operação reversível?

## 5. Resolução

Item 4: a taxa é uma regra da conta de origem, então fica em `transferir` ou em
uma subclasse. Uma versão simples:

```python
TAXA_TRANSFERENCIA = 2.00

def transferir(self, destino, valor):
    ...
    total = valor + self.TAXA_TRANSFERENCIA
    retirada = self._debitar(total, Movimentacao.TRANSFERENCIA_ENVIADA)
    ...
```

Mas atenção: agora o valor debitado (`valor + taxa`) é diferente do valor
creditado (`valor`). O extrato precisa deixar isso explícito, talvez com dois
registros: `TRANSFERENCIA_ENVIADA` (valor) e `TARIFA` (taxa).

Item 5: o código atual valida antes de debitar e considera o crédito
"impossível de falhar" (mesmo valor já validado). Se quiséssemos robustez
total, faríamos:

```python
if not credito.ok:
    self._creditar(valor, Movimentacao.ESTORNO)   # desfaz o débito
    return Resultado.falha("transferencia_nao_concluida")
```

Isso exige um tipo novo de movimentação e um teste específico. É um bom
exercício depois da Parte 7.

## 6. Como executar

```bash
python -m exemplos.parte6_transferencias
```

Trecho esperado:

```text
  Operacao realizada.
  origem: R$ 300.00 | destino: R$ 300.00
...
TRANSFERENCIA_ENVIADA  R$     200.00   ...
TRANSFERENCIA_RECEBIDA R$     200.00   ...
OK: o valor saiu de uma conta, chegou a outra e as duas registram o fato.
```

## 7. Termina quando

- O valor sai de uma conta e chega à outra.
- As duas contas refletem a transferência no histórico, com tipos diferentes.
- Falhas não alteram nenhum dos dois lados.

## 8. Gabarito

<details>
<summary>Ver respostas</summary>

- **Por que a origem não faz `destino._saldo += valor`?** Porque isso quebraria
  o encapsulamento (Parte 2) e pularia a validação e o registro do destino.
- **Por que recusar transferir para si mesma?** Sem essa checagem, o débito e o
  crédito se anulariam, mas o histórico ganharia duas linhas inúteis.
- **E se o valor for 0?** `_debitar` recusa antes de qualquer mudança.
- **Duas contas no mesmo arquivo podem se conhecer?** Sim. Elas colaboram por
  métodos públicos/internos, sem compartilhar o atributo `_saldo`.

</details>
