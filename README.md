# Kensei Cybersec AI

Bem-vindo ao repositório `Kensei Cybersec AI` — um espaço de aprendizado prático para projetos de cibersegurança, automação e inteligência artificial.

---

## 🌟 Visão Geral

Este repositório reúne experimentos, aplicações e protótipos desenvolvidos por semana. O foco está em:

- aprendizado contínuo em Python;
- exemplos de análise de dados de segurança;
- automações e utilitários práticos;
- aplicações interativas com Streamlit;
- integração com APIs e agentes inteligentes.

---

## 📁 Estrutura de Pastas

```text
kensei-cybersec-ai/
├── .env.example        # modelo de variáveis de ambiente
├── .gitignore
├── README.md           # documento principal do repositório
├── requirements.txt    # dependências Python do projeto
├── semana-02/          # exercícios básicos e utilitários em Python
├── semana-03/          # análise de dados de incidentes e visualização
├── semana-04/          # apps menores, automações e chatbots simples
├── semana-05-cancelada/ # pasta reservada para semana cancelada
├── semana-06/          # protótipos de agentes e definições JSON
└── semana-07/          # apps interativos e projetos Streamlit
```

---

## 📌 Descrição por Pasta

### `semana-02/`
Projetos introdutórios com pequenos scripts e utilitários para prática em Python.

Exemplos:
- `celsius_to_fahrenheit.py` — conversão de temperaturas
- `conversor_moedas.py` — conversão de moedas
- `gerador_senhas.py` — geração de senhas seguras
- `lista_de_compras.py` — organizador de itens
- `organizador_arquivos.py` — automação de arquivos
- `quiz_cybersecurity.py` — quiz de cibersegurança

### `semana-03/`
Análise de dados de incidentes de segurança e preparação de gráficos.

Exemplos:
- `01_explore_data.py` — exploração inicial dos dados
- `02_clean_data.py` — limpeza do conjunto de dados
- `03_analyze_private.py` — análise adicional de incidentes
- `04_visualize_incidents.py` — visualizações e gráficos
- `incidents_master.csv` / `incidents_master_cleaned.csv` — dados usados nos scripts

### `semana-04/`
Aplicações e automações escritas em Python para tarefas práticas.

Exemplos:
- `app.py` — aplicação principal ou demo
- `chatbot_terminal.py` — chatbot rodando no terminal
- `translate.py` — tradução de texto
- `run_report.py` — gera relatórios a partir de dados
- `analyze_csv_report.py` / `analyze_text.py` — análise de CSV e texto

### `semana-05-cancelada/`
Espaço reservado para uma semana que foi cancelada.

### `semana-06/`
Protótipos de agentes e arquivos JSON para experimentação em agentes conversacionais.

Arquivos notáveis:
- `agent_pesquisador.json`
- `agent_viagem.json`
- `analista_dados.json`
- `chat_calc.json`
- `soc_agent.json`

### `semana-07/`
Projetos mais maduros e interativos, muitos usando Streamlit e automação de IA.

Principais aplicações:
- `dashboard.py` — painel de análise de ataques cibernéticos
- `chatbot_openai.py` — chatbot com integração OpenAI
- `pdf_summarizer.py` — resumo e Q/A de documentos PDF
- `soc_agent_ui.py` — interface para agente SOC via webhook
- `language_tutor.py` — tutor de idiomas com plano de estudos
- `calculadora_imc.py` — ferramenta de cálculo de IMC

---

## 🚀 Como rodar o projeto

### 1. Criar ambiente Python

```bash
python -m venv .venv
```

### 2. Ativar o ambiente

No Windows:

```powershell
.venv\Scripts\activate
```

No macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar um app Streamlit

```bash
streamlit run semana-07/dashboard.py
```

Outros exemplos:

```bash
streamlit run semana-07/chatbot_openai.py
streamlit run semana-07/pdf_summarizer.py
```

---

## ⚠️ Observações

- Alguns exemplos podem exigir variáveis de ambiente, como `OPENAI_API_KEY`.
- Use o arquivo `.env.example` como modelo ao criar um arquivo `.env`.
- Cada pasta `semana-*` pode ter documentação própria e comentários nos scripts.

---

## 💡 Dicas

- Comece por `semana-02/` se quiser revisar conceitos básicos em Python.
- Vá para `semana-03/` para trabalhar com análise de dados de incidentes.
- Explore `semana-07/` para ver aplicações interativas e integrações com IA.

---

## 🤝 Contribuições

Contribuições são bem-vindas!

1. Faça um fork
2. Crie uma branch de feature
3. Abra um pull request

---

## 📚 Licença

Projeto distribuído sob a licença MIT.


