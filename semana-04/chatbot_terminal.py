#!/usr/bin/env python3
"""
Terminal chatbot using Gemini API. Maintains conversation history and uses a cybersecurity system prompt.

Usage:
  python chatbot_terminal.py
Commands:
  /exit or /quit  - exit the chat
"""
import sys
from dotenv import load_dotenv
from colorama import init as colorama_init, Fore, Style

from gemini_client import GeminiClient

load_dotenv()
colorama_init(autoreset=True)

SYSTEM_PROMPT = (
    "Você é um assistente especializado em cibersegurança. Forneça respostas concisas, técnicas quando necessárias, "
    "e inclua recomendações práticas e medidas preventivas. Evite dar instruções que violem leis ou que facilitem atividades maliciosas."
)

PROMPT_SEPARATOR = "\n"


def build_prompt(system_prompt, history, user_input):
    parts = [f"System: {system_prompt}", "Conversation:"]
    for i, (u, a) in enumerate(history, start=1):
        parts.append(f"User: {u}")
        parts.append(f"Assistant: {a}")
    parts.append(f"User: {user_input}")
    parts.append("Assistant:")
    return PROMPT_SEPARATOR.join(parts)


def estimate_tokens(text: str) -> int:
    """Rough token estimate: use characters/4 heuristic."""
    if not text:
        return 0
    return max(1, int(len(text) / 4))


def main():
    try:
        client = GeminiClient.from_env()
    except Exception as exc:
        print("Erro ao inicializar GeminiClient:", exc)
        sys.exit(1)

    print("Chatbot Gemini (digite /exit para sair)")
    history = []  # list of (user, assistant)
    cumulative_tokens = 0

    while True:
        try:
            user = input('\nVocê: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nSaindo...')
            break

        if not user:
            continue
        if user.lower() in ('/exit', '/quit'):
            print('Saindo...')
            break

        # show user input in bright white
        print(Style.BRIGHT + Fore.WHITE + f"\nVocê: {user}")

        prompt = build_prompt(SYSTEM_PROMPT, history, user)
        prompt_tokens = estimate_tokens(prompt)
        try:
            reply = client.generate_text(
                prompt, temperature=0.2, max_output_tokens=400)
        except Exception as exc:
            print(Fore.RED + 'Erro na chamada à API Gemini:' + str(exc))
            continue

        reply_tokens = estimate_tokens(reply)
        exchange_tokens = prompt_tokens + reply_tokens
        cumulative_tokens += exchange_tokens

        # print assistant in green, show token usage
        print(Fore.GREEN + Style.BRIGHT + "\nAssistente:")
        print(Fore.GREEN + reply)
        print(
            Style.DIM + f"\nTokens estimados (prompt+reply): {exchange_tokens} | Total sessão (estimado): {cumulative_tokens}")

        history.append((user, reply))


if __name__ == '__main__':
    main()
