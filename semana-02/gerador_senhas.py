import random
import string
from datetime import datetime


def criar_caracteres(maiusculas, numeros, simbolos):
    """
    Retorna a string de caracteres disponíveis para a senha.
    """
    caracteres = string.ascii_lowercase
    if maiusculas:
        caracteres += string.ascii_uppercase
    if numeros:
        caracteres += string.digits
    if simbolos:
        caracteres += string.punctuation
    return caracteres


def gerar_uma_senha(tamanho, caracteres):
    """
    Gera uma única senha aleatória.
    """
    return ''.join(random.choice(caracteres) for _ in range(tamanho))


def gerar_lote_senhas():
    """
    Gera um lote de 5 senhas e salva em arquivo com data.
    """
    print("=== GERADOR DE SENHAS (LOTE) ===\n")

    # Solicita o tamanho da senha
    while True:
        try:
            tamanho = int(input("Qual o tamanho da senha? (mínimo 4): "))
            if tamanho < 4:
                print("Por favor, escolha um tamanho mínimo de 4 caracteres.")
                continue
            break
        except ValueError:
            print("Por favor, digite um número válido.")

    # Solicita preferências adicionais
    maiusculas = input("\nDeseja incluir MAIÚSCULAS? (s/n): ").lower() == 's'
    numeros = input("Deseja incluir NÚMEROS? (s/n): ").lower() == 's'
    simbolos = input("Deseja incluir SÍMBOLOS? (s/n): ").lower() == 's'

    # Cria a lista de caracteres
    caracteres = criar_caracteres(maiusculas, numeros, simbolos)

    # Gera 5 senhas
    senhas = [gerar_uma_senha(tamanho, caracteres) for _ in range(5)]

    # Exibe na tela
    print(f"\n{'='*40}")
    print("5 SENHAS GERADAS:")
    print(f"{'='*40}")
    for i, senha in enumerate(senhas, 1):
        print(f"{i}. {senha}")
    print(f"{'='*40}\n")

    # Salva em arquivo com data
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open("senhas.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"\n{'='*50}\n")
        arquivo.write(f"Data/Hora: {data_hora}\n")
        arquivo.write(
            f"Tamanho: {tamanho} | Maiúsculas: {'Sim' if maiusculas else 'Não'} | ")
        arquivo.write(
            f"Números: {'Sim' if numeros else 'Não'} | Símbolos: {'Sim' if simbolos else 'Não'}\n")
        arquivo.write(f"{'='*50}\n")
        for i, senha in enumerate(senhas, 1):
            arquivo.write(f"{i}. {senha}\n")

    print("✅ Senhas salvas em 'senhas.txt'!\n")

    # Opção de gerar outro lote
    outra = input("Gerar outro lote de senhas? (s/n): ").lower()
    if outra == 's':
        print("\n")
        gerar_lote_senhas()


if __name__ == "__main__":
    gerar_lote_senhas()
