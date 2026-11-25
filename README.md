# OOP-PYTHON — banco didático

Projeto de estudo de **Programação Orientada a Objetos** em Python, usando um
banco fictício como desculpa para praticar classes, objetos, encapsulamento,
composição, histórico de operações, transferências, testes e (opcionalmente)
herança.

> Todos os dados são inventados. O projeto não acessa dinheiro real, não guarda
> informações pessoais e não deve ser usado como sistema bancário.

## Requisitos

- Python 3.10 ou mais novo (testado com 3.12).
- Nenhuma biblioteca externa: só a biblioteca padrão.

## Começando

Na raiz do projeto:

```bash
# demonstração principal
python testecontas.py

# duas contas independentes (Parte 1)
python testecontas2.py

# todos os testes automatizados
python -m unittest discover -s testes -t . -v
```

No Windows, se `python` não funcionar, use `py` no lugar.

Saída esperada dos testes:

```text
Ran 39 tests in 0.003s

OK
```

## Estrutura

```text
OOP-PYTHON/
├── Cliente.py            # dados do titular
├── Conta.py              # regras da conta (o saldo só muda aqui)
├── Extrato.py            # histórico de uma conta
├── Movimentacao.py       # um fato: tipo + valor + data
├── Resultado.py          # resposta de uma operação (ok + motivo)
├── ContaComLimite.py     # exercício opcional de herança
├── mensagens.py          # tradução de motivo -> frase
├── testecontas.py        # demonstração principal
├── testecontas2.py       # demonstração de duas contas independentes
├── caderno/              # aulas: conceito, exercício e resolução
├── exemplos/             # um script executável por capítulo
└── testes/               # suíte unittest
```

## Como estudar

Cada capítulo do `caderno/` tem a mesma estrutura: conceito, exercício,
resolução comentada, como executar, critério de conclusão e gabarito.

| Parte | Tema | Execute |
| --- | --- | --- |
| [0](caderno/parte-0.md) | Ler o projeto e anotar o que falha | `python testecontas.py` |
| [1](caderno/parte-1.md) | Objetos e estados independentes | `python testecontas2.py` |
| [2](caderno/parte-2.md) | Encapsulamento do saldo | `python -m exemplos.parte2_encapsulamento` |
| [3](caderno/parte-3.md) | Regras × mensagens | `python -m exemplos.parte3_mensagens` |
| [4](caderno/parte-4.md) | Associação e composição | `python -m exemplos.parte4_composicao` |
| [5](caderno/parte-5.md) | Movimentações e datas | `python -m exemplos.parte5_movimentacoes` |
| [6](caderno/parte-6.md) | Transferência entre contas | `python -m exemplos.parte6_transferencias` |
| [7](caderno/parte-7.md) | Testes com `unittest` | `python -m unittest discover -s testes -t . -v` |
| [8](caderno/parte-8.md) | Revisão e apresentação | leitura + checklist |
| [Opcional](caderno/opcional-heranca.md) | Herança e polimorfismo | `python -m exemplos.opcional_polimorfismo` |

## O modelo em uma olhada

```python
from Cliente import Cliente
from Conta import Conta

joao = Cliente("123", "Joao", "Rua 1")
conta = Conta(1, [joao], 100)

resultado = conta.depositar(50)
print(resultado.ok)          # True
print(conta.saldo)           # 150

resultado = conta.sacar(500)
print(resultado.ok)          # False
print(resultado.motivo)      # saldo_insuficiente
print(conta.saldo)           # 150 (nada mudou)

print(conta.extrato.formatar())
```

Regras de ouro do projeto:

1. O saldo só muda dentro de `Conta` (via `_creditar`/`_debitar`).
2. `Conta` não imprime: devolve `Resultado`.
3. `clientes` é sempre uma lista, mesmo com um único titular.
4. Cada conta tem o próprio `Extrato`.
5. Toda movimentação tem tipo, valor e data.
6. Transferência é tudo ou nada, e gera um registro em cada conta.

## Decisões de projeto

- **`_saldo` + `@property`**: leitura livre, escrita bloqueada de fora.
- **`Resultado`**: separa "o que aconteceu" de "como mostrar".
- **`Movimentacao`**: histórico é uma sequência de objetos, não de listas
  posicionais.
- **`saldo_disponivel`**: gancho que permite limite de crédito sem reescrever
  a regra de saque.
- **`Extrato.formatar()`**: devolve texto; não imprime nem altera o histórico.
- **`round(..., 2)`**: melhora a exibição, mas o ideal para dinheiro é
  `Decimal` (veja os próximos passos na Parte 8).

## O que mudou em relação ao código inicial

| Antes | Agora |
| --- | --- |
| `numeroConta` | `numero` |
| `nomeTitular` | `nome_titular` |
| `sataabertura` | `data_abertura` |
| `extrato.transactions` | `extrato.movimentacoes` |
| `transferenciaDEvalor` | `transferir` |
| `gerar_extrato()` | `conta.resumo()` + `extrato.formatar()` |
| `gerar_saldo()` | `conta.resumo()` |
| `saldo` público | `_saldo` + `@property saldo` |
| mensagens dentro da conta | `Resultado.motivo` + `mensagens.py` |

## Limites deste projeto

- Não há persistência: ao encerrar o Python, os objetos somem.
- Não há autenticação, agência, cartão, limite de crédito rotativo, juros etc.
- `float` é usado para simplificar o estudo; dinheiro de verdade pede
  `Decimal`.
- Não é um sistema bancário. É um caderno de exercícios executável.

## Próximos passos

1. Trocar `float` por `Decimal`.
2. Adicionar type hints.
3. Transformar `Movimentacao` em `@dataclass(frozen=True)`.
4. Persistir contas em JSON ou SQLite.
5. Criar uma API (Flask/FastAPI) reutilizando as mesmas classes.
6. Implementar estorno de transferência e testar a falha no meio do caminho.
