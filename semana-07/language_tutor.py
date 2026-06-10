import streamlit as st
import random
import textwrap

st.set_page_config(page_title='Language Tutor', layout='centered')

LANG_VOCAB = {
    'English': [('hello', 'olá'), ('thank you', 'obrigado'), ('please', 'por favor'), ('water', 'água'), ('food', 'comida')],
    'Spanish': [('hola', 'hello'), ('gracias', 'thank you'), ('por favor', 'please'), ('agua', 'water'), ('comida', 'food')],
    'French': [('bonjour', 'hello'), ('merci', 'thank you'), ('s\'il vous plaît', 'please'), ('eau', 'water'), ('nourriture', 'food')],
    'German': [('hallo', 'hello'), ('danke', 'thank you'), ('bitte', 'please'), ('Wasser', 'water'), ('Essen', 'food')],
    'Portuguese': [('olá', 'hello'), ('obrigado', 'thank you'), ('por favor', 'please'), ('água', 'water'), ('comida', 'food')],
}

EXERCISES = {
    'English': [
        ("I __ to the store.", "went"),
        ("She __ a book.", "reads"),
    ],
    'Spanish': [
        ("Yo __ agua.", "bebo"),
        ("Ella __ un libro.", "lee"),
    ],
}


def init_state():
    if 'flash_idx' not in st.session_state:
        st.session_state.flash_idx = 0
    if 'known' not in st.session_state:
        st.session_state.known = set()


def study_plan(language, level, weekly_minutes):
    minutes = int(weekly_minutes)
    plan = []
    per_day = max(10, minutes // 7)
    plan.append(f"Estudo recomendado: {per_day} minutos por dia.")
    if level == 'Beginner':
        plan.append(
            'Foco nas bases: saudações, vocabulário essencial, pronúncia.')
        plan.append(
            'Sessões: vocabulário + listening curto + prática oral (10 min cada).')
    elif level == 'Intermediate':
        plan.append(
            'Foco em gramática básica, leitura curta e conversação estruturada.')
    else:
        plan.append(
            'Foco em fluência: leituras, podcasts, produção escrita e revisão de erros.')
    plan.append(
        'Dica: revisite vocabulário com espaçamento (SRS) e fale em voz alta.')
    return plan


def show_tips():
    st.subheader('Dicas de estudo')
    tips = [
        'Use pequenos blocos de tempo (10–25 min) com foco total.',
        'Pratique fala todos os dias — mesmo 5 minutos falados ajudam.',
        'Anote 5 palavras novas por dia e revise nos próximos 7 dias.',
        'Combine recursos: vídeo + transcript + SRS (flashcards).',
        'Foque em frases úteis, não apenas palavras isoladas.'
    ]
    for t in tips:
        st.write('•', t)


def show_flashcard(language):
    vocab = LANG_VOCAB.get(language, [])
    if not vocab:
        st.info('Sem vocabulário disponível para esta língua.')
        return
    idx = st.session_state.flash_idx % len(vocab)
    word, meaning = vocab[idx]
    st.markdown(f"### {word}")
    if st.button('Mostrar tradução'):
        st.success(meaning)
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Conheço'):
            st.session_state.known.add(word)
            st.session_state.flash_idx += 1
    with col2:
        if st.button('Próxima'):
            st.session_state.flash_idx += 1
    st.write(f'Conhecidas nesta sessão: {len(st.session_state.known)}')


def show_exercise(language):
    exs = EXERCISES.get(language)
    if not exs:
        st.info('Sem exercícios prontos para esta língua — tente criar com a IA.')
        return
    sent, answer = random.choice(exs)
    st.write('Preencha a lacuna:')
    st.write(sent)
    resp = st.text_input('Sua resposta', key='exercise_input')
    if st.button('Checar resposta'):
        if resp.strip().lower() == answer.lower():
            st.success('Correto!')
        else:
            st.error(f'Incorreto — resposta: {answer}')


def generate_with_openai(prompt, api_key):
    try:
        import openai
    except Exception:
        return 'openai library not instalado. pip install openai'
    openai.api_key = api_key
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.7,
            max_tokens=400
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f'Erro: {e}'


def main():
    init_state()
    st.title('Instrutor de Idiomas — Tutor de Estudos')

    st.sidebar.header('Configuração')
    language = st.sidebar.selectbox('Idioma alvo', list(LANG_VOCAB.keys()))
    level = st.sidebar.selectbox(
        'Nível', ['Beginner', 'Intermediate', 'Advanced'])
    weekly = st.sidebar.slider('Minutos por semana', 30, 840, 210)
    api_key = st.sidebar.text_input(
        'OPENAI_API_KEY (opcional)', type='password')

    st.header('Plano de estudo personalizado')
    plan = study_plan(language, level, weekly)
    for p in plan:
        st.write('- ', p)

    st.markdown('---')
    show_tips()

    st.markdown('---')
    st.subheader('Flashcards')
    show_flashcard(language)

    st.markdown('---')
    st.subheader('Exercício rápido')
    show_exercise(language)

    st.markdown('---')
    st.subheader('Gerar conteúdo com IA (opcional)')
    prompt = st.text_area(
        'Peça ao instrutor IA: por exemplo, "Crie 5 frases para praticar o passado em inglês"', height=120)
    if st.button('Gerar com OpenAI'):
        if not api_key:
            st.error('Forneça OPENAI_API_KEY na sidebar para usar a IA.')
        elif not prompt.strip():
            st.warning('Escreva um pedido na caixa de texto.')
        else:
            with st.spinner('Gerando...'):
                out = generate_with_openai(prompt, api_key)
            st.text_area('Resultado (IA)', value=out, height=240)


if __name__ == '__main__':
    main()
