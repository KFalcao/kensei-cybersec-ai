import pandas as pd

# Carregar o dataset limpo
df = pd.read_csv('incidents_master_cleaned.csv')

# Filtrar empresas privadas (is_public_company == False)
private_companies = df[df['is_public_company'] == False]

# Agrupar por país (country_hq) e contar o número de ataques (incidentes)
attacks_by_country = private_companies.groupby('country_hq').size().reset_index(name='num_attacks')

# Ordenar por número de ataques em ordem decrescente
attacks_by_country = attacks_by_country.sort_values(by='num_attacks', ascending=False)

# Mostrar top 10 países com mais ataques
top_10 = attacks_by_country.head(10)

print("=" * 80)
print("TOP 10 PAÍSES COM MAIS ATAQUES EM EMPRESAS PRIVADAS")
print("=" * 80)
print(top_10.to_string(index=False))