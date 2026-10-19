# 📂 Evidências

Logs de execução de cada etapa do laboratório, extraídos diretamente
do terminal durante os testes. Todos os BSSIDs, endereços MAC e a
senha recuperada foram ocultados ou omitidos antes da publicação.

## 🗂️ Índice

| Arquivo | Etapa | Ferramenta |
|---|---|---|
| [`01-setup-monitor-mode.txt`](./01-setup-monitor-mode.txt) | Preparação do ambiente | `airmon-ng` |
| [`02-reconhecimento.txt`](./02-reconhecimento.txt) | Reconhecimento da rede-alvo | `airodump-ng` |
| [`03-captura-direcionada.txt`](./03-captura-direcionada.txt) | Captura direcionada e handshake | `airodump-ng` |
| [`04-deauth.txt`](./04-deauth.txt) | Deautenticação | `aireplay-ng` |
| [`05-conversao-hcxpcapngtool.txt`](./05-conversao-hcxpcapngtool.txt) | Conversão do handshake | `hcxpcapngtool` |
| [`06-hashcat.txt`](./06-hashcat.txt) | Teste de dicionário | `hashcat` |

## ⚠️ Nota sobre sanitização

Os seguintes dados foram removidos ou substituídos antes da publicação:

- **BSSID** da rede-alvo → substituído por `XX:XX:XX:XX:XX:XX`
- **Endereços MAC** dos dispositivos conectados → substituídos por `XX:XX:XX:XX:XX:XX`
- **Senha recuperada** → omitida, confirmado apenas o status de sucesso

> 📄 Para a análise completa de cada etapa, com comandos e contexto,
> veja o [README principal](../readme.md).
