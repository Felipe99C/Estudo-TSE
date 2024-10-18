#%%

import os
import sqlalchemy
import pandas as pd

#  insere os caminhos dos diretórios e pastas
#  para o streamlit conseguir acessar o database mais fácil

prepare_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(prepare_path)
base_path = os.path.dirname(src_path)
data_path = os.path.join(base_path, "Data")


database_path = os.path.join(data_path,"database_gd.db")
engine = sqlalchemy.create_engine(f"sqlite:///{database_path}")

print(database_path)
#%%

query_path = os.path.join(prepare_path, "partidos3.sql")
with open(query_path, "r") as open_file:
    query = open_file.read()
    
df = pd.read_sql(query, engine)

# Parquet é um formato de armazenamento de dados altamente eficiente,
# otimizado para leitura e gravação de grandes volumes de dados.

file_name = os.path.join(data_path, "data_partidos.parquet")
df.to_parquet(file_name, index=False) #