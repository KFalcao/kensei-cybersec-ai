import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Carregar os dados
df = pd.read_csv('incidents_master_cleaned.csv')

# Processar dados para gráficos

# 1. Gráfico de barras: Ataques por ano
df['incident_date'] = pd.to_datetime(df['incident_date'])
df['year'] = df['incident_date'].dt.year
attacks_per_year = df.groupby('year').size().reset_index(name='count')

fig1 = px.bar(attacks_per_year, x='year', y='count', title='Ataques por Ano',
              labels={'year': 'Ano', 'count': 'Número de Ataques'})

# 2. Gráfico de pizza: Tipo da empresa (pública/privada)
company_type_counts = df['is_public_company'].value_counts().reset_index()
company_type_counts.columns = ['is_public', 'count']
company_type_counts['type'] = company_type_counts['is_public'].map({True: 'Pública', False: 'Privada'})

fig2 = px.pie(company_type_counts, values='count', names='type', title='Tipo da Empresa')

# 3. Mapa: Ataques por país
country_counts = df['country_hq'].value_counts().reset_index()
country_counts.columns = ['country', 'count']

# Usar códigos ISO para países
country_codes = {
    'US': 'USA', 'CA': 'CAN', 'IL': 'ISR', 'NL': 'NLD', 'BR': 'BRA', 'GB': 'GBR', 'DE': 'DEU', 'FR': 'FRA',
    'AU': 'AUS', 'JP': 'JPN', 'CN': 'CHN', 'IN': 'IND', 'KR': 'KOR', 'SG': 'SGP', 'HK': 'HKG', 'TW': 'TWN'
}
country_counts['iso_alpha'] = country_counts['country'].map(country_codes)

fig3 = px.choropleth(country_counts, locations='iso_alpha', color='count',
                     hover_name='country', title='Ataques por País',
                     color_continuous_scale=px.colors.sequential.Plasma)

# Salvar cada gráfico em um arquivo HTML separado
fig1.write_html('ataques_por_ano.html')
fig2.write_html('tipo_empresa.html')
fig3.write_html('ataques_por_pais.html')

print("Gráficos salvos em arquivos HTML separados:")
print("- ataques_por_ano.html")
print("- tipo_empresa.html")
print("- ataques_por_pais.html")