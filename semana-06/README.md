# Semana 06 - Workflows de Agentes com n8n + LangChain

Esta pasta contém definições de workflows (no formato JSON) que implementam agentes inteligentes usando **n8n** e **LangChain**. Cada agente é um chatbot especializado com acesso a ferramentas específicas para resolver tarefas.

---

## 📋 Arquivos de Workflow

### 1. **agent_pesquisador.json**
**Agente Pesquisador Investigativo**

Um pesquisador analítico que investiga tópicos em profundidade.

**Ferramentas disponíveis:**
- Wikipedia (acesso a conteúdo enciclopédico)
- SerpAPI (busca na web)
- URLs adicionais para cruzamento de fontes

**Caso de uso:**
- Pesquisar tópicos históricos ou técnicos
- Investigar conceitos complexos em cibersegurança
- Compilar resumos estruturados com citações de fontes

**Como usar:**
1. Importar o JSON no n8n
2. Configurar credenciais de SerpAPI
3. Ativar o workflow
4. Enviar mensagens pelo chat pedindo pesquisas

---

### 2. **agent_viagem.json**
**Agente Consultor de Viagens Expert**

Um consultor sênior de turismo que planeja itinerários e orçamentos de viagens.

**Ferramentas disponíveis:**
- SerpAPI (buscar voos, hotéis, atrações)
- Calculadora (estimar custos, converter moedas)
- Consulta de informações turísticas

**Caso de uso:**
- Planejar roteiros dia a dia
- Pesquisar preços de voos e hospedagem
- Estimar orçamento total de viagem
- Obter dicas locais e informações de clima

**Como usar:**
1. Importar o JSON no n8n
2. Configurar SerpAPI com chave válida
3. Iniciar o workflow
4. Conversar informando destino, orçamento, datas e estilo de viagem

---

### 3. **analista_dados.json**
**Agente Analista de Dados (CSV + Python/Pandas)**

Um analista de dados sênior que responde perguntas em linguagem natural sobre dados em CSV.

**Ferramentas disponíveis:**
- Ferramenta de Código (Python/Pandas) — executa scripts para analisar DataFrames
- Calculadora (para operações matemáticas simples)
- Processamento de arquivos CSV

**Caso de uso:**
- Responder perguntas sobre dados tabulares
- Filtrar e agrupar dados dinamicamente
- Calcular estatísticas e gerar insights
- Traduzir resultados técnicos em linguagem de negócio

**Como usar:**
1. Importar o JSON no n8n
2. Conectar um nó de upload de CSV antes do agente
3. Perguntar ao agente em português, ex:
   - "Qual é a média de incidentes por mês?"
   - "Liste os 5 tipos de ataque mais frequentes"
   - "Qual a distribuição de severidade?"

---

### 4. **chat_calc.json**
**Assistente Generalista com Calculadora e Wikipedia**

Um assistente versátil que combina conversação natural com ferramentas úteis.

**Ferramentas disponíveis:**
- Calculadora (operações matemáticas, conversões de unidades)
- Wikipedia (dados enciclopédicos)

**Caso de uso:**
- Respostas gerais sobre vários tópicos
- Cálculos de física, conversões (km→miles, °C→°F, etc.)
- Pesquisas rápidas de informações históricas ou biográficas

**Como usar:**
1. Importar o JSON no n8n
2. Ativar o workflow
3. Fazer perguntas, ex:
   - "Quanto é 25 km em milhas?"
   - "Quem foi Albert Einstein?"
   - "Calcule 15% de 250"

---

### 5. **soc_agent.json**
**Agente de Investigação de Segurança (VirusTotal + URLScan)**

Um analista de inteligência de ameaças que investiga a segurança de IPs, domínios e URLs.

**Ferramentas disponíveis:**
- VirusTotal API (verificação de reputação de IPs, domínios, URLs)
- URLScan (análise profunda de páginas web)
- Classificação de ameaças (SEGURO / SUSPEITO / MALICIOSO)

**Caso de uso:**
- Verificar reputação de domínios suspeitos
- Analisar URLs encontradas em e-mails
- Investigar IPs de origem de tráfego estranho
- Consultar detecções de antivírus cruzadas
- Identificar redirecionamentos maliciosos

