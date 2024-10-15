#%%
import streamlit as st
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt        # Criação de gráficos
import matplotlib.image as img         # Manipulação de imagens
import seaborn as sn                   # Visualização de dados
from matplotlib.offsetbox import OffsetImage, AnnotationBbox  # Adicionar imagens e textos em posições customizadas nos gráficos
from adjustText import adjust_text      # Ajuste automático da posição de textos nos gráficos
from sklearn import cluster


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
estado = st.selectbox(label="Estado", placeholder="Selecione o estado para o filtro", options=uf_options)

# Filtrando os dados pelo estado selecionado
data = df[df['SG_UF'] == estado]

#st.dataframe(data)

# Configuração do gráfico
#fig, ax = plt.subplots(dpi=360, figsize=(6,5.5))


# Criando gráfico de dispersão com os clusters
fig = plt.figure(dpi=360, figsize=(6,5.5))

#calculando as taxas gerais
#tx_cor_raca_nao_branca = data["total_cor_raca_nao_branca"].sum() / data["total_candidaturas"].sum() # Taxa de pessoas não brancas
#tx_cor_raca_preta_parda = data["total_cor_raca_preta_parda"].sum() / data["total_candidaturas"].sum() # Taxa de pessoas pretas ou pardas



sn.scatterplot(data=data,
               x="tx_gen_feminino",
               y="tx_cor_raca_preta",
               size="total_candidaturas", # Tamanho das bolhas representa o total de candidaturas
               sizes=(5,300),
               #hue="clusterBR",
               #palette='viridis',
               alpha=0.6,
)

# Adicionando textos de novo
texts = []
for i in data['SG_PARTIDO']:
    data_tmp = data[data['SG_PARTIDO'] == i]
    x = data_tmp['tx_gen_feminino'].values[0]
    y = data_tmp['tx_cor_raca_preta'].values[0]
    texts.append(plt.text(x, y, i, fontsize=9))

adjust_text(texts,
            force_points=0.0002,
            force_text=0.4,
            expand_points=(0.5, 0.75), expand_text=(0.5, 0.75),
            arrowprops=dict(arrowstyle="-", color='black', lw=0.2),
            pull_threshold=1000,
            )

plt.grid(True)
plt.suptitle("Partidos: Cor vs Genero - Eleições 2024")
plt.title("Maior a bolha, maior o tamanho do partido", fontdict={"size":9})
plt.xlabel("Taxa de Mulheres")
plt.ylabel("Taxa de Pessoas Pretas")

tx_gen_feminino = data["total_gen_feminino"].sum() / data["total_candidaturas"].sum() # Taxa de candidaturas femininas
tx_cor_raca_preta = data["total_cor_raca_preta"].sum() / data["total_candidaturas"].sum() # Taxa de pessoas pretas

# Linhas de referência de novo
plt.hlines(y=tx_cor_raca_preta, xmin=0.3, xmax=0.55, colors='black', alpha=0.6, linestyles='--', label=f"Pessoas Pretas Geral: {100*tx_cor_raca_preta:.0f}%")
plt.vlines(x=tx_gen_feminino, ymin=0.05, ymax=0.35, colors='tomato', alpha=0.6, linestyles='--', label=f"Mulheres Geral: {100*tx_gen_feminino:.0f}%")

handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[-2:]
labels = labels[-2:]

# Exibindo a legenda e adicionando o logo
plt.legend(handles=handles, labels=labels)
st.pyplot(fig)


#####################################################################






#
#
#n.scatterplot(data = data,
#              x="tx_gen_feminino",
#              y="tx_cor_raca_preta",
#              size="total_candidaturas",
#              sizes=(5,300),
#              #hue="clusterBR",
#              #palette='viridis',
#              alpha=0.6,
#              ax=ax                    
#
#
# Limitar o número de textos para ajustar
#ax_texts = 200 # Defina o limite de textos, aqui 100 por exemplo
#
#
# Adicionando textos de novo
#exts = []
#or i in df['SG_PARTIDO'].head(max_texts):
#   data = df[df['SG_PARTIDO'] == i]
#   x = data['tx_gen_feminino'].values[0]
#   y = data['tx_cor_raca_preta'].values[0]
#   texts.append(plt.text(x, y, i, fontsize=9))
#
# Ajuste de texto para evitar sobreposição
#djust_text(texts,
#           force_points=0.0002,
#           force_text=0.4,
#           expand_points=(0.5, 0.75),
#           expand_text=(0.5, 0.75),
#           arrowprops=dict(arrowstyle="-",
#           color='black', lw=0.2),
#           pull_threshold=1000,
#
#
#calculando as taxas gerais
#x_cor_raca_nao_branca = data["total_cor_raca_nao_branca"].sum() / data["total_candidaturas"].sum() # Taxa de pessoas não brancas
#x_gen_feminino = data["total_gen_feminino"].sum() / data["total_candidaturas"].sum() # Taxa de candidaturas femininas
#x_cor_raca_preta_parda = data["total_cor_raca_preta_parda"].sum() / data["total_candidaturas"].sum() # Taxa de pessoas pretas ou pardas
#x_cor_raca_preta = data["total_cor_raca_preta"].sum() / data["total_candidaturas"].sum() # Taxa de pessoas pretas
#
# Linhas de referência
#lt.vlines(x=tx_gen_feminino, ymin=0.05, ymax=0.35, colors='tomato', alpha=0.6, linestyles='--', label=f"Mulheres Geral: {100*tx_gen_feminino:.0f}%")
#lt.hlines(y=tx_cor_raca_preta, xmin=0.3, xmax=0.55, colors='black', alpha=0.6, linestyles='--', label=f"Pessoas Pretas Geral: {100*tx_cor_raca_preta:.0f}%")
#
# Ajuste da legenda
#andles, labels = ax.get_legend_handles_labels()
#x.legend(handles=handles[2:], labels=labels[2:])
#
#handles, labels = plt.gca().get_legend_handles_labels()
#handles = handles[13:]
#labels = labels[13:]
#
#plt.grid(True)
#plt.title("Partidos: Cor vs Genero - Eleições 2024")
#plt.xlabel("Taxa de Mulheres")
#plt.ylabel("Taxa de Pessoas Pretas")
#
# Exibindo a legenda e adicionando o logo
#plt.legend(handles=handles, labels=labels)
#t.pyplot(fig)
#
#
#
#