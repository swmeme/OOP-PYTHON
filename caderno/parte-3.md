# Parte 3 — Separar regras de mensagens

> **Conceitos:** abstração, separação de responsabilidades, camada de
> apresentação.
> **Código:** `Conta.py` (já sem `print`), `Resultado.py`, `mensagens.py`.
> **Exemplo:** `exemplos/parte3_mensagens.py`.

## 1. Objetivo

Manter as regras em `Conta` e deixar as frases ("Saldo insuficiente") para o
script que conversa com a pessoa.

## 2. Conceito

Abstrair é oferecer uma operação simples e esconder os passos internos. Mas
abstração também é saber **onde cada responsabilidade mora**:

| Pergunta | Quem responde |
| --- | --- |
| O valor é válido? | `Conta` |
| Há saldo suficiente? | `Conta` |
| Como o saldo é atualizado? | `Conta` |
| Que frase mostrar? | `mensagens.py` / script |
| Onde mostrar? | script / tela |

Se a `Conta` imprimisse "Saldo insuficiente", ela ficaria presa a uma língua,
a um formato e a um meio (terminal). No dia em que o projeto virar API ou
aplicativo, a regra teria de ser reescrita.

## 3. O contrato da conta

```python
resultado = conta.sacar(500)

if resultado:                  # usa Resultado.__bool__
    print("Saque feito")
else:
    print(resultado.motivo)    # "saldo_insuficiente"
```

`motivo` é um **código**, não uma frase. Isso permite traduzir:

```python
MENSAGENS = {
    "valor_invalido": "O valor precisa ser um numero maior que zero.",
    "saldo_insuficiente": "Saldo insuficiente para esta operacao.",
    "mesma_conta": "Nao e possivel transferir para a mesma conta.",
    "destino_invalido": "A conta de destino nao foi informada corretamente.",
}

def descrever(resultado):
    if resultado:
        return "Operacao realizada."
    return MENSAGENS.get(resultado.motivo, "Operacao nao realizada.")
```

## 4. Exercício

1. Rode o exemplo e compare a "tela simples" com a "tela técnica".
2. Responda: quem sabe que o motivo se chama `saldo_insuficiente`? Quem sabe
   que a frase é "Saldo insuficiente"?
3. Crie uma terceira interface que mostre tudo em maiúsculas.
4. **Desafio:** faça uma versão em inglês sem tocar em `Conta.py`.
5. **Reflexão:** por que `Resultado` não deveria ter um método `imprimir()`?

## 5. Resolução

Item 3, sem alterar a conta:

```python
def tela_gritando(rotulo, resultado):
    texto = descrever(resultado)
    print(f"*** {rotulo.upper()}: {texto.upper()} ***")
```

Item 4, trocando só o dicionário:

```python
MENSAGENS_EN = {
    "valor_invalido": "The amount must be greater than zero.",
    "saldo_insuficiente": "Insufficient funds.",
    "mesma_conta": "You cannot transfer to the same account.",
    "destino_invalido": "Invalid destination account.",
}
```

Item 5: porque imprimir é uma decisão de interface. `Resultado` é um dado do
domínio; se ele chamasse `print`, voltaríamos ao problema que a parte resolve.
Quem decide o destino do texto é quem chama.

## 6. Como executar

```bash
python -m exemplos.parte3_mensagens
```

Saída esperada (trecho):

```text
[tela] deposito 50: feito
[log]   deposito 50: ok
[tela] saque 500: Saldo insuficiente para esta operacao.
[log]   saque 500: falhou (saldo_insuficiente)
[tela] saque -10: O valor precisa ser um numero maior que zero.
[log]   saque -10: falhou (valor_invalido)
```

## 7. Termina quando

- Uma operação pode ser usada sem que `Conta` imprima nada.
- Trocar as mensagens não exige editar `Conta.py`.
- Você sabe explicar a diferença entre **motivo** (dado) e **mensagem** (texto
  de interface).

## 8. Gabarito

<details>
<summary>Ver respostas</summary>

- **Quem conhece o motivo?** `Conta` (quem produz) e `mensagens.py` (quem
  traduz). O resto do sistema só repassa o código.
- **Quem conhece a frase?** Apenas a camada de apresentação.
- **`Resultado.imprimir()` seria ruim?** Sim: acoplaria o domínio ao terminal,
  dificultaria testes (capturar `stdout` é chato) e impediria reutilizar a
  mesma regra em uma API.
- **Isso é MVC?** É uma versão simples da mesma ideia: modelo (Conta/Extrato),
  visão (mensagens/script) e controle (o script que dispara as operações).

</details>
