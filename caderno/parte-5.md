# Parte 5 — Registrar movimentações

> **Conceitos:** objeto de valor/histórico, data, imutabilidade na prática,
> formatação sem efeito colateral.
> **Código:** `Movimentacao.py`, `Extrato.py`, `Conta.py`.
> **Exemplo:** `exemplos/parte5_movimentacoes.py`.

## 1. Objetivo

Registrar depósito, saque e transferência com **tipo, valor e data**. Corrigir
o bug da data e fazer o extrato mostrar tudo sem alterar o histórico.

## 2. Conceito

Nem todo objeto representa uma "coisa" (Cliente, Conta). Alguns representam
**fatos que aconteceram**. `Movimentacao` é isso: um registro histórico.

```python
class Movimentacao:
    ABERTURA = "ABERTURA"
    DEPOSITO = "DEPOSITO"
    SAQUE = "SAQUE"
    TRANSFERENCIA_ENVIADA = "TRANSFERENCIA_ENVIADA"
    TRANSFERENCIA_RECEBIDA = "TRANSFERENCIA_RECEBIDA"

    def __init__(self, tipo, valor, data=None):
        ...
        self.tipo = tipo
        self.valor = valor
        self.data = data if data is not None else datetime.now()
```

O bug original era sutil:

```python
datetime.datetime.today    # a função (sem parênteses)
datetime.datetime.today()  # a data de agora
```

Sem `()`, o extrato guardava a **função**, e `strftime` quebrava. O conserto é
chamar a função.

## 3. Tipos como constantes

Em vez de espalhar strings soltas, a classe oferece nomes:

```python
Movimentacao.DEPOSITO   # "DEPOSITO"
```

Assim um erro de digitação vira `ValueError` na criação, e não um texto
estranho no extrato. O construtor valida tipo, valor e data.

## 4. Extrato: registrar e formatar

```python
def registrar(self, movimentacao):
    if not isinstance(movimentacao, Movimentacao):
        raise TypeError("o extrato so aceita objetos Movimentacao")
    self._movimentacoes.append(movimentacao)

@property
def movimentacoes(self):
    return tuple(self._movimentacoes)

def formatar(self):
    linhas = [f"Extrato da conta {self.numero_conta}", "-" * 52]
    ...
    return "\n".join(linhas)
```

Duas proteções didáticas:

- `movimentacoes` devolve uma **tupla**: quem está fora pode ler, mas não
  consegue `append`/`remove`.
- `formatar()` só **lê** a lista. Nada de ordenar, remover ou recriar itens.

## 5. Exercício

1. Rode o exemplo e observe `repr` de cada movimentação (tipo, valor, data).
2. Confirme que o extrato mostra a data no formato `dd/mm/aaaa`.
3. Crie uma movimentação com data fixa (`datetime(2024, 3, 15, 9, 30)`) e
   formate.
4. Tente `conta.extrato.movimentacoes.append(...)` e anote o erro.
5. **Desafio:** crie o tipo `PIX` e registre um depósito via PIX.

## 6. Resolução

Item 5, sem inventar outro mecanismo:

```python
# Movimentacao.py
PIX_RECEBIDO = "PIX_RECEBIDO"

@classmethod
def tipos_validos(cls):
    return (..., cls.PIX_RECEBIDO)

# Conta.py
def receber_pix(self, valor):
    return self._creditar(valor, Movimentacao.PIX_RECEBIDO)
```

O ideal é que toda operação nova passe por `_creditar`/`_debitar`; assim a
validação e o registro continuam em um lugar só.

Ponto importante sobre a data: `date.today()` e `datetime.now()` são
**avaliados na hora da chamada**. Por isso não se guarda a função, e sim o
resultado dela.

## 7. Como executar

```bash
python -m exemplos.parte5_movimentacoes
```

Trecho esperado:

```text
Movimentacao(tipo='DEPOSITO', valor=50, data=datetime.datetime(2026, 11, 25, ...))
DEPOSITO               R$      50.00   25/11/2026 10:58
...
mesmo historico? True
```

## 8. Termina quando

- Cada operação válida aparece no extrato com tipo, valor e data.
- A data é um `datetime` e pode ser formatada.
- Formatar o extrato não muda o histórico.

## 9. Gabarito

<details>
<summary>Ver respostas</summary>

- **Por que uma classe em vez de uma lista `[tipo, valor, data]`?** Porque
  `mov.tipo` é mais legível que `mov[0]`, o construtor valida os dados e o
  `repr` ajuda a depurar. A lista original era frágil: qualquer posição errada
  quebrava a formatação.
- **A movimentação pode ser alterada depois?** Python não impede
  `mov.valor = 999`. A convenção é tratar o objeto como histórico imutável. Um
  próximo passo seria `@dataclass(frozen=True)`.
- **Por que `tuple` no `movimentacoes`?** Para proteger o histórico de
  alterações externas por acidente.

</details>
