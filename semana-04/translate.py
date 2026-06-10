#!/usr/bin/env python3
"""
Translate text or file to PT-BR using Gemini. Detects source language and returns JSON:
{ "detected_language": "en", "translation": "..." }

Usage:
  python translate.py --text "Some text to translate"
  python translate.py --file path/to/file.txt
  python translate.py --file path/to/file.txt --output out.json
"""
import argparse
import sys
import json
import re
from pathlib import Path
from dotenv import load_dotenv

from gemini_client import GeminiClient

load_dotenv()

SYSTEM_INSTRUCTION = (
    "Você é um tradutor profissional. Primeiro detecte o idioma de entrada, depois traduza o texto para Português do Brasil (pt-BR). "
    "Preserve o tom, formatação, nomes próprios e termos técnicos. Responda estritamente com JSON contendo as chaves: 'detected_language' (código ISO, ex: 'en'), 'translation' (string). "
    "Não adicione texto explicativo, exemplos ou metadados extras. Se não for possível, retorne {\"error\": \"mensagem\"}."
)


def extract_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        pass
    m = re.search(r"(\{.*\})", text, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    return None


def build_prompt(system_instr: str, content: str) -> str:
    return f"{system_instr}\n\nTexto a ser traduzido:\n{content}\n\nJSON:"


def main():
    parser = argparse.ArgumentParser(
        description='Translate text/file to PT-BR using Gemini')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text', '-t', help='Text to translate')
    group.add_argument('--file', '-f', help='Path to a text file to translate')
    group.add_argument(
        '--dir', '-d', help='Path to a directory containing .txt files to translate')
    parser.add_argument(
        '--output', '-o', help='Output file to write JSON (optional)')
    parser.add_argument(
        '--glossary', help='Path to a glossary file (one term per line) of technical terms NOT to translate')
    args = parser.parse_args()

    # load glossary terms (one per line) or use sensible defaults
    glossary_terms = []
    if getattr(args, 'glossary', None):
        gpath = Path(args.glossary)
        if gpath.exists():
            try:
                glossary_terms = [t.strip() for t in gpath.read_text(
                    encoding='utf-8').splitlines() if t.strip()]
            except Exception:
                glossary_terms = []
    if not glossary_terms:
        glossary_terms = [
            'phishing', 'malware', 'ransomware', 'DDoS', 'XSS', 'SQL injection',
            'APT', 'C2', 'payload'
        ]
    glossary_txt = ", ".join(glossary_terms)

    def append_glossary(instr: str) -> str:
        return instr + f"\n\nNão traduza ou altere os termos técnicos seguintes (preserve a grafia): {glossary_txt}."

    try:
        client = GeminiClient.from_env()
    except Exception as exc:
        print(json.dumps(
            {"error": f"Failed to init Gemini client: {exc}"}, ensure_ascii=False))
        sys.exit(1)

    if args.dir:
        d = Path(args.dir)
        if not d.exists() or not d.is_dir():
            print(json.dumps(
                {"error": f"Directory not found: {args.dir}"}, ensure_ascii=False))
            sys.exit(1)

        txt_files = sorted(
            [p for p in d.iterdir() if p.is_file() and p.suffix.lower() == '.txt'])
        if not txt_files:
            print(json.dumps(
                {"error": "No .txt files found in directory"}, ensure_ascii=False))
            sys.exit(0)

        for p in txt_files:
            try:
                content = p.read_text(encoding='utf-8')
            except Exception as exc:
                print(json.dumps(
                    {"file": str(p), "error": f"Failed to read file: {exc}"}, ensure_ascii=False))
                continue

            # ask model to return only the translated text and preserve glossary terms
            batch_instr = append_glossary(SYSTEM_INSTRUCTION)
            batch_instr = batch_instr + \
                "\nResponda somente com o texto traduzido em Português do Brasil (pt-BR), sem JSON ou comentários."
            prompt = build_prompt(batch_instr, content)
            try:
                resp = client.generate_text(
                    prompt, temperature=0.0, max_output_tokens=1200)
            except Exception as exc:
                print(json.dumps(
                    {"file": str(p), "error": f"API call failed: {exc}"}, ensure_ascii=False))
                continue

            # save translated text to file with _pt suffix
            out_path = p.with_name(p.stem + '_pt' + p.suffix)
            try:
                out_path.write_text(resp, encoding='utf-8')
                print(f"Translated and saved: {out_path}")
            except Exception as exc:
                print(json.dumps({"file": str(
                    p), "error": f"Failed to write output file: {exc}"}, ensure_ascii=False))
        sys.exit(0)

    if args.file:
        p = Path(args.file)
        if not p.exists():
            print(json.dumps(
                {"error": f"File not found: {args.file}"}, ensure_ascii=False))
            sys.exit(1)
        try:
            content = p.read_text(encoding='utf-8')
        except Exception as exc:
            print(json.dumps(
                {"error": f"Failed to read file: {exc}"}, ensure_ascii=False))
            sys.exit(1)
    else:
        content = args.text.strip()

    if not content:
        print(json.dumps({"error": "Empty input"}, ensure_ascii=False))
        sys.exit(1)
    # build prompt using glossary-aware instruction
    instr = append_glossary(SYSTEM_INSTRUCTION)
    prompt = build_prompt(instr, content)
    try:
        resp = client.generate_text(
            prompt, temperature=0.0, max_output_tokens=800)
    except Exception as exc:
        print(json.dumps(
            {"error": f"API call failed: {exc}"}, ensure_ascii=False))
        sys.exit(1)

    parsed = extract_json(resp)
    if parsed is None:
        # return raw for inspection
        out = {"error": "Invalid JSON in model response", "raw": resp}
    else:
        out = parsed

    out_str = json.dumps(out, ensure_ascii=False, indent=2)
    if args.output:
        try:
            Path(args.output).write_text(out_str, encoding='utf-8')
            print(f"Wrote output to {args.output}")
        except Exception as exc:
            print(json.dumps(
                {"error": f"Failed to write output file: {exc}"}, ensure_ascii=False))
            sys.exit(1)
    else:
        print(out_str)


if __name__ == '__main__':
    main()