**Como usar:**
1. Importar o JSON no n8n
2. Configurar API keys:
   - VirusTotal API key (https://www.virustotal.com/api/v3/)
   - URLScan API key (https://urlscan.io/)
3. Ativar o workflow
4. Enviar para análise:
   - "Verificar se 192.168.1.1 é seguro"
   - "Investigar site: example-phishing.com"
   - "Analisar URL: http://suspicious-link.xyz/payload"

---

## 🛠️ Configuração Geral

### Pré-requisitos
- **n8n** instalado e rodando (cloud ou self-hosted)
- **LangChain** integrado ao n8n
- **OpenAI API key** (modelo: gpt-4o-mini)
- Chaves de API específicas para cada workflow:
  - SerpAPI (para pesquisa web)
  - VirusTotal (para análise de segurança)
  - URLScan (para análise de URLs)

### Passos de Importação
1. Abrir n8n em seu navegador
2. Clicar em **+ Workflow** → **Import from File**
3. Selecionar um dos arquivos JSON
4. Revisar os nós e credenciais
5. Configurar credenciais faltantes
6. Testar o fluxo (enviar mensagem de teste)
7. Ativar o workflow (botão "Activate")

### Estrutura Comum
Cada workflow segue este padrão:
- **Chat Trigger** — escuta mensagens do usuário
- **AI Agent** — orquestra a lógica usando LangChain
- **OpenAI Chat Model** — modelo de linguagem (gpt-4o-mini)
- **Ferramentas** — acesso a APIs externas (SerpAPI, Wikipedia, calculadora, etc.)

---

## 📊 Comparação de Agentes

| Agente | Especialidade | Ferramentas | Melhor para |
|--------|---------------|-----------|-----------|
| **Pesquisador** | Investigação em profundidade | Wikipedia, Web Search | Pesquisa acadêmica, análise de tópicos |
| **Viagem** | Planejamento turístico | SerpAPI, Calculadora | Roteiros, orçamentos, dicas de viagem |
| **Analista Dados** | Análise de dados tabulares | Python/Pandas, Calculadora | Q&A sobre CSV, insights rápidos |
| **Generalista** | Assistência geral | Calculadora, Wikipedia | Perguntas diversas, cálculos |
| **SOC/Segurança** | Análise de ameaças | VirusTotal, URLScan | Investigação de domínios, IPs, URLs |

---

## 🔐 Notas de Segurança

- **Credenciais**: Nunca comitar chaves de API no GitHub. Use variáveis de ambiente ou n8n Credentials Manager.
- **VirusTotal & URLScan**: APIs sensíveis — guardar com acesso restrito.
- **SerpAPI**: Verificar quotas de uso para evitar exceder limites.

---

## 💡 Exemplos de Uso

### Pesquisador
```
Usuário: "Investigue o histórico do malware WannaCry"
Agente: [busca Wikipedia e web] → "WannaCry foi um ransomware que..."
```

### Consultor de Viagens
```
Usuário: "Quero viajar para Barcelona em julho por 2 semanas com orçamento de R$5000"
Agente: [pesquisa voos, hotéis, atrações] → "Aqui está o roteiro e orçamento..."
```

### Analista de Dados
```
Usuário: "Qual o tipo de ataque mais comum no CSV?"
Agente: [executa Pandas] → "O tipo mais comum é phishing com 35% dos casos..."
```

### Generalista
```
Usuário: "Quanto é 50 km em milhas?"
Agente: [calculadora] → "50 km = 31,07 milhas"
```

### SOC Agent
```
Usuário: "Verificar domínio suspicious-site.xyz"
Agente: [VirusTotal + URLScan] → "[MALICIOSO] Detectado em 23 motores de antivírus..."
```

---

## 📝 Próximos Passos

- [ ] Testar cada workflow individualmente
- [ ] Criar credenciais de teste nas plataformas de API
- [ ] Ajustar `systemMessage` para tom/linguagem preferidos
- [ ] Adicionar nós de logging para auditoria
- [ ] Integrar webhooks para notificações em tempo real
- [ ] Criar dashboards para análise de histórico de consultas

---

**Data de Criação**: Junho 2026  
**Status**: Workflows prontos para teste e deployment
