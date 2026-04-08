# Script para converter Celsius para Fahrenheit e vice-versa

print("=== Conversor de Temperatura ===\n")

try:
    # Menu de escolha
    print("Escolha a conversão:")
    print("1 - Celsius para Fahrenheit")
    print("2 - Fahrenheit para Celsius\n")

    opcao = input("Digite 1 ou 2: ").strip()

    if opcao == "1":
        # Conversão Celsius para Fahrenheit
        celsius = float(input("Digite a temperatura em Celsius: "))
        fahrenheit = (celsius * 9/5) + 32
        print(f"\n{celsius:.2f}°C = {fahrenheit:.2f}°F\n")

    elif opcao == "2":
        # Conversão Fahrenheit para Celsius
        fahrenheit = float(input("Digite a temperatura em Fahrenheit: "))
        celsius = (fahrenheit - 32) * 5/9
        print(f"\n{fahrenheit:.2f}°F = {celsius:.2f}°C\n")

    else:
        print("Opção inválida! Digite 1 ou 2.")

except ValueError:
    print("Erro! Por favor, digite um número válido.")
