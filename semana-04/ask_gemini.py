#!/usr/bin/env python3
"""
Simple script to send a question to the Gemini API and print the response.
Usage:
  python ask_gemini.py "Sua pergunta aqui"
or
  python ask_gemini.py        # e digite a pergunta quando solicitado
"""
import sys
from dotenv import load_dotenv

from gemini_client import GeminiClient

load_dotenv()


def main():
    # Always prompt the user interactively for the question
    try:
        prompt = input("Pergunta para Gemini: ").strip()
    except EOFError:
        prompt = ""

    if not prompt:
        print("Nenhuma pergunta fornecida. Encerrando.")
        sys.exit(1)

    try:
        client = GeminiClient.from_env()
        response = client.generate_text(prompt)
        print("\n--- Resposta Gemini ---\n")
        print(response)
    except Exception as exc:
        print("Erro ao chamar a API Gemini:", exc)
        sys.exit(2)


if __name__ == "__main__":
    main()
