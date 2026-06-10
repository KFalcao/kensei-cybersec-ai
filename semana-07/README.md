# Semana 07 — Resumo dos Projetos

Este diretório contém vários protótipos e apps em Streamlit desenvolvidos durante a semana 07. Abaixo há uma descrição rápida de cada arquivo, instruções de execução e notas sobre dependências e arquivos de histórico.

## Arquivos e descrições

- `app.py` / `calculadora_imc.py`
  - Calculadora de IMC (Índice de Massa Corporal).
  - Entrada: peso (kg) e altura (m). Saída: valor do IMC, classificação (Abaixo do peso / Peso normal / Sobrepeso / Obesidade), barra de progresso visual e gráfico de faixas.

- `dashboard.py`
  - Dashboard para análise de ataques cibernéticos a partir de um CSV (`cyber_attacks.csv`).
  - Funcionalidades: upload automático/por upload, sidebar com filtros (ano, país, tipo de ataque), KPIs, tabela, gráficos (por ano e top países) e mapa mundi choropleth.
  - Observação: para o mapa é recomendado instalar `pycountry` para mapear nomes de países para ISO3.

- `chatbot_openai.py`
  - Chatbot que conversa com o usuário via API OpenAI.
  - Mantém histórico em `st.session_state`, exibe mensagens em bolhas e possui campo para inserir `OPENAI_API_KEY` na sidebar.

- `pdf_summarizer.py`
  - Upload de PDF, extração de texto (PyPDF2), resumo e classificação via OpenAI e Q/A sobre o documento.
  - Histórico salvo em `semana-07/pdf_history.json` e PDFs guardados em `semana-07/history_pdfs/`.

- `soc_agent_ui.py`
  - Interface para enviar um IP/URL a um agente SOC implementado no n8n via webhook.
  - Mostra resultado na tela, salva histórico em `semana-07/soc_history.json` e permite exportar relatórios em PDF (usa `fpdf`) ou JSON.

- `language_tutor.py`
  - Instrutor de idiomas simples com plano de estudo, dicas, flashcards e exercícios rápidos.
  - Opção de gerar conteúdo (ex.: frases, exercícios) via OpenAI quando a chave é fornecida.


## Como executar (exemplos)

1. Crie/ative um ambiente Python e instale dependências essenciais:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install streamlit pandas plotly altair openai PyPDF2 fpdf requests pycountry
```

2. Execute o app desejado (exemplos):

```bash
streamlit run semana-07/dashboard.py
streamlit run semana-07/chatbot_openai.py
streamlit run semana-07/pdf_summarizer.py
streamlit run semana-07/soc_agent_ui.py
streamlit run semana-07/language_tutor.py
```

Observações:
- Para usar recursos da OpenAI, defina a variável `OPENAI_API_KEY` ou cole a chave no campo da sidebar dos apps.
- O `dashboard.py` procura por `cyber_attacks.csv` na raiz ou `data/`. Caso não exista, use o uploader na sidebar.
- O `soc_agent_ui.py` necessita da URL do webhook do n8n (configurar na sidebar ou via variável `N8N_SOC_WEBHOOK`).


## Arquivos de histórico

- `semana-07/pdf_history.json` — histórico de PDFs processados (quando existe).
- `semana-07/history_pdfs/` — PDFs enviados pelo usuário.
- `semana-07/soc_history.json` — histórico de investigações SOC.


## Sugestões e próximos passos

- Gerar um `requirements.txt` com as dependências usadas neste diretório.
- Adicionar testes básicos e exemplos de dados (CSV) para facilitar demonstrações.
- Melhorar UI/tema e adicionar autenticação quando expor webhooks.

---

Se quiser, eu gero o `requirements.txt` com as dependências detectadas e adiciono exemplos de uso/dados para cada app. Quer que eu crie isso agora?
