import threading
import time


def input_com_timeout(mensagem, timeout=10):
    """Função para ler input com timeout"""
    resultado = [None]

    def ler_input():
        resultado[0] = input(mensagem)

    thread = threading.Thread(target=ler_input, daemon=True)
    thread.start()
    thread.join(timeout=timeout)

    if resultado[0] is None:
        print("\n⏱ Tempo esgotado!")
        return None
    return resultado[0]


def quiz_cybersecurity():
    """Quiz de 5 perguntas sobre cibersegurança"""

    perguntas = [
        {
            "pergunta": "1. O que é Phishing?",
            "opcoes": ["a) Um ataque de negação de serviço", "b) Tentativa de enganar usuários para roubar dados", "c) Um tipo de criptografia"],
            "resposta_correta": "b"
        },
        {
            "pergunta": "2. Qual é a função de um firewall?",
            "opcoes": ["a) Criptografar dados em trânsito", "b) Monitorar e filtrar tráfego de rede", "c) Detectar malware no computador"],
            "resposta_correta": "b"
        },
        {
            "pergunta": "3. O que significa 2FA (Autenticação de Dois Fatores)?",
            "opcoes": ["a) Duas senhas diferentes", "b) Verificação de dois mecanismos de identidade", "c) Dois computadores na mesma rede"],
            "resposta_correta": "b"
        },
        {
            "pergunta": "4. Qual é o maior risco de usar senhas fracas?",
            "opcoes": ["a) Consumir mais banda de internet", "b) Facilitar o acesso não autorizado de hackers", "c) Diminuir a velocidade do computador"],
            "resposta_correta": "b"
        },
        {
            "pergunta": "5. O que é um Ransomware?",
            "opcoes": ["a) Um software que organiza arquivos", "b) Malware que criptografa dados e exige resgate", "c) Um antivírus poderoso"],
            "resposta_correta": "b"
        }
    ]

    pontuacao = 0

    print("=" * 50)
    print("QUIZ DE CIBERSEGURANÇA - 5 PERGUNTAS")
    print("=" * 50)
    print()

    for i, item in enumerate(perguntas):
        print(item["pergunta"])
        for opcao in item["opcoes"]:
            print(f"  {opcao}")

        print("⏱ Você tem 10 segundos para responder!")
        resposta = input_com_timeout("Sua resposta (a/b/c): ", timeout=10)

        if resposta is None or resposta.lower().strip() not in ['a', 'b', 'c']:
            print("✗ Errado! Resposta inválida ou tempo esgotado!\n")
        elif resposta.lower().strip() == item["resposta_correta"]:
            print("✓ Correto!\n")
            pontuacao += 1
        else:
            print(
                f"✗ Errado! A resposta correta é: {item['resposta_correta']}\n")

    print("=" * 50)
    print(f"RESULTADO FINAL: {pontuacao}/5")
    print("=" * 50)

    if pontuacao >= 3:
        print("✓ PARABÉNS! Você PASSOU no quiz! 🎉")
    else:
        print("✗ Infelizmente você não passou. Estude mais sobre cibersegurança!")

    print()


if __name__ == "__main__":
    quiz_cybersecurity()
