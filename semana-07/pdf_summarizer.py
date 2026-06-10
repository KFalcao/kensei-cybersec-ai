import streamlit as st
import os
from pathlib import Path
import json
from datetime import datetime
import shutil


st.set_page_config(page_title="PDF Summarizer", layout="wide")


HISTORY_PATH = Path(__file__).parent / 'pdf_history.json'
HISTORY_DIR = Path(__file__).parent / 'history_pdfs'
HISTORY_DIR.mkdir(exist_ok=True)


def init_state():
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.environ.get('OPENAI_API_KEY', '')
    if 'history' not in st.session_state:
        if HISTORY_PATH.exists():
            try:
                st.session_state.history = json.loads(HISTORY_PATH.read_text())
            except Exception:
                st.session_state.history = []
        else:
            st.session_state.history = []


def save_history():
    try:
        HISTORY_PATH.write_text(json.dumps(
            st.session_state.history, ensure_ascii=False, indent=2))
    except Exception:
        pass


def add_history_entry(filename, summary):
    entry = {
        'filename': filename,
        'summary': summary,
        'date': datetime.utcnow().isoformat() + 'Z'
    }
    st.session_state.history.insert(0, entry)
    save_history()


def extract_text_from_pdf(path: Path) -> str:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        st.error('Instale PyPDF2: pip install PyPDF2')
        return ''
    try:
        reader = PdfReader(str(path))
        texts = []
        for page in reader.pages:
            txt = page.extract_text()
            if txt:
                texts.append(txt)
        return '\n'.join(texts)
    except Exception as e:
        st.error(f'Erro ao extrair PDF: {e}')
        return ''


def call_openai_summary(text: str, api_key: str) -> dict:
    try:
        import openai
    except Exception:
        return {'error': 'openai library not installed. pip install openai'}

    openai.api_key = api_key

    # limit text to reasonable size to avoid token overflow
    short = text[:3000]
    prompt = f"""
Você é um assistente que resume e classifica documentos.
Receba o texto do documento abaixo e retorne um JSON com campos:
- summary: resumo em até 200 palavras
- classification: lista curta de tags separadas por vírgula
Retorne apenas JSON.

Texto:
""" + short

    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.3,
            max_tokens=600,
        )
        content = resp.choices[0].message.content.strip()
        # try parse JSON from content
        try:
            return json.loads(content)
        except Exception:
            # fallback: return text as summary
            return {'summary': content, 'classification': ''}
    except Exception as e:
        return {'error': str(e)}


def call_openai_answer(prompt_text: str, question: str, api_key: str) -> str:
    try:
        import openai
    except Exception:
        return 'openai library not installed. pip install openai'
    openai.api_key = api_key
    messages = [
        {'role': 'system', 'content': 'Você responde perguntas com base no contexto fornecido.'},
        {'role': 'user', 'content': prompt_text + '\n\nPergunta: ' + question}
    ]
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.2,
            max_tokens=500,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f'Erro: {e}'


def main():
    init_state()

    st.title('PDF Summarizer & Q/A')
    st.sidebar.header('Config')
    st.session_state.api_key = st.sidebar.text_input(
        'OPENAI_API_KEY', value=st.session_state.api_key, type='password')

    st.sidebar.markdown('Histórico de PDFs analisados:')
    for i, h in enumerate(st.session_state.history[:20]):
        label = f"{h['filename']} — {h['date'][:10]}"
        if st.sidebar.button(label, key=f'hist_{i}'):
            st.session_state.selected_history = h

    if st.sidebar.button('Limpar histórico'):
        st.session_state.history = []
        save_history()

    # Main area
    uploaded = st.file_uploader(
        'Envie um PDF para resumir e classificar', type=['pdf'])
    selected_text = ''
    if uploaded is not None:
        save_path = HISTORY_DIR / uploaded.name
        with open(save_path, 'wb') as f:
            shutil.copyfileobj(uploaded, f)
        st.success(f'Arquivo salvo em {save_path}')
        text = extract_text_from_pdf(save_path)
        if not text:
            st.warning('Nenhum texto extraído do PDF.')
            return
        st.session_state.current_text = text
        with st.spinner('Resumindo e classificando com a IA...'):
            res = call_openai_summary(text, st.session_state.api_key)
        if 'error' in res:
            st.error(res['error'])
            return
        summary = res.get('summary', '')
        classification = res.get('classification', '')
        st.subheader('Resumo')
        st.write(summary)
        st.subheader('Classificação')
        st.write(classification)
        add_history_entry(uploaded.name, summary)
        selected_text = text

    # If user clicked a history item, show its summary
    if 'selected_history' in st.session_state:
        h = st.session_state.selected_history
        st.subheader(f"Histórico — {h['filename']}")
        st.markdown(f"**Data:** {h['date']}")
        st.markdown(f"**Resumo:**\n{h['summary']}")
        # try to load text file if exists
        hist_path = HISTORY_DIR / h['filename']
        if hist_path.exists():
            t = extract_text_from_pdf(hist_path)
            st.session_state.current_text = t

    # Q&A
    st.markdown('---')
    st.subheader('Pergunte sobre o documento')
    question = st.text_input('Pergunta')
    if st.button('Perguntar'):
        if not st.session_state.api_key:
            st.error('Insira OPENAI_API_KEY na sidebar.')
        elif 'current_text' not in st.session_state or not st.session_state.current_text:
            st.warning(
                'Nenhum documento carregado ou selecionado no histórico.')
        else:
            context = st.session_state.current_text[:3000]
            answer = call_openai_answer(
                context, question, st.session_state.api_key)
            st.subheader('Resposta')
            st.write(answer)


if __name__ == '__main__':
    main()
