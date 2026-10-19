import itertools

def gerar_wordlist(nome_arquivo="wordlist_custom.txt", tamanho_min=4, tamanho_max=8):
    # Caracteres utilizados: números de 0 a 9 e o símbolo @
    caracteres = "0123456789@"

    print(f"[*] Iniciando a geração da wordlist...")
    print(f"[*] Caracteres utilizados: {caracteres}")
    print(f"[*] Tamanho das senhas: de {tamanho_min} a {tamanho_max} caracteres.")

    total_senhas = 0

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for tamanho in range(tamanho_min, tamanho_max + 1):
            print(f"[+] Gerando combinações de tamanho {tamanho}...")
            for combinacao in itertools.product(caracteres, repeat=tamanho):
                senha = "".join(combinacao)

                # Garante que a senha contém pelo menos um '@'
                if "@" not in senha:
                    continue

                f.write(senha + "\n")
                total_senhas += 1

    print(f"\n[!] Sucesso! Wordlist gerada com {total_senhas} senhas.")
    print(f"[!] Arquivo salvo como: {nome_arquivo}")


if __name__ == "__main__":
    # Cuidado: tamanhos muito grandes (ex: tamanho_max=12) geram arquivos de vários GB
    gerar_wordlist(nome_arquivo="passwords.txt", tamanho_min=8, tamanho_max=9)
