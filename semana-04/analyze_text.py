#!/usr/bin/env python3
"""
Analyze text using Gemini: return JSON with
- summary (3 sentences)
- sentiment (positive|neutral|negative)
- keywords (5 words)

Usage:
  python analyze_text.py "Seu texto aqui"
or
  python analyze_text.py    # lê do stdin
"""
import sys
import json
import re
import os
from pathlib import Path
import argparse
from dotenv import load_dotenv

from gemini_client import GeminiClient

load_dotenv()

parser = argparse.ArgumentParser(
    description='Analyze text(s) and save JSON analysis')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    '--file', '-f', help='Path to a single .txt file to analyze')
group.add_argument(
     '--dir', '-d', help='Path to a directory containing .txt files to process')
 parser.add_argument(
      '--output-dir', '-o', help='Directory to save analysis JSON files (defaults to each file\'s folder)')
  args = parser.parse_args()

   try:
        client = GeminiClient.from_env()
    except Exception as exc:
        print(json.dumps(
            {"error": f"Falha ao inicializar cliente: {exc}"}, ensure_ascii=False))
        sys.exit(2)

    def analyze_and_save(text: str, src_path: Path, out_dir: Path | None):
        prompt = build_prompt(INSTRUCTION, text)
        try:
            resp = client.generate_text(
                prompt, temperature=0.0, max_output_tokens=400)
        except Exception as exc:
            print(json.dumps({"file": str(
                src_path), "error": f"Chamada à API falhou: {exc}"}, ensure_ascii=False))
            return

        parsed = extract_json(resp)
        if parsed is None:
            out = {"error": "Resposta não está em JSON válido", "raw": resp}
        else:
            out = parsed

        # ensure required keys when possible
        if isinstance(out, dict) and all(k in out for k in ("summary", "sentiment", "keywords")):
            pass
        # write output
        if out_dir:
            out_path = out_dir / (src_path.stem + "_analise.json")
        else:
            out_path = src_path.with_name(src_path.stem + "_analise.json")
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
            print(f"Salvo: {out_path}")
        except Exception as exc:
            print(json.dumps(
                {"file": str(src_path), "error": f"Falha ao salvar: {exc}"}, ensure_ascii=False))

    if args.file:
        p = Path(args.file)
        if not p.exists() or not p.is_file():
            print(json.dumps(
                {"error": f"Arquivo não encontrado: {args.file}"}, ensure_ascii=False))
            sys.exit(1)
        try:
            text = p.read_text(encoding='utf-8')
        except Exception as exc:
            print(json.dumps(
                {"error": f"Falha ao ler arquivo: {exc}"}, ensure_ascii=False))
            sys.exit(1)
        out_dir = Path(args.output_dir) if args.output_dir else None
        analyze_and_save(text, p, out_dir)
    else:
        d = Path(args.dir)
        if not d.exists() or not d.is_dir():
            print(json.dumps(
                {"error": f"Diretório não encontrado: {args.dir}"}, ensure_ascii=False))
            sys.exit(1)
        out_dir = Path(args.output_dir) if args.output_dir else None
        if out_dir and not out_dir.exists():
            try:
                out_dir.mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                print(json.dumps(
                    {"error": f"Falha ao criar output-dir: {exc}"}, ensure_ascii=False))
                sys.exit(1)

        txt_files = sorted(
            [p for p in d.iterdir() if p.is_file() and p.suffix.lower() == '.txt'])
        if not txt_files:
            print(json.dumps(
                {"error": "Nenhum arquivo .txt encontrado no diretório"}, ensure_ascii=False))
            sys.exit(0)

        for p in txt_files:
            try:
                text = p.read_text(encoding='utf-8')
            except Exception as exc:
                print(json.dumps(
                    {"file": str(p), "error": f"Falha ao ler arquivo: {exc}"}, ensure_ascii=False))
                continue
            analyze_and_save(text, p, out_dir)
        text = sys.stdin.read().strip()

    if not text:
        print(json.dumps(
            {"error": "Nenhum texto fornecido"}, ensure_ascii=False))
        sys.exit(1)

    try:
        client = GeminiClient.from_env()
    except Exception as exc:
        print(json.dumps(
            {"error": f"Falha ao inicializar cliente: {exc}"}, ensure_ascii=False))
        sys.exit(2)

    prompt = build_prompt(INSTRUCTION, text)
    try:
        resp = client.generate_text(
            prompt, temperature=0.0, max_output_tokens=400)
    except Exception as exc:
        print(json.dumps(
            {"error": f"Chamada à API falhou: {exc}"}, ensure_ascii=False))
        sys.exit(3)

    parsed = extract_json(resp)
    if parsed is None:
        # retorna raw em key 'raw' para inspeção
        print(json.dumps(
            {"error": "Resposta não está em JSON válido", "raw": resp}, ensure_ascii=False))
        sys.exit(4)

    # valida formato mínimo
    if not all(k in parsed for k in ("summary", "sentiment", "keywords")):
        print(json.dumps(
            {"error": "JSON recebido não contém todas as chaves requeridas", "data": parsed}, ensure_ascii=False))
        sys.exit(5)

    print(json.dumps(parsed, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
