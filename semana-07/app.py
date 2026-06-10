import streamlit as st
import pandas as pd
import altair as alt


st.set_page_config(page_title="Calculadora de IMC", layout="centered")

st.title("Calculadora de IMC")
st.write("Digite seu peso e altura para calcular o Índice de Massa Corporal (IMC).")

col1, col2 = st.columns(2)

with col1:
    peso = st.number_input("Peso (kg)", min_value=0.0,
                           format="%.2f", value=70.0)
with col2:
    altura = st.number_input(
        "Altura (m)", min_value=0.0, format="%.2f", value=1.75)

if altura <= 0 or peso <= 0:
    st.warning("Por favor insira peso e altura maiores que zero.")
else:
    imc = peso / (altura ** 2)
    imc_text = f"{imc:.2f}"

    # Classificação do IMC
    if imc < 18.5:
        categoria = "Abaixo do peso"
        nivel = "underweight"
    elif imc < 25:
        categoria = "Peso normal"
        nivel = "normal"
    elif imc < 30:
        categoria = "Sobrepeso"
        nivel = "overweight"
    else:
        categoria = "Obesidade"
        nivel = "obesity"

    st.subheader("Resultado")
    st.markdown(f"**IMC:** {imc_text}")

    # Mensagem colorida de classificação (usando alert helpers do Streamlit)
    if nivel == "underweight":
        st.info(f"Classificação: {categoria}")
    elif nivel == "normal":
        st.success(f"Classificação: {categoria}")
    elif nivel == "overweight":
        st.warning(f"Classificação: {categoria}")
    else:
        st.error(f"Classificação: {categoria}")

    # Barra de progresso visual: mapeia IMC entre 10 e 40 para 0-100%
    min_bmi = 10
    max_bmi = 40
    pct = int(100 * (min(max(imc, min_bmi), max_bmi) -
              min_bmi) / (max_bmi - min_bmi))
    st.write("Visualização do IMC:")
    st.progress(pct)

    # Gráfico de barras com faixas de IMC e indicador do usuário
    ranges = [
        {"category": "Abaixo do peso", "start": 10,
            "end": 18.5, "color": "#4da6ff"},
        {"category": "Peso normal", "start": 18.5, "end": 25, "color": "#4CAF50"},
        {"category": "Sobrepeso", "start": 25, "end": 30, "color": "#FFB74D"},
        {"category": "Obesidade", "start": 30, "end": 40, "color": "#e53935"},
    ]

    df = pd.DataFrame(ranges)

    base = alt.Chart(df).mark_bar().encode(
        x=alt.X('start:Q', title='IMC', scale=alt.Scale(domain=[10, 40])),
        x2='end:Q',
        y=alt.Y('category:N', axis=alt.Axis(title=None), sort=None),
        color=alt.Color('category:N', scale=alt.Scale(
            domain=df['category'].tolist(), range=df['color'].tolist()), legend=None)
    ).properties(height=120, width=600)

    rule = alt.Chart(pd.DataFrame({'imc': [imc]})).mark_rule(color='black', strokeWidth=3).encode(
        x='imc:Q'
    )

    text = alt.Chart(pd.DataFrame({'imc': [imc], 'label': [f'IMC {imc_text}']})).mark_text(align='left', dx=5, dy=-10).encode(
        x='imc:Q',
        text='label:N'
    )

    chart = (base + rule + text).configure_view(strokeWidth=0)
    st.altair_chart(chart, use_container_width=True)

    # Nota explicativa
    st.caption(
        "Mapa aproximado: 10 (baixo) → 40 (alto). Consulte um profissional de saúde para avaliação completa.")
