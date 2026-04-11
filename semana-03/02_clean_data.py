import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv('incidents_master.csv')

print("=" * 80)
print("LIMPEZA DO DATASET")
print("=" * 80)

# 1. Remover duplicados
initial_shape = df.shape
df.drop_duplicates(inplace=True)
print(f"Duplicados removidos: {initial_shape[0] - df.shape[0]} linhas")

# 2. Preencher valores nulos
# Para colunas numéricas, preencher com a mediana
numeric_cols = ['company_revenue_usd', 'employee_count', 'data_compromised_records', 'downtime_hours', 'quality_score']
for col in numeric_cols:
    if col in df.columns:
        median_val = df[col].median()
        df[col].fillna(median_val, inplace=True)
        print(f"Valores nulos em {col} preenchidos com mediana: {median_val}")

# Para colunas categóricas, preencher com 'Unknown'
categorical_cols = ['industry_secondary', 'attack_vector_secondary', 'attributed_group', 'data_source_secondary', 'notes']
for col in categorical_cols:
    if col in df.columns:
        df[col].fillna('Unknown', inplace=True)
        print(f"Valores nulos em {col} preenchidos com 'Unknown'")

# 3. Converter datas
date_cols = ['incident_date', 'discovery_date', 'disclosure_date', 'created_at', 'updated_at']
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        print(f"Coluna {col} convertida para datetime")

# 4. Remover dados inválidos
# Remover linhas com datas inválidas (NaT)
df.dropna(subset=date_cols, inplace=True)
print(f"Linhas com datas inválidas removidas após limpeza: {initial_shape[0] - df.shape[0]}")

# Remover valores negativos em colunas numéricas onde não fazem sentido
df = df[df['company_revenue_usd'] >= 0]
df = df[df['employee_count'] >= 0]
df = df[df['data_compromised_records'] >= 0]
df = df[df['downtime_hours'] >= 0]
df = df[df['quality_score'] >= 0]
print("Valores negativos removidos em colunas numéricas")

print(f"Dataset limpo: {df.shape[0]} linhas, {df.shape[1]} colunas")

# Salvar o dataset limpo
df.to_csv('incidents_master_cleaned.csv', index=False)
print("Dataset limpo salvo como 'incidents_master_cleaned.csv'")

print("\n" + "=" * 80)
print("PRIMEIRAS LINHAS DO DATASET LIMPO")
print("=" * 80)
print(df.head())