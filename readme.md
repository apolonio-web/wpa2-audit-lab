<div align="center">

# 🔐 WPA2 Audit Lab

**Auditoria de segurança WPA2 em ambiente controlado, com ferramenta própria de geração de wordlist**

![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-1E90FF?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-0A2540?style=for-the-badge&logo=linux&logoColor=white)
![Python](https://img.shields.io/badge/Python-1E90FF?style=for-the-badge&logo=python&logoColor=white)

</div>

> ⚠️ **Teste realizado exclusivamente em rede própria**, para fins de
> aprendizado em segurança ofensiva. Nenhum dispositivo de terceiros
> foi acessado ou afetado. Veja o [aviso legal](#️-aviso-legal) completo
> abaixo.

---

## 📑 Sumário

- [Objetivo](#-objetivo)
- [O que este projeto inclui](#-o-que-este-projeto-inclui)
- [Estrutura do repositório](#%EF%B8%8F-estrutura-do-repositório)
- [Ambiente de teste](#%EF%B8%8F-ambiente-de-teste)
- [Ferramentas utilizadas](#-ferramentas-utilizadas)
- [Metodologia](#%EF%B8%8F-metodologia)
- [Resultado](#-resultado)
- [Recomendações](#%EF%B8%8F-recomendações)
- [Aviso legal](#%EF%B8%8F-aviso-legal)
- [Autor](#-autor)

---

## 🎯 Objetivo

Avaliar a resistência da senha de uma rede Wi-Fi WPA2 própria a um
ataque de dicionário, utilizando uma ferramenta própria em Python para
geração de wordlist customizada, documentando todo o processo, do
reconhecimento à mitigação.

---

## 📦 O que este projeto inclui

- 🐍 Ferramenta própria em Python para geração de wordlists customizadas
- 🔍 Metodologia completa de auditoria WPA2 (reconhecimento → captura → quebra → mitigação)
- 📊 Evidências de cada etapa do processo
- 🛡️ Recomendações de mitigação baseadas no resultado obtido

---

## 🗂️ Estrutura do repositório

```
wpa2-audit-lab/
├── README.md
├── wordlist-generator/
│   ├── README.md
│   └── gerador.py
├── relatorio/
│   └── relatorio-completo.md
└── evidencias/
    ├── 01-setup-monitor-mode.txt
    ├── 02-reconhecimento.txt
    ├── 03-captura-direcionada.txt
    ├── 04-deauth.txt
    ├── 05-conversao-hcxpcapngtool.txt
    └── 06-hashcat.txt
```

---

## 🖥️ Ambiente de teste

| Item | Detalhe |
|---|---|
| Alvo | Rede Wi-Fi própria (rede doméstica) |
| Protocolo | WPA2-PSK (CCMP) |
| Sistema operacional | Linux (Fedora) |
| Interface de rede | Intel iwlwifi (modo monitor) |
| GPU para quebra | Intel UHD Graphics (OpenCL) |

---

## 🧰 Ferramentas utilizadas

| Ferramenta | Função no projeto |
|---|---|
| `airmon-ng` | Ativação do modo monitor na interface de rede |
| `airodump-ng` | Reconhecimento e captura do handshake WPA2 |
| `aireplay-ng` | Deautenticação, para forçar reconexão e captura do handshake |
| `aircrack-ng` | Suíte de apoio à validação da captura |
| `hcxpcapngtool` | Conversão do handshake para formato compatível com o Hashcat |
| `hashcat` | Teste de dicionário contra o handshake |
| Gerador de wordlist (Python) | Ferramenta própria para geração de senhas candidatas — [ver documentação](./wordlist-generator/) |

---

## 🗺️ Metodologia

### 1. Preparação do ambiente

A interface de rede (`wlo1`, chipset Intel iwlwifi) foi identificada e
colocada em modo monitor:

```bash
sudo airmon-ng start wlo1
```

Processos que poderiam interferir na captura (`NetworkManager`,
`wpa_supplicant`, `avahi-daemon`) foram finalizados:

```bash
sudo airmon-ng check kill
```

A interface em modo monitor foi confirmada com `iw dev`, resultando na
interface `wlo1mon` ativa.

### 2. Reconhecimento

Uma varredura geral identificou a rede-alvo e os dispositivos
conectados a ela:

```bash
sudo airodump-ng wlo1mon
```

| Parâmetro | Valor |
|---|---|
| ESSID | `wifi-teste` |
| Criptografia | WPA2 (CCMP/PSK) |
| Canal | 3 |
| BSSID | `XX:XX:XX:XX:XX:XX` *(ocultado)* |

### 3. Captura direcionada

A captura foi travada no canal e BSSID da rede-alvo, com o tráfego
salvo em arquivo `.cap`:

```bash
sudo airodump-ng -c 3 --bssid XX:XX:XX:XX:XX:XX -w ~/handshakes/ wlo1mon
```

### 4. Deautenticação e captura do handshake

Pacotes de deautenticação foram enviados com `aireplay-ng`, explorando
a ausência de autenticação nesse tipo de frame no protocolo 802.11. A
reconexão automática de um dispositivo-alvo permitiu a captura do
handshake WPA2:

```bash
sudo aireplay-ng --deauth 10 -a XX:XX:XX:XX:XX:XX -c XX:XX:XX:XX:XX:XX wlo1mon
```

✅ Handshake capturado com sucesso, confirmado pela marcação `EAPOL`
associada ao dispositivo-alvo no painel do `airodump-ng`.

### 5. Conversão do handshake

O arquivo `.cap` foi convertido para o formato `.hc22000`, compatível
com o Hashcat, utilizando `hcxpcapngtool`:

```bash
hcxpcapngtool -o 01.hc22000 ~/handshakes/-01.cap
```

| Métrica | Valor |
|---|---|
| Pacotes processados | 24.449 |
| Mensagens EAPOL capturadas | 15 |
| Pares EAPOL (total) | 7 |
| Pares EAPOL válidos (melhor par) | 1 |
| Pares escritos no arquivo `.hc22000` | 1 |

> A ferramenta identificou 1 par de handshake válido, suficiente para
> o teste no Hashcat. O arquivo de captura não continha cabeçalho
> *radiotap* nem *probe requests* não direcionados, o que é anotado
> aqui como ponto de melhoria para capturas futuras (uso do formato
> `pcapng`).

### 6. Teste de força

O handshake convertido foi testado contra a wordlist customizada,
gerada pela ferramenta própria em Python, utilizando ataque de
dicionário (modo `-a 0`) com o tipo de hash `22000`
(WPA-PBKDF2-PMKID+EAPOL):

```bash
hashcat -m 22000 -a 0 01.hc22000 ~/wordlist/list.txt
```

| Métrica | Valor |
|---|---|
| Status | `Cracked` |
| Senha recuperada | ✅ Sim *(omitida por segurança)* |
| Wordlist utilizada | 11.333 senhas (~94 KB) |
| Tempo total de execução | ~1 segundo |
| Velocidade | ~11.649 H/s |
| Keyspace testado | 100% (22.666/22.666) |

---

## 📊 Resultado

A senha foi recuperada em menos de 2 segundos, utilizando uma
wordlist pequena e direcionada. Isso indica que o padrão da senha
(combinação curta de números com um caractere especial fixo) era
previsível o suficiente para estar contido numa wordlist pequena,
sem necessidade de um ataque de força bruta completo contra todo o
espaço de combinações possíveis.

---

## 🛡️ Recomendações

- Uso de senhas longas (16+ caracteres), sem padrões reconhecíveis
  (datas, sequências numéricas), geradas preferencialmente por um
  gerenciador de senhas
- Desativação do WPS, caso esteja habilitado no roteador
- Verificação e atualização do firmware do dispositivo
- Migração para WPA3, quando o hardware do roteador suportar, já que
  o protocolo reduz a exposição do handshake
- Troca da senha da rede após qualquer teste desse tipo, já que o
  handshake capturado permanece válido para testes offline enquanto a
  senha não for alterada

---

## ⚖️ Aviso legal

Este projeto foi conduzido exclusivamente em ambiente de minha
propriedade, com o único objetivo de aprendizado em segurança
ofensiva. Nenhuma rede ou dispositivo de terceiros foi testado,
acessado ou afetado.

Testes de segurança em redes de terceiros sem autorização expressa
constituem crime, conforme a Lei nº 12.737/2012 (Lei Carolina
Dieckmann) e o Marco Civil da Internet (Lei nº 12.965/2014). Todo o
conteúdo deste repositório é apresentado para fins educacionais e de
divulgação responsável.

---

## 👤 Autor

**Apolônio Melo**
[GitHub](https://github.com/apolonio-web) · [LinkedIn](https://linkedin.com/in/apolonio-melo)
