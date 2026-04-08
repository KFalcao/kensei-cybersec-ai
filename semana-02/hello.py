# Script que pede o nome e saudação em maiúsculo

while True:
    nome = input("Digite seu nome: ")
    if len(nome) >= 3:
        break
    print("Nome deve ter pelo menos 3 letras. Tente novamente!")

print(f"Olá, {nome.upper()}!")
