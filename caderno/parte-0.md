# Parte 0 — Entender o projeto que já existia

> **Conceitos:** classe, objeto, atributo, método e `self`.
> **Código alterado nesta etapa:** nenhum. Esta parte é só observação.
> **Pré-requisito:** Python 3.10 ou mais novo.

> **Atenção:** esta parte foi escrita olhando o código **original**. O
> repositório de hoje já contém as correções das partes seguintes, então a
> sonda abaixo não roda mais como está. Para repetir a experiência, veja o
> código original com `git show 0c20314:Conta.py` (e os demais arquivos) ou
> consulte o histórico do repositório. A lista de falhas continua valendo como
> ponto de partida do estudo.

## 1. Objetivo

Ler o projeto original com calma, executá-lo e anotar o que funciona e o que
falha. Essas anotações são a linha de base: tudo o que vem depois corrige ou
melhora algo que você viu aqui.

## 2. Conceitos

| Termo | Ideia | No projeto |
| --- | --- | --- |
| **Classe** | O molde/planta que descreve dados e comportamentos. | `class Conta:` em `Conta.py` |
| **Objeto** | Uma coisa concreta criada a partir do molde. | `Conta(1, [...], 0)` |
| **Atributo** | Um dado guardado no objeto. | `self.saldo`, `self.numero` |
| **Método** | Uma função que pertence ao objeto. | `depositar()`, `sacar()` |
| **`self`** | O próprio objeto, dentro dos métodos. | `self.saldo += valor` |

Uma frase para guardar: **a classe é o molde; o objeto é a peça produzida com
esse molde.** `Conta` é a classe; `conta1` e `conta2` são dois objetos
diferentes, cada um com seu próprio saldo.

Onde está cada coisa no ponto de partida:

| Arquivo | Papel |
| --- | --- |
| `Cliente.py` | Define a classe `Cliente` (dados de quem é titular). |
| `Conta.py` | Define a classe `Conta` (número, clientes, saldo, extrato, operações). |
| `Extrato.py` | Define a classe `Extrato` (lista de movimentações e impressão). |
| `testecontas.py` | Script que cria objetos e chama métodos. Não define classe. |
| `testecontas2.py` | Outro script de teste manual, com duas contas. |

## 3. Roteiro de observação (sem alterar o código)

Rode os dois scripts na pasta do projeto:

```bash
python testecontas.py
python testecontas2.py
```

Depois rode esta sonda, que cria contas e tenta casos de borda. Ela só lê o
código original:

```python
import datetime
from Conta import Conta
from Cliente import Cliente

ana = Cliente("111", "Ana", "Rua A")

# 1) depósito e extrato
conta = Conta(10, [ana], 100)
conta.depositar(50)
print("saldo:", conta.saldo)
print("registro guardado:", conta.extrato.transactions[0])
try:
    conta.extrato.extrato(10)
except Exception as erro:
    print("ERRO:", type(erro).__name__, erro)

# 2) o saque entra no histórico?
antes = len(conta.extrato.transactions)
conta.sacar(30)
print("movimentações antes/depois:", antes, len(conta.extrato.transactions))

# 3) valores inválidos
conta.depositar(-20)
print("saldo após depositar -20:", conta.saldo)
conta.sacar(-20)
print("saldo após sacar -20:", conta.saldo)

# 4) cliente único, sem lista
conta2 = Conta(11, ana, 0)
try:
    conta2.gerar_extrato()
except Exception as erro:
    print("ERRO:", type(erro).__name__, erro)

# 5) transferência
origem = Conta(20, [ana], 100)
destino = Conta(21, [ana], 10)
print("retorno:", origem.transferenciaDEvalor(destino, 40))
print("saldos:", origem.saldo, destino.saldo)
print("tipos na origem:", [m[0] for m in origem.extrato.transactions])
print("tipos no destino:", [m[0] for m in destino.extrato.transactions])
print("retorno valor negativo:", origem.transferenciaDEvalor(destino, -10))
```

### O que foi observado

Saída real da sonda (resumida):

```text
saldo: 150
registro guardado: ['DEPOSITO: ', 50, 'DATA: ', <built-in method today ...>]
ERRO: AttributeError 'builtin_function_or_method' object has no attribute 'strftime'
movimentações antes/depois: 1 1
saldo após depositar -20: 100
saldo após sacar -20: 120
ERRO: TypeError 'Cliente' object is not iterable
retorno: Transferência realizada!
saldos: 60 50
tipos na origem: ['TRANSFERENCIA: ']
tipos no destino: ['DEPOSITO: ']
retorno valor negativo: Transferência realizada!
saldos após -10: 70 40
```

## 4. O que funciona e o que falha

Funciona:

- criar clientes e contas;
- depósito e saque no caminho feliz;
- `gerar_extrato()` com lista de clientes;
- transferência no caminho feliz.

Falhas e pontos fracos encontrados:

| # | Problema | Consequência | Corrigido na |
| --- | --- | --- | --- |
| 1 | `datetime.datetime.today` sem `()` no depósito | o extrato quebra com `AttributeError` | Parte 5 |
| 2 | saque não registra no extrato | histórico incompleto | Parte 5 |
| 3 | depósito/saque aceitam zero e negativo | saldo muda ao contrário | Parte 2 |
| 4 | `clientes` às vezes é lista, às vezes é um `Cliente` | `TypeError` ao gerar extrato | Parte 4 |
| 5 | transferência aceita valor negativo | dinheiro "aparece" do nada | Parte 2/6 |
| 6 | saldo é alterado direto de fora (`self.saldo -= ...`) | regra espalhada pelo código | Parte 2 |
| 7 | `Conta` imprime mensagens | regra e interface misturadas | Parte 3 |
| 8 | extrato da origem diz `TRANSFERENCIA`, o destino diz `DEPOSITO` | histórico incoerente | Parte 6 |
| 9 | `sataabertura` (erro de digitação) | atributo confuso | Parte 4 |
| 10 | não existem testes automatizados | conferência manual e frágil | Parte 7 |

> **Importante:** não conserte nada agora. Anotar primeiro é o que permite
> comparar o "antes" com o "depois".

## 5. Termina quando

Você consegue responder, sem olhar:

1. Qual arquivo define `Conta`? E `Cliente`? E `Extrato`?
2. Qual a diferença entre a classe `Conta` e o objeto `conta1`?
3. O que é `self` dentro de `depositar`?
4. O que acontece com `conta2` quando você deposita em `conta1`? Por quê?

## 6. Gabarito

<details>
<summary>Ver respostas</summary>

1. `Conta.py`, `Cliente.py` e `Extrato.py`.
2. `Conta` é a definição (o molde). `conta1` é um objeto criado a partir dela,
   com seus próprios valores de `numero`, `clientes`, `saldo` e `extrato`.
3. `self` é a conta que recebeu a chamada. Em `conta1.depositar(100)`, `self` é
   `conta1`.
4. Nada. Cada objeto tem seus próprios atributos; o saldo de `conta2` só muda
   se um método chamado em `conta2` (ou que receba `conta2`) alterar o estado
   dela.

</details>
