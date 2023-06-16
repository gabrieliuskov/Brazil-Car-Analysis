import pandas as pd

# Import, filtro e padronização dado de dados
df = pd.read_csv("datasets/carros.csv")
df["brand"] = df.brand.apply(lambda x: x.title())
df["gear"] = df.gear.apply(lambda x: x.title())


# Variaveis auxiliares para criação de graficos e callbacks
marcas_data = df["brand"].sort_values().unique()
anos_data = df["year_of_reference"].sort_values().unique()
gear_data = df["gear"].sort_values().unique()
month_data = df.month_of_reference.unique()
engine_data = range(int(round(df.engine_size.min()-df.engine_size.min(),0)), int(round(df.engine_size.max(),0))+1,1)
maior_engine = max(engine_data)
values_engine = (min(engine_data), max(engine_data))
veiculo_anos_data = df.year_model.sort_values().unique()
mes_dashboard = {i: j for i, j in enumerate(month_data)}
mes_inverso = {j: i+1 for i, j in enumerate(month_data)}


# Exportação de dados para o dash
store_data = df.to_dict()
