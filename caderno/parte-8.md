# Parte 8 — Revisar e apresentar o projeto

> **Conceitos:** organização de código, responsabilidade de cada módulo,
> documentação executável.
> **Código:** repositório inteiro + `README.md`.

## 1. Objetivo

Deixar o projeto compreensível para outra pessoa: ela deve conseguir entender o
propósito, executar o programa e rodar os testes seguindo o README.

## 2. Responsabilidades

| Arquivo | Responsabilidade | Não faz |
| --- | --- | --- |
| `Cliente.py` | guardar dados do titular | não valida saldo, não imprime |
| `Conta.py` | validar e executar operações, proteger o saldo | não imprime, não formata extrato |
| `Extrato.py` | guardar e formatar o histórico | não decide se uma operação é válida |
| `Movimentacao.py` | representar um fato (tipo, valor, data) | não altera conta |
| `Resultado.py` | dizer se deu certo e por quê | não traduz para frases |
| `ContaComLimite.py` | acrescentar limite de crédito | não reescreve saque |
| `mensagens.py` | traduzir motivo → frase | não altera saldo |
| `testecontas.py` | demonstrar o uso | não define regra |
| `exemplos/` | um roteiro por capítulo | não é biblioteca |
| `testes/` | verificar comportamento | não imprime relatório manual |

Regra prática: se você não consegue dizer em uma frase o que o arquivo faz,
provavelmente ele tem responsabilidades demais.

## 3. Exercício de revisão

Responda antes de abrir o gabarito:

1. Onde está a única linha que soma dinheiro ao saldo? E a que subtrai?
2. Se o banco decidir cobrar tarifa, qual arquivo muda?
3. Se o extrato precisar ser impresso em PDF, qual arquivo muda?
4. Se a frase "Saldo insuficiente" mudar, qual arquivo muda?
5. Por que `Resultado` e `Movimentacao` são classes separadas?
6. O que aconteceria se `Extrato` guardasse o saldo também?

## 4. Revisão do código

Faça esta checagem no repositório:

- [ ] Nenhum `print` dentro de `Cliente.py`, `Conta.py`, `Extrato.py`,
      `Movimentacao.py` ou `Resultado.py`.
- [ ] Nenhum acesso a `_saldo` fora de `Conta.py`/`ContaComLimite.py`.
- [ ] `Conta` sempre recebe uma lista de clientes.
- [ ] Toda movimentação tem tipo, valor e data.
- [ ] `transferir` não duplica registros de saque/depósito.
- [ ] Os testes passam com `python -m unittest discover -s testes -t .`.
- [ ] O README explica como rodar tudo, sem depender de conhecimento prévio.

## 5. Roteiro de apresentação (5 minutos)

1. **Problema:** estudar OOP com um banco didático, sem dados reais.
2. **Modelo:** mostre `Cliente`, `Conta`, `Extrato`, `Movimentacao` no quadro.
3. **Encapsulamento:** mostre `conta.saldo = 999` falhando.
4. **Regra × mensagem:** mostre `Resultado(motivo=...)` e `mensagens.py`.
5. **Composição:** mostre duas contas com extratos independentes.
6. **Transferência:** mostre o antes/depois dos saldos e os dois extratos.
7. **Testes:** rode a suíte e mostre um teste falhando de propósito.
8. **Próximos passos:** `Decimal`, type hints, persistência, API.

## 6. O que mudou em relação ao projeto original

| Antes | Agora |
| --- | --- |
| `numeroConta` | `numero` |
| `nomeTitular` | `nome_titular` |
| `sataabertura` | `data_abertura` |
| `extrato.transactions` (listas) | `extrato.movimentacoes` (objetos) |
| `transferenciaDEvalor` | `transferir` |
| `gerar_extrato()` | `conta.resumo()` + `conta.extrato.formatar()` |
| `gerar_saldo()` | `conta.resumo()` |
| `Extrato.extrato(numero)` | `Extrato.formatar()` |
| `saldo` público | `_saldo` + `@property saldo` |
| mensagens dentro da conta | `Resultado.motivo` + `mensagens.py` |

As renomeações seguem o padrão do Python (PEP 8) e deixam claro o papel de cada
atributo. Os conceitos continuam os mesmos; só ficaram mais fáceis de ler.

## 7. Termina quando

Outra pessoa, sem ajuda, consegue:

1. clonar o repositório;
2. rodar a demonstração;
3. rodar os testes;
4. apontar o que cada arquivo faz;
5. explicar por que o saldo não pode ser alterado de fora.

## 8. Gabarito

<details>
<summary>Ver respostas</summary>

1. `Conta._creditar` soma; `Conta._debitar` subtrai.
2. `Conta.py` (ou uma subclasse, se a tarifa for opcional). A mensagem nova
   ficaria em `mensagens.py`.
3. Apenas a camada de apresentação: hoje `Extrato.formatar()` devolve texto;
   um gerador de PDF consumiria os mesmos dados.
4. `mensagens.py`.
5. Porque têm ciclos de vida e papéis diferentes: `Resultado` é a resposta de
   uma ação; `Movimentacao` é um fato registrado no histórico.
6. O extrato passaria a ter duas fontes de verdade sobre o dinheiro (o saldo e
   as movimentações), que podem divergir. O saldo é responsabilidade da conta;
   o extrato só relata fatos.

</details>

## 9. Próximos passos sugeridos

- trocar `float` por `Decimal`;
- adicionar type hints (`def sacar(self, valor: float) -> Resultado:`);
- transformar `Movimentacao` em `@dataclass(frozen=True)`;
- persistir contas em JSON ou SQLite;
- criar uma API com Flask/FastAPI reutilizando as mesmas classes;
- separar `Conta` em conta + serviço de transferência quando as regras
  crescerem.
