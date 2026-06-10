#!/usr/bin/env python3
"""
Load a CSV with pandas, analyze it, and ask Gemini to generate an executive report in Markdown.

Usage:
  python analyze_csv_report.py --csv data.csv --output report.md [--focus "business question"]

The script prints the output path and also writes the Markdown report.
"""
from gemini_client import GeminiClient
import matplotlib.pyplot as plt
import argparse
import sys
import os
from textwrap import shorten
from dotenv import load_dotenv
import pandas as pd
import matplotlib
matplotlib.use('Agg')


load_dotenv()

PROMPT_TEMPLATE = (
    "Você é um analista executivo de dados especializado em cibersegurança.\n"
    "Abaixo segue um resumo dos metadados e estatísticas extraídas do arquivo CSV.\n"
    "Com base nesses achados, gere um relatório executivo em Markdown contendo pelo menos: um título, um parágrafo de resumo (máx. 3-4 frases), principais descobertas quantitativas, recomendações práticas, implication for stakeholders, e limitações dos dados. Seja conciso e objetivo.\n\n"
    "Resumo dos dados:\n{data_summary}\n\n"
    "Instruções adicionais: {focus}\n\n"
    "Resposta em Markdown:"
)


def df_summary(df: pd.DataFrame, sample_rows: int = 5, max_chars: int = 2000) -> str:
    parts = []
    parts.append(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")

    # dtypes and missing
    missing = df.isnull().sum()
    dtypes = df.dtypes.astype(str)
    parts.append("\nColunas (tipo | missing):")
    for col in df.columns:
        parts.append(f"- {col}: {dtypes[col]} | missing={int(missing[col])}")

    # numeric summary
    num = df.select_dtypes(include=['number'])
    if not num.empty:
        parts.append(
            "\nResumo numérico (count, mean, std, min, 25%, 50%, 75%, max):")
        desc = num.describe().T
        for col, row in desc.iterrows():
            vals = ", ".join([f"{k}={round(v, 3)}" for k, v in row.items()])
            parts.append(f"- {col}: {vals}")

    # top values for object cols
    obj = df.select_dtypes(include=['object', 'category'])
    if not obj.empty:
        parts.append("\nTop valores por coluna (até 5):")
        for col in obj.columns:
            try:
                top = df[col].value_counts(dropna=True).head(5)
                tops = "; ".join([f"{i}({c})" for i, c in zip(
                    top.index.astype(str), top.values)])
                parts.append(f"- {col}: {tops}")
            except Exception:
                continue

    # sample rows
    parts.append("\nAmostra (primeiras linhas):")
    try:
        sample = df.head(sample_rows).to_csv(index=False)
        parts.append(shorten(sample, width=800, placeholder='...'))
    except Exception:
        parts.append("(não foi possível gerar amostra)")

    text = "\n".join(parts)
    if len(text) > max_chars:
        return shorten(text, width=max_chars, placeholder='...')
    return text


def build_prompt(data_summary: str, focus: str) -> str:
    if not focus:
        focus_text = "Sem instruções adicionais."
    else:
        focus_text = f"Foco pedido: {focus}"
    return PROMPT_TEMPLATE.format(data_summary=data_summary, focus=focus_text)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze CSV and generate executive Markdown report via Gemini')
    parser.add_argument('--csv', '-c', required=True,
                        help='Path to input CSV file')
    parser.add_argument('--output', '-o', default='report.md',
                        help='Output Markdown file')
    parser.add_argument('--focus', '-f', default='',
                        help='Optional focus / business question for the report')
    parser.add_argument('--sample-rows', type=int, default=5,
                        help='Number of sample rows to include in summary')
    parser.add_argument('--max-tokens', type=int, default=800,
                        help='Max tokens for the AI response')
    args = parser.parse_args()

    csv_path = args.csv
    out_path = args.output

    if not os.path.exists(csv_path):
        print(f"Arquivo CSV não encontrado: {csv_path}")
        sys.exit(1)

    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:
        print(f"Falha ao ler CSV: {exc}")
        sys.exit(1)

    summary = df_summary(df, sample_rows=args.sample_rows, max_chars=4000)
    # create charts and add references to the summary
    out_parent = Path(out_path).resolve().parent
    images_dir = out_parent / (Path(out_path).stem + "_images")
    images_dir.mkdir(parents=True, exist_ok=True)

    def save_charts(df: pd.DataFrame, images_dir: Path):
        charts = []
        # detect datetime-like columns
        datetime_cols = []
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    parsed = pd.to_datetime(df[col], errors='coerce')
                    if parsed.notna().sum() > 0:
                        datetime_cols.append(col)
                        df['_parsed_' + col] = parsed
                except Exception:
                    continue

        # plot time-series for first datetime col
        if datetime_cols:
            col = datetime_cols[0]
            series = df.dropna(
                subset=['_parsed_' + col]).set_index('_parsed_' + col)
            if not series.empty:
                counts = series.resample('M').size()
                if counts.sum() > 0:
                    fig, ax = plt.subplots()
                    counts.plot(ax=ax)
                    ax.set_title(f'Contagem por mês: {col}')
                    ax.set_ylabel('Contagem')
                    fname = images_dir / f"timeseries_{col}.png"
                    fig.tight_layout()
                    fig.savefig(fname)
                    plt.close(fig)
                    charts.append((fname, f'Contagem por mês para {col}'))

        # numeric histograms (top 3 by variance)
        num = df.select_dtypes(include=['number'])
        if not num.empty:
            variances = num.var().sort_values(ascending=False)
            for col in variances.index[:3]:
                try:
                    fig, ax = plt.subplots()
                    num[col].dropna().hist(ax=ax, bins=30)
                    ax.set_title(f'Distribuição: {col}')
                    fname = images_dir / f"hist_{col}.png"
                    fig.tight_layout()
                    fig.savefig(fname)
                    plt.close(fig)
                    charts.append((fname, f'Distribuição da coluna {col}'))
                except Exception:
                    continue

        # categorical bar charts (top 3 categorical columns with <=50 unique)
        obj = df.select_dtypes(include=['object', 'category'])
        cat_scores = []
        for col in obj.columns:
            try:
                unique = df[col].nunique(dropna=True)
                if 1 < unique <= 50:
                    cat_scores.append((unique, col))
            except Exception:
                continue
        cat_scores.sort()
        for _, col in cat_scores[:3]:
            try:
                top = df[col].value_counts(dropna=True).head(10)
                fig, ax = plt.subplots()
                top.plot(kind='bar', ax=ax)
                ax.set_title(f'Top valores: {col}')
                fname = images_dir / f"bar_{col}.png"
                fig.tight_layout()
                fig.savefig(fname)
                plt.close(fig)
                charts.append((fname, f'Principais valores em {col}'))
            except Exception:
                continue

        return charts

    charts = save_charts(df, images_dir)
    # append charts info to summary for AI context
    if charts:
        charts_list_text = "\n\nGráficos gerados (arquivos):\n"
        for p, caption in charts:
            # relative path from report location
            rel = os.path.relpath(p, start=out_parent)
            charts_list_text += f"- {rel}: {caption}\n"
        summary = summary + charts_list_text

    prompt = build_prompt(summary, args.focus)

    try:
        client = GeminiClient.from_env()
    except Exception as exc:
        print(f"Falha ao inicializar Gemini client: {exc}")
        sys.exit(1)

    try:
        md = client.generate_text(
            prompt, temperature=0.2, max_output_tokens=args.max_tokens)
    except Exception as exc:
        print(f"Chamada à API falhou: {exc}")
        sys.exit(1)

    # Append image references to the Markdown report so images are visible
    if charts:
        md += "\n\n---\n### Gráficos gerados\n"
        for p, caption in charts:
            rel = os.path.relpath(p, start=out_parent).replace('\\\\', '/')
            md += f"\n#### {caption}\n![]({rel})\n"

    # Save markdown
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"Relatório gerado: {out_path}")
    except Exception as exc:
        print(f"Falha ao salvar relatório: {exc}")
        sys.exit(1)


if __name__ == '__main__':
    main()
