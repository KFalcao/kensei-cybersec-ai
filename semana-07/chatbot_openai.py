import streamlit as st
import os
from typing import List, Dict

st.set_page_config(page_title="Chatbot OpenAI", layout="wide")

CSS = """
<style>
.chat-container{max-width:900px;margin:auto}
.chat-bubble{padding:12px;border-radius:12px;margin:8px 0;display:inline-block;max-width:80%}
.user{background:#DCF8C6;align-self:flex-end}
.assistant{background:#F1F0F0}
.chat-row{display:flex;flex-direction:row}
.user-row{justify-content:flex-end}
.assistant-row{justify-content:flex-start}
.meta{font-size:12px;color:#666;margin-bottom:4px}
</style>
"""


def init_state():
    if 'messages' not in st.session_state:
        # list of dicts {'role': str, 'content': str}
        st.session_state.messages = []
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.environ.get('OPENAI_API_KEY', '')


def call_openai_api(messages: List[Dict[str, str]], api_key: str) -> str:
    try:
        import openai
    except Exception as e:
        st.error('Biblioteca `openai` não instalada. Execute: pip install openai')
        return 'Erro: openai não disponível'

    openai.api_key = api_key
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        st.error(f'Erro ao chamar OpenAI: {e}')
        return f'Erro ao chamar OpenAI: {e}'


def render_messages():
    st.markdown("<div class='chat-container'>" + CSS, unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role = msg.get('role')
        content = msg.get('content')
        if role == 'user':
            st.markdown(
                f"<div class='chat-row user-row'><div class='chat-bubble user'>{content}</div></div>", unsafe_allow_html=True)
        elif role == 'assistant':
            st.markdown(
                f"<div class='chat-row assistant-row'><div class='chat-bubble assistant'>{content}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div class='chat-row assistant-row'><div class='chat-bubble assistant'><b>System:</b> {content}</div></div>", unsafe_allow_html=True)


def main():
    init_state()

    st.title('Chatbot com OpenAI')
    st.sidebar.header('Configuração')
    api_key = st.sidebar.text_input(
        'OPENAI_API_KEY', value=st.session_state.api_key, type='password')
    st.session_state.api_key = api_key

    st.sidebar.markdown(
        'Insira sua chave OpenAI acima. Você também pode definir a variável de ambiente `OPENAI_API_KEY` para usar automaticamente.')
    if st.sidebar.button('Limpar histórico'):
        st.session_state.messages = []

    system_prompt = st.sidebar.text_area(
        'System prompt (opcional)', value='Você é um assistente útil.', height=80)

    if system_prompt and (len(st.session_state.messages) == 0 or st.session_state.messages[0].get('role') != 'system'):
        # ensure system prompt is first message
        st.session_state.messages.insert(
            0, {'role': 'system', 'content': system_prompt})

    # Chat area
    chat_col, input_col = st.columns([4, 1])
    with chat_col:
        render_messages()

    with input_col:
        user_input = st.text_area('Sua mensagem', key='user_input', height=120)
        if st.button('Enviar'):
            if not st.session_state.api_key:
                st.error('Insira a OPENAI_API_KEY no sidebar antes de enviar.')
            elif not user_input.strip():
                st.warning('Escreva uma mensagem para enviar.')
            else:
                # Append user message
                st.session_state.messages.append(
                    {'role': 'user', 'content': user_input})
                with st.spinner('Aguardando resposta do modelo...'):
                    assistant_text = call_openai_api(
                        st.session_state.messages, st.session_state.api_key)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': assistant_text})
                st.experimental_rerun()


if __name__ == '__main__':
    main()
