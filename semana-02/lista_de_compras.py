import os

ARQUIVO = "lista_compras.txt"

# Carregar lista do arquivo se existir
lista_compras = []
if os.path.exists(ARQUIVO):
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            lista_compras = [linha.strip()
                             for linha in f.readlines() if linha.strip()]
        print("✓ Lista carregada do arquivo!")
    except Exception as e:
        print(f"⚠ Erro ao carregar arquivo: {e}")

while True:
    print("\n=== LISTA DE COMPRAS ===")
    print("1. Adicionar item")
    print("2. Ver itens")
    print("3. Remover item")
    print("4. Sair")
    print("=" * 25)

    opcao = input("Escolha uma opção (1-4): ").strip()

    if opcao == "1":
        item = input("Digite o item a adicionar: ").strip()
        if item:
            lista_compras.append(item)
            print(f"✓ '{item}' adicionado à lista!")
        else:
            print("⚠ Item vazio não pode ser adicionado!")

    elif opcao == "2":
        if lista_compras:
            print("\n📋 Itens na lista:")
            for i, item in enumerate(lista_compras, 1):
                print(f"  {i}. {item}")
        else:
            print("⚠ A lista está vazia!")

    elif opcao == "3":
        if lista_compras:
            print("\n📋 Itens na lista:")
            for i, item in enumerate(lista_compras, 1):
                print(f"  {i}. {item}")
            try:
                indice = int(input("Digite o número do item a remover: ")) - 1
                if 0 <= indice < len(lista_compras):
                    item_removido = lista_compras.pop(indice)
                    print(f"✓ '{item_removido}' removido da lista!")
                else:
                    print("⚠ Índice inválido!")
            except ValueError:
                print("⚠ Digite um número válido!")
        else:
            print("⚠ A lista está vazia!")

    elif opcao == "4":
        # Salvar lista em arquivo antes de sair
        try:
            with open(ARQUIVO, "w", encoding="utf-8") as f:
                for item in lista_compras:
                    f.write(item + "\n")
            print("✓ Lista salva em 'lista_compras.txt'")
        except Exception as e:
            print(f"⚠ Erro ao salvar arquivo: {e}")

        print("👋 Até logo!")
        break

    else:
        print("⚠ Opção inválida! Digite 1, 2, 3 ou 4.")
