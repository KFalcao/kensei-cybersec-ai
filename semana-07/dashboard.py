import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Cyber Attacks Dashboard", layout="wide")


def load_dataset():
    # Try common locations for the CSV
    candidates = [Path("cyber_attacks.csv"), Path("data/cyber_attacks.csv")]
    for p in candidates:
        if p.exists():
            try:
                return pd.read_csv(p)
            except Exception:
                pass

    uploaded = st.sidebar.file_uploader(
        "Carregar CSV (ex: cyber_attacks.csv)", type=["csv"])
    if uploaded is not None:
        return pd.read_csv(uploaded)

    st.sidebar.info(
        "Nenhum arquivo encontrado automaticamente. Faça upload do CSV ou coloque 'cyber_attacks.csv' na raiz do projeto.")
    return None


@st.cache_data
def map_countries_to_iso3(country_series):
    try:
        import pycountry
    except Exception:
        return pd.Series([None] * len(country_series), index=country_series.index)

    def to_iso3(name):
        if pd.isna(name):
            return None
        try:
            return pycountry.countries.lookup(name).alpha_3
        except Exception:
            # common corrections
            fixes = {
                'United States': 'USA',
                'United States of America': 'USA',
                'UK': 'GBR',
                'Russia': 'RUS',
                'South Korea': 'KOR',
                'North Korea': 'PRK',
                'Iran': 'IRN'
            }
            if name in fixes:
                return fixes[name]
            return None

    return country_series.map(to_iso3)


def main():
    st.title("Cyber Attacks Dashboard")
    st.write(
        "Carregue o CSV dos ataques (ex: dataset do Kaggle) para explorar dados de 2015-2024.")

    df = load_dataset()
    if df is None:
        return

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]

    # Guess useful column names
    country_col = None
    year_col = None
    attack_col = None
    for c in df.columns:
        lc = c.lower()
        if 'country' in lc:
            country_col = c
        if 'year' in lc:
            year_col = c
        if 'attack' in lc or 'type' in lc or 'threat' in lc:
            attack_col = c

    # Sidebar filters
    st.sidebar.header("Filtros")
    if year_col and year_col in df.columns:
        years = sorted(df[year_col].dropna().unique().tolist())
        selected_years = st.sidebar.multiselect("Ano", years, default=years)
        df = df[df[year_col].isin(selected_years)]
    if country_col and country_col in df.columns:
        countries = sorted(df[country_col].dropna().unique().tolist())
        selected_countries = st.sidebar.multiselect(
            "País", countries, default=None)
        if selected_countries:
            df = df[df[country_col].isin(selected_countries)]
    if attack_col and attack_col in df.columns:
        attacks = sorted(df[attack_col].dropna().unique().tolist())
        selected_attacks = st.sidebar.multiselect(
            "Tipo de ataque", attacks, default=None)
        if selected_attacks:
            df = df[df[attack_col].isin(selected_attacks)]

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de registros", len(df))
    with col2:
        if country_col:
            st.metric("Países únicos", int(df[country_col].nunique()))
        else:
            st.metric("Países únicos", "N/A")
    with col3:
        if attack_col and attack_col in df.columns:
            top_attack = df[attack_col].value_counts().idxmax()
            st.metric("Tipo mais comum", str(top_attack))
        else:
            st.metric("Tipo mais comum", "N/A")
    with col4:
        if year_col and year_col in df.columns:
            years_count = df[year_col].nunique()
            st.metric("Anos presentes", int(years_count))
        else:
            st.metric("Anos presentes", "N/A")

    st.markdown("---")

    # Table
    st.subheader("Tabela de registros")
    st.dataframe(df.head(500))

    # Chart 1: ataques por ano
    if year_col and year_col in df.columns:
        attacks_by_year = df.groupby(year_col).size().reset_index(name='count')
        fig1 = px.bar(attacks_by_year, x=year_col,
                      y='count', title='Ataques por Ano')
        st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: top países
    if country_col and country_col in df.columns:
        attacks_by_country = df.groupby(country_col).size().reset_index(
            name='count').sort_values('count', ascending=False)
        fig2 = px.bar(attacks_by_country.head(15), x='count', y=country_col,
                      orientation='h', title='Top 15 Países por Número de Ataques')
        st.plotly_chart(fig2, use_container_width=True)

        # Map choropleth
        st.subheader("Mapa Mundial: ataques por país")
        iso_series = map_countries_to_iso3(attacks_by_country[country_col])
        map_df = attacks_by_country.copy()
        map_df['iso_alpha'] = iso_series.values
        map_df = map_df.dropna(subset=['iso_alpha'])
        if not map_df.empty:
            fig_map = px.choropleth(map_df, locations='iso_alpha', color='count',
                                    hover_name=country_col, color_continuous_scale='OrRd', title='Ataques por País')
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info(
                'Não foi possível mapear países para códigos ISO3. Instale `pycountry` para habilitar o mapa.')


if __name__ == '__main__':
    main()
