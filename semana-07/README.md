# Semana 07 — Apps Interativos e Prototipagem

Este diretório reúne aplicações interativas em Python, muitos projetos com Streamlit e experimentos com IA e segurança.

## 🚀 O que está aqui

- `app.py` / `calculadora_imc.py` — calculadora de IMC com visualização e interpretação.
- `dashboard.py` — painel de análise de ataques cibernéticos com filtros, gráficos e mapa.
- `chatbot_openai.py` — chatbot conversacional usando OpenAI.
- `pdf_summarizer.py` — uploader de PDF, extração de texto e resumo/Q&A com OpenAI.
- `soc_agent_ui.py` — interface para investigações SOC com webhook n8n.
- `language_tutor.py` — tutor de idiomas com exercícios e planos de estudo.

---

## 📌 Descrições rápidas

### `app.py` / `calculadora_imc.py`
Calculadora de Índice de Massa Corporal. O app recebe peso e altura, exibe o resultado, mostra a classificação e conta com visualizações para facilitar a interpretação.

### `dashboard.py`
Painel de análise de incidentes cibernéticos. Permite:
- carregar dados por upload;
- filtrar por ano, país e tipo de ataque;
- ver KPIs, tabelas e gráficos;
- exibir mapa mundi com intensidade de ataques.

> Dica: instale `pycountry` para garantir o mapeamento correto de nomes de países para código ISO3.

### `chatbot_openai.py`
Chatbot interativo com histórico de conversa. O usuário pode inserir a chave `OPENAI_API_KEY` e interagir com a interface de bolhas de mensagem.

### `pdf_summarizer.py`
Ferramenta para resumir PDFs. Faz upload de arquivos, extrai texto com `PyPDF2`, usa OpenAI para gerar resumo e perguntas/respostas, e grava histórico local.

### `soc_agent_ui.py`
Interface para executar consultas SOC usando um webhook do n8n. Salva histórico e permite exportar respostas em PDF ou JSON.

### `language_tutor.py`
Tutor básico de idiomas com: planos de estudo, flashcards, exercícios e geração de conteúdo quando a chave OpenAI está disponível.

---

## ⚙️ Como rodar

1. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
```

No macOS/Linux:

```bash
source .venv/bin/activate
```

2. Instale as dependências necessárias:

```bash
pip install -r ../requirements.txt
```

3. Execute o app desejado:

```bash
streamlit run dashboard.py
streamlit run chatbot_openai.py
streamlit run pdf_summarizer.py
streamlit run soc_agent_ui.py
streamlit run language_tutor.py
```

---

## 🧩 Dependências sugeridas

Se precisar instalar apenas os pacotes usados nesta pasta:

```bash
pip install streamlit pandas plotly altair openai PyPDF2 fpdf requests pycountry
```

---

## 📁 Arquivos de histórico e dados

- `pdf_history.json` — histórico de PDFs processados.
- `history_pdfs/` — PDFs enviados pelo usuário.
- `soc_history.json` — histórico de consultas SOC.

> O `dashboard.py` tenta localizar `cyber_attacks.csv` na raiz ou em `data/`; se não encontrar, use o uploader integrado.

---

## 💡 Recomendações

- Use `semana-07/dashboard.py` para explorar visualmente padrões de ataques.
- Use `chatbot_openai.py` e `pdf_summarizer.py` com `OPENAI_API_KEY` para testar funcionalidades de IA.
- Configure a URL do webhook do n8n para utilizar `soc_agent_ui.py`.

---

## ✅ Próximos passos

- Criar `requirements.txt` específico para `semana-07`.
- Incluir exemplos de dados para o dashboard.
- Adicionar instruções de configuração de webhook e de chaves de API.
