#%%
import os
import pandas as pd
import sqlalchemy
import json

#%%

# Conexão com o SQLite
engine = sqlalchemy.create_engine("sqlite:///E:/Estudos/Ciência de dados/Projetos/TSE_2024/Estudo-TSE/Data/database.db")

#copia os dados dos arquivos para a tabela 
with open("ingestoes.json","r") as open_file:
    ingestoes = json.load(open_file)

for i in ingestoes:
    path = i['path']
    df = pd.read_csv(path, encoding='latin-1', sep=';')
    # Renomeando as colunas para minúsculas
    # df.columns = df.columns.str.lower()
    # Exportando os dados para o banco de dados
    df.to_sql(i["table"], engine, if_exists="replace", index=False)