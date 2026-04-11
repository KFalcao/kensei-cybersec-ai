import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv('incidents_master.csv')

print("=" * 80)
print("PRIMEIRAS LINHAS DO DATASET")
print("=" * 80)
print(df.head())

print("\n" + "=" * 80)
print("INFORMAÇÕES DO DATASET")
print("=" * 80)
print(df.info())

print("\n" + "=" * 80)
print("ESTATÍSTICAS DO DATASET")
print("=" * 80)
print(df.describe())
