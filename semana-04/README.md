# Semana 04 - Integração com API Gemini

Este diretório contém utilitários e exemplos para integrar com a API Gemini e comandos de análise de texto/dados.

**Principais arquivos**

- `.gitignore` - protege o arquivo `.env` e artefatos locais
- `.env.example` - modelo de variáveis de ambiente (copie para `.env` e preencha `GEMINI_API_KEY`)
- `requirements.txt` - dependências (`flask`, `python-dotenv`, `requests`, `pandas`, `numpy`, `matplotlib`, `colorama`)
- `gemini_client.py` - cliente simples para chamar a API Gemini (lê `GEMINI_API_KEY` de `.env`)
- `app.py` - pequena API Flask com endpoint `/generate`
- `ask_gemini.py` - script interativo que pergunta ao usuário e imprime a resposta da Gemini
- `chatbot_terminal.py` - chatbot interativo em terminal (histórico de sessão, cores, tokens estimados)
- `analyze_text.py` - analisa texto e gera JSON com `summary`, `sentiment`, `keywords`; aceita `--file` ou `--dir` (gera `<name>_analise.json`)
- `translate.py` - traduz para pt-BR; aceita `--text`, `--file` ou `--dir`; preserva termos técnicos via `--glossary` e salva arquivos com sufixo `_pt`
- `analyze_csv_report.py` - carrega CSV, gera estatísticas, cria gráficos (PNG) e pede à Gemini um relatório executivo em Markdown (gráficos referenciados no relatório)
- `run_report.py` - wrapper para executar `analyze_csv_report.py` lendo `report_config.json` e gravando logs
- `report_config.json` - configuração para execução diária (csv_path, output_path, focus, time, task_name)
- `register_task.ps1` - script PowerShell para registrar tarefa diária no Agendador do Windows

**Como começar**

1. Crie e ative um ambiente virtual:
```
python -m venv .venv
.venv\Scripts\activate  # Windows
```
2. Instale dependências:
```
pip install -r requirements.txt
```
3. Configure sua chave:
```
copy .env.example .env
# edite .env e coloque GEMINI_API_KEY
```

**Exemplos de uso rápido**

- Rodar servidor Flask:
```
python app.py
```

- Perguntar interativamente à Gemini:
```
python ask_gemini.py
```

- Chatbot terminal (cores e tokens):
```
python chatbot_terminal.py
```

- Analisar um arquivo de texto e salvar JSON:
```
python analyze_text.py --file exemplo.txt
```

- Processar pasta de textos (gera `nome_analise.json` por arquivo):
```
python analyze_text.py --dir textos/
```

- Traduzir pasta inteira preservando termos técnicos (glossário opcional):
```
python translate.py --dir textos/ --glossary glossary.txt
```

- Gerar relatório executivo a partir de CSV (gera `relatorio.md` e imagens):
```
python analyze_csv_report.py --csv ../semana-03/incidents_master_cleaned.csv --output relatorio.md --focus "Resumo executivo"
```

- Agendar geração diária (Windows): editar `report_config.json` e executar como Administrador:
```
cd semana-04
.\register_task.ps1
```

**Logs e saída**

- Execuções agendadas escrevem logs em `semana-04/run_report.log`.
- Relatórios e gráficos são salvos no local especificado em `report_config.json`.

Se quiser que eu adicione mais exemplos de visualização, suporte a envio por e-mail, ou integração com CI/CD para publicar os relatórios, diga qual opção prefere.
