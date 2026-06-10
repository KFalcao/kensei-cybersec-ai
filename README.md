# Kensei Cybersec AI

Um repositório dedicado ao estudo e desenvolvimento de soluções que combinam **Cibersegurança** e **Inteligência Artificial**.

## 🎯 Objetivo

Este projeto tem como objetivo explorar e documentar técnicas, ferramentas e estratégias na interseção entre cibersegurança e IA, incluindo:

- Detecção de anomalias e ameaças usando ML
- Análise de vulnerabilidades com IA
- Sistemas de defesa adaptáveis
- Processamento de linguagem natural para análise de segurança
- Automação de respostas a incidentes
- Padrões de detecção de ataques cibernéticos

## 📚 Estrutura do Repositório

```
kensei-cybersec-ai/
├── README.md
├── docs/
│   └── Documentação e guias de estudo
├── notebooks/
│   └── Jupyter notebooks para análise e experimentação
├── src/
│   └── Código-fonte de aplicações e ferramentas
├── datasets/
│   └── Conjuntos de dados para treinamento e análise
├── models/
│   └── Modelos de ML treinados
└── requirements.txt
```

## 🛠️ Tecnologias

- **Python 3.x** - Linguagem principal
- **TensorFlow / PyTorch** - Frameworks de ML
- **Scikit-learn** - Machine Learning
- **Pandas / NumPy** - Processamento de dados
- **Jupyter Notebooks** - Experimentação interativa
- **Git** - Controle de versão

## 🚀 Como Começar

### Pré-requisitos

- Python 3.8+
- pip ou conda
- Git

### Instalação

```bash
# Clone o repositório
git clone https://github.com/KFalcao/kensei-cybersec-ai.git
cd kensei-cybersec-ai

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

## 📖 Tópicos de Estudo

### Segurança
- Malware Analysis
- Network Security
- Threat Intelligence
- Vulnerability Assessment
- Incident Response

### Inteligência Artificial
- Supervised Learning
- Unsupervised Learning
- Deep Learning
- Natural Language Processing (NLP)
- Anomaly Detection

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## 📧 Contato

Para dúvidas ou sugestões, entre em contato através de:
- GitHub Issues
- Email: [seu-email@exemplo.com]

---

**Data de Criação:** Abril de 2026

**Status:** Em Desenvolvimento 🚧

---

PROMT Utilizado: Crie um README.MD para o este repoitório que será de estudos de cybersec e IA. Faça commit desse projeto para o github no repositorio abaixo https://github.com/KFalcao/kensei-cybersec-ai

## 📁 Projetos por Semana

A seguir há uma descrição resumida dos exemplos e apps organizados por pasta `semana-*`.

- **semana-02/** — Scripts introdutórios e utilitários (ex.: `celsius_to_fahrenheit.py`, `conversor_moedas.py`, `gerador_senhas.py`, `hello.py`, `lista_de_compras.py`).
- **semana-03/** — Análise de dados de incidentes: `01_explore_data.py`, `02_clean_data.py`, `03_analyze_private.py`, `04_visualize_incidents.py` e os datasets `incidents_master.csv` / `incidents_master_cleaned.csv`.
- **semana-04/** — Pequenas aplicações e automações (ex.: `app.py`, `chatbot_terminal.py`, `translate.py`, `run_report.py`).
- **semana-06/** — Definições de agentes e protótipos (arquivos JSON de agentes para experimentação).
- **semana-07/** — Aplicações Streamlit e ferramentas interativas importantes:
	- `calculadora_imc.py`: calculadora de IMC com visualização e gráfico.
	- `dashboard.py`: dashboard para análise de ataques cibernéticos a partir de CSV (KPIs, gráficos, mapa mundi choropleth).
	- `chatbot_openai.py`: chatbot com histórico em sessão e bolhas de chat; usa `OPENAI_API_KEY`.
	- `pdf_summarizer.py`: upload de PDFs, extração de texto (PyPDF2), resumo/classificação via OpenAI e Q/A sobre o documento; histórico salvo em `semana-07/pdf_history.json` e PDFs em `semana-07/history_pdfs/`.
	- `soc_agent_ui.py`: UI que chama um agente SOC no n8n via webhook, mostra resultado, salva histórico e permite exportar relatórios em PDF/JSON.
	- `language_tutor.py`: instrutor de idiomas com plano de estudos, flashcards, exercícios e integração opcional com OpenAI para gerar conteúdo.

## ▶️ Executando exemplos Streamlit

1. Crie/ative seu ambiente Python e instale dependências (exemplo):
```bash
python -m venv .venv
source .venv/bin/activate   # ou .venv\Scripts\activate no Windows
pip install -r requirements.txt
```
2. Execute um app na pasta `semana-07`, por exemplo:
```bash
streamlit run semana-07/dashboard.py
streamlit run semana-07/chatbot_openai.py
streamlit run semana-07/pdf_summarizer.py
```

## ℹ️ Observações
- Vários exemplos requerem chaves externas (ex.: `OPENAI_API_KEY`) — defina via variável de ambiente ou copie `.env.example` para `.env`.
- O diretório `semana-07/` também possui um README local (`semana-07/README.md`) com descrições detalhadas de cada app.
- Este README é um panorama rápido; cada pasta `semana-*` contém documentação e comentários nos próprios scripts.


