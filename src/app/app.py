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

features_map = {
    "PERCENTUAL FEMININO": "tx_gen_feminino",
    "PERCENTUAL RACA PRETA": "tx_cor_raca_preta",
    "PERCENTUAL RACA PRETA PARDA": "tx_cor_raca_preta_parda",
    "PERCENTUAL RACA NÃO-BRANCA": "tx_cor_raca_nao_branca",
    "MEDIA BENS TOTAL":"avgBens",
    "MEDIA BENS SEM ZEROS (por mil)": "avgBensNotZero",
    "PERCENTUAL ESTADO CIVIL CASADO(A)": "txEstadoCivilCasado",
    "PERCENTUAL ESTADO CIVIL SOLTEIRO(A)": "txEstadoCivilSolteiro",
    "PERCENTUAL ESTADO CIVIL DIVORCIADO(A)": "txEstadoCivilSeparadodivorciado",
    "MÉDIA IDADE": "avgIdade",
}

features_options = list(features_map.keys())
features_options.sort()

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


# Definição dos estados
col1, col2, = st.columns(2)
# cria um select box com os estados e passa o valor selecionado para o filtrado mais abaixo
with col1:
    estado = st.selectbox(label="Estado", placeholder="Selecione o estado para o filtro", options=uf_options)

with col2:
    cargo = st.selectbox(label="Cargo", placeholder="Selecione o cargo para filtro", options=cargos_opt)

# Definição dos eixos
col1, col2, = st.columns(2)
with col1:
    x_option= st.selectbox(label='Eixo x', options=features_options,index = features_options.index("PERCENTUAL FEMININO"))
    x = features_map[x_option]
    new_features_options = features_options.copy()
    new_features_options.remove(x_option)

with col2:
    #features_options.remove(x_option)
    default_y_option = "PERCENTUAL RACA PRETA" if "PERCENTUAL RACA PRETA" in new_features_options else new_features_options[0]
    y_option = st.selectbox(label='Eixo y', options=new_features_options,index=new_features_options.index("PERCENTUAL RACA PRETA"))
    y = features_map[y_option]

size = st.checkbox("Tamando das Bolhas")

# Definição do uso dos cluster
col1, col2, = st.columns(2)
with col1:
    cluster = st.checkbox("Definir Cluster")
    if cluster:
        n_cluster = st.number_input("Quantidade de cluster", value=6, format="%d", max_value=10, min_value=1)

with col2:
    if cluster:
        features_options_select = st.multiselect(label='Variaveis para agrupamento',
                                                 options=features_options,
                                                 default=["PERCENTUAL FEMININO", "PERCENTUAL RACA PRETA"])
        features_select = [features_map[i] for i in features_options_select]

# Filtrando os dados pelo estado selecionado
data = df[(df['SG_UF']==estado) & (df['DS_CARGO']==cargo)].copy()

total_candidatos = int(data["total_candidaturas"].sum())
st.markdown(f"Total de Candidaturas: {total_candidatos}")

if cluster:
    data = make_clusters(data = data, features=features_select, n=n_cluster)

fig = make_scatter(data,
                   x=x , y=y, 
                   x_label=x_option,
                   y_label=y_option,
                   size=size,
                   cluster=cluster)

st.pyplot(fig)
