#%%
import streamlit as st
import pandas as pd
import sqlalchemy
from utils import make_scatter, make_clusters
import os
import gdown

prepare_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(prepare_path)
base_path = os.path.dirname(src_path)
data_path = os.path.join(base_path, "Data")

#Link para baixar os arquivos fontes
#@st.cache_data(ttl=60*60*24) #define o tamando do cache para 1 dia (60 segundos * 60 * 24 = 1 dia)
#def download_db():
#    url_database = "https://drive.google.com/uc?id=1lXM0kZqa7AARTW9VS9q0FF9Kcn3N_f5R"
#    gdown.download(url_database, database_path,quiet=False)

#deixa o database e as querys em cache por 24h
#@st.cache_data(ttl=60*60*24) #define o tamando do cache para 1 dia (60 segundos * 60 * 24 = 1 dia)
def create_df():
    filename = os.path.join(data_path, "data_partidos.parquet")
    return pd.read_parquet(filename)
    

#%%

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

cargos_opt = df["DS_CARGO"].unique().tolist()
cargos_opt.sort()
cargos_opt.remove("GERAL")
cargos_opt = ["GERAL"] + cargos_opt # dessa forma garante que o BR será a primeira opção

col1, col2 = st.columns(2)

print(uf_options)

# cria um select box com os estados e passa o valor selecionado para o filtrado mais abaixo


with col1:
    estado = st.selectbox(label="Estado", placeholder="Selecione o estado para o filtro", options=uf_options)
    size = st.checkbox("Tamando das Bolhas")
    cluster = st.checkbox("Definir Cluster")

with col2:
    cargo = st.selectbox(label="Cargo", placeholder="Selecione o cargo para filtro", options=cargos_opt)
    st.markdown('')
    n_cluster = st.number_input("Quantidade de cluster", value=6, format="%d", max_value=10, min_value=1)

# Filtrando os dados pelo estado selecionado
data = df[(df['SG_UF']==estado) & (df['DS_CARGO']==cargo)].copy()

total_candidatos = int(data["total_candidaturas"].sum())
st.markdown(f"Total de Candidaturas: {total_candidatos}")

if cluster:
    data = make_clusters(data, n_cluster)

fig = make_scatter(data, size=size, cluster=cluster)

st.pyplot(fig)
