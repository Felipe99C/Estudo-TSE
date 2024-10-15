#%%
import streamlit as st
import pandas as pd
import sqlalchemy
from utils import make_scatter

engine = sqlalchemy.create_engine("sqlite:///E:/Estudos/Ciência de dados/Projetos/TSE_2024/Estudo-TSE/Data/database.db")\

with open("partidos2.sql", "r") as open_file:
    query = open_file.read()

df = pd.read_sql(query, engine)
df.head()

#%%


welcome = """
# TSE Analytics - Eleições 2024

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


# Filtrando os dados pelo estado selecionado
data = df[df['SG_UF'] == estado]

fig = make_scatter(data, size=size, cluster=cluster)

st.pyplot(fig)
