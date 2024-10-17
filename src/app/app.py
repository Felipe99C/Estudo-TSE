#%%
import streamlit as st
import pandas as pd
import sqlalchemy
from utils import make_scatter, make_clusters
import os
import gdown

#  insere os caminhos dos diretórios e pastas
#  para o streamlit conseguir acessar o database mais fácil

app_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(app_path)
base_path = os.path.dirname(src_path)
data_path = os.path.join(base_path, "Data")

database_path = os.path.join(data_path,"database_gd.db")
engine = sqlalchemy.create_engine(f"sqlite:///{database_path}")

#Link para baixar os arquivos fontes
@st.cache_data(ttl=60*60*24) #define o tamando do cache para 1 dia (60 segundos * 60 * 24 = 1 dia)
def download_db():
    url_database = "https://drive.google.com/uc?id=1lXM0kZqa7AARTW9VS9q0FF9Kcn3N_f5R"
    gdown.download(url_database, database_path,quiet=False)

#deixa o database e as querys em cache por 24h
@st.cache_data(ttl=60*60*24) #define o tamando do cache para 1 dia (60 segundos * 60 * 24 = 1 dia)
def create_df():
    query_path = os.path.join(app_path, "partidos2.sql")
    with open(query_path, "r") as open_file:
            query = open_file.read()
    
    return pd.read_sql(query, engine)

#%%

download_db()

df = create_df()

welcome = """
# TSE Analytics - Eleições 2024

Acompanhando a iniciativa Téo me Why em conjunto com a comunidade visando aprender mais sobre análise de dados e ciência de dados.

Como Primeira análise dos partidos, foi focado a questão da diversidade de mulheres e pessoas pretas nas candidaturas de 2024.

"""

st.markdown(welcome)

uf_options = df["SG_UF"].unique().tolist()
uf_options.sort()
uf_options.remove("BR")
uf_options = ["BR"] + uf_options # dessa forma garante que o BR será a primeira opção

# cria um select box com os estados e passa o valor selecionado para o filtrado mais abaixo
estado = st.sidebar.selectbox(label="Estado", placeholder="Selecione o estado para o filtro", options=uf_options)
size = st.sidebar.checkbox("Tamando das Bolhas")
cluster = st.sidebar.checkbox("Definir Cluster")
n_cluster = st.sidebar.number_input("Quantidade de cluster", value=6, format="%d", max_value=10, min_value=1)


# Filtrando os dados pelo estado selecionado
data = df[df['SG_UF'] == estado]

if cluster:
    data = make_clusters(data, n_cluster)

fig = make_scatter(data, size=size, cluster=cluster)

st.pyplot(fig)
