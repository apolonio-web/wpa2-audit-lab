# 🐍 Gerador de Wordlist Customizada

Ferramenta própria em Python para geração de wordlists por combinação
de caracteres, criada para uso no laboratório [`wpa2-audit-lab`](../).

## 🎯 Objetivo

Gerar uma wordlist customizada com base em um alfabeto reduzido e
específico, simulando senhas que seguem um padrão conhecido (por
exemplo, apenas números e um caractere especial), em vez de depender
de wordlists genéricas prontas.

## ⚙️ Como funciona

A ferramenta usa `itertools.product` para gerar todas as combinações
possíveis de um conjunto de caracteres, dentro de uma faixa de
tamanhos definida, e grava apenas as combinações que contêm pelo menos
um `@`.

| Parâmetro | Descrição | Valor usado no projeto |
|---|---|---|
| `caracteres` | Alfabeto usado na geração | `0123456789@` |
| `tamanho_min` | Tamanho mínimo da senha | 8 |
| `tamanho_max` | Tamanho máximo da senha | 9 |
| `nome_arquivo` | Arquivo de saída | `passwords.txt` |

## 🚀 Uso

```bash
python3 gerador.py
```

O script grava o resultado em `passwords.txt`, no mesmo diretório.

## 📄 Exemplo de saída

``
10000000@
10000001@
10000002@
```


## ⚠️ Sobre o tamanho do arquivo

Como a geração é por força bruta combinatória, o número de senhas
cresce exponencialmente com o tamanho. Para um alfabeto de 11
caracteres, o tamanho 9 já representa até ~2,36 bilhões de
combinações antes do filtro do `@`. Por isso o `tamanho_max` deve ser
ajustado com cuidado, dependendo do poder de processamento disponível
e do tempo aceitável de teste.

No teste documentado neste projeto, a wordlist gerada por este script
não foi a que efetivamente quebrou a senha. Uma wordlist menor e mais
direcionada (11.333 senhas), baseada em um padrão mais específico,
obteve sucesso em segundos. Isso reforça que wordlists direcionadas
tendem a ser mais eficientes do que a força bruta pura, quando há
indícios do padrão da senha.

## 🔜 Possíveis melhorias futuras

- Adicionar suporte a letras maiúsculas/minúsculas
- Permitir múltiplos caracteres obrigatórios (não só `@`)
- Gerar a wordlist em streaming direto para o Hashcat, sem salvar em
  disco, para reduzir o uso de espaço
- Adicionar parâmetros via linha de comando (`argparse`), em vez de
  editar o código para mudar configurações

## ⚖️ Uso responsável

Esta ferramenta foi desenvolvida exclusivamente para fins educacionais
e para uso em testes de segurança autorizados, em ambientes próprios
ou com permissão explícita. Veja o [aviso legal](../#%EF%B8%8F-aviso-legal)
completo no README principal do projeto.
