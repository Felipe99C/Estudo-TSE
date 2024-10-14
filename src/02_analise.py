#%%

# Importando bibliotecas necessárias
import os
import pandas as pd                   # Manipulação de dados
import sqlalchemy                      # Conexão com banco de dados
import matplotlib.pyplot as plt        # Criação de gráficos
import matplotlib.image as img         # Manipulação de imagens
import seaborn as sn                   # Visualização de dados
from matplotlib.offsetbox import OffsetImage, AnnotationBbox  # Adicionar imagens e textos em posições customizadas nos gráficos
from adjustText import adjust_text      # Ajuste automático da posição de textos nos gráficos
from sklearn import cluster

#%%

# Lendo uma query SQL de um arquivo
with open("partidos1.sql", "r") as open_file:
    query = open_file.read()

# Conexão com o SQLite
engine = sqlalchemy.create_engine("sqlite:///E:/Estudos/Ciência de dados/Projetos/TSE_2024/Estudo-TSE/Data/database.db")

# Executando a query SQL e armazenando o resultado em um DataFrame
df = pd.read_sql_query(query, engine)

df.head()  # Exibindo as primeiras linhas da tabela para verificar os dados
#%%
# df.columns

tx_cor_raca_nao_branca = df["total_cor_raca_nao_branca"].sum() / df["total_candidaturas"].sum() # Taxa de pessoas não brancas
tx_gen_feminino = df["total_gen_feminino"].sum() / df["total_candidaturas"].sum() # Taxa de candidaturas femininas
tx_cor_raca_preta_parda = df["total_cor_raca_preta_parda"].sum() / df["total_candidaturas"].sum() # Taxa de pessoas pretas ou pardas
tx_cor_raca_preta = df["total_cor_raca_preta"].sum() / df["total_candidaturas"].sum() # Taxa de pessoas pretas

# Quadrante dos partidos que possuem pessoas negras e mulheres
sn.scatterplot(data=df,
               x="tx_gen_feminino",  # Eixo X: Taxa de mulheres por partido
               y="tx_cor_raca_preta",  # Eixo Y: Taxa de pessoas pretas por partido
               )

# Adicionando textos ao gráfico, identificando os partidos
texts = []
for i in df["SG_PARTIDO"]:
    data =df[df["SG_PARTIDO"]==i]
    x = data["tx_feminino_BR"].values[0]
    y = data["tx_cor_raca_preta_BR"].values[0]
    texts.append(plt.text(x,y,i,fontsize=9))

plt.grid(True)
plt.title("Partidos: Cor vs Genero - Eleições 2024")  # Título do gráfico
plt.xlabel("Taxa de Mulheres")  # Rótulo do eixo X
plt.ylabel("Taxa de Pessoas Pretas")  # Rótulo do eixo Y
