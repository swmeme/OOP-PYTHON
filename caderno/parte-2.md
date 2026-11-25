# Parte 2 — A conta cuida do próprio saldo

> **Conceitos:** encapsulamento, atributo privado por convenção, `@property`,
> validação de entrada, retorno em vez de `print`.
> **Código:** `Conta.py`, `Resultado.py`.
> **Exemplo:** `exemplos/parte2_encapsulamento.py`.

## 1. Objetivo

Fazer com que **nenhum código fora de `Conta` altere o saldo diretamente**.
Depósitos e saques inválidos não podem mudar nada.

## 2. Conceito

Encapsular é juntar dados + regras no mesmo objeto e oferecer uma porta de
entrada pequena. Quem usa a conta não precisa saber que existe `_saldo`; só
precisa saber que existe `depositar` e `sacar`.

No código original, qualquer arquivo podia fazer:

```python
conta.saldo -= 100   # ninguém validou nada
conta.saldo += -50   # "depósito" que diminui o saldo
```

Agora:

```python
class Conta:
    def __init__(self, numero, clientes, saldo_inicial=0):
        ...
        self._saldo = 0

    @property
    def saldo(self):
        return self._saldo          # leitura liberada

    @property
    def saldo_disponivel(self):
        return self._saldo          # ponto de extensão (Parte opcional)

    def depositar(self, valor):
        return self._creditar(valor, Movimentacao.DEPOSITO)

    def sacar(self, valor):
        return self._debitar(valor, Movimentacao.SAQUE)
```

O prefixo `_` em `_saldo` é um **acordo** em Python: "não mexa aqui de fora".
Não é uma trava absoluta, mas deixa a intenção clara. Já `@property` sem
`setter` faz `conta.saldo = 999` levantar `AttributeError` de verdade.

## 3. As três regras

Toda mudança de saldo passa por dois métodos internos:

```python
def _creditar(self, valor, tipo):
    if not self._valor_valido(valor):
        return Resultado.falha("valor_invalido")
    self._saldo = round(self._saldo + valor, 2)
    self.extrato.registrar(Movimentacao(tipo, valor))
    return Resultado.sucesso()

def _debitar(self, valor, tipo):
    if not self._valor_valido(valor):
        return Resultado.falha("valor_invalido")
    if valor > self.saldo_disponivel:
        return Resultado.falha("saldo_insuficiente")
    self._saldo = round(self._saldo - valor, 2)
    self.extrato.registrar(Movimentacao(tipo, valor))
    return Resultado.sucesso()
```

1. **Valor válido:** número real, finito, maior que zero. `bool` é recusado de
   propósito (`True` vale 1 em Python, mas não é um valor monetário).
2. **Saldo suficiente:** compara com `saldo_disponivel`, não com `_saldo`.
3. **Registro:** a movimentação é criada no mesmo lugar em que o saldo muda.

> Detalhe didático: usamos `round(..., 2)` porque `float` tem erro de
> arredondamento (`0.1 + 0.2`). Para dinheiro de verdade, o ideal é `Decimal`.

## 4. Resultado em vez de mensagem

Métodos não imprimem. Eles **respondem**:

```python
class Resultado:
    def __init__(self, ok, motivo=None):
        self.ok = ok
        self.motivo = motivo

    @classmethod
    def sucesso(cls):
        return cls(True)

    @classmethod
    def falha(cls, motivo):
        return cls(False, motivo)

    def __bool__(self):
        return self.ok
```

Assim o script pode fazer `if conta.depositar(100):` e a conta continua sem
saber o que é um "print".

## 5. Exercício

1. Rode o exemplo e observe as tentativas inválidas.
2. Tente escrever (`conta.saldo = 1_000_000`) e anote o erro.
3. Confirme que `conta.depositar(True)` falha e explique por quê.
4. Explique por que `_debitar` compara com `saldo_disponivel` e não com `_saldo`.
5. **Desafio:** permita depósito de valor `Decimal` sem quebrar o resto.

## 6. Resolução

As respostas 1–4 estão no código. Para a 5, um caminho possível:

```python
from decimal import Decimal

@staticmethod
def _valor_valido(valor, permitir_zero=False):
    if isinstance(valor, bool):
        return False
    if not isinstance(valor, (int, float, Decimal)):
        return False
    if isinstance(valor, float) and not math.isfinite(valor):
        return False
    if isinstance(valor, Decimal) and not valor.is_finite():
        return False
    return valor >= 0 if permitir_zero else valor > 0
```

E, nos cálculos, converter o saldo para `Decimal` e arredondar com
`quantize(Decimal("0.01"))`. É uma melhoria real, mas misturar `float` e
`Decimal` no mesmo saldo gera `TypeError`; por isso ela fica como desafio, não
como parte do caminho principal.

## 7. Como executar

```bash
python -m exemplos.parte2_encapsulamento
```

Trecho esperado:

```text
depositar(0) -> Resultado(ok=False, motivo='valor_invalido') | saldo: 150
depositar(-30) -> Resultado(ok=False, motivo='valor_invalido') | saldo: 150
sacar(10000) -> Resultado(ok=False, motivo='saldo_insuficiente') | motivo: saldo_insuficiente | saldo: 150
AttributeError: property 'saldo' of 'Conta' object has no setter
```

## 8. Termina quando

- Nenhum trecho fora de `Conta` escreve no saldo.
- Depósito e saque inválidos deixam saldo **e histórico** iguais.
- `Conta` não imprime nada.

## 9. Gabarito

<details>
<summary>Ver respostas</summary>

- **Por que `saldo_disponivel`?** Porque a conta comum tem disponível igual ao
  saldo, mas a `ContaComLimite` (exercício opcional) soma o limite. Assim a
  regra de saque é escrita uma vez só.
- **Por que recusar `bool`?** `True == 1`; aceitar `True` como depósito de R$ 1
  esconde um erro de programação.
- **`_saldo` é privado de verdade?** Não. Python não impede o acesso; o `_` é
  convenção. A proteção forte vem de não expor um `setter` e de concentrar as
  regras nos métodos.
- **`round` resolve o problema de dinheiro?** Melhora a aparência, mas não é
  exato. `Decimal` é a ferramenta correta para valores monetários.

</details>
