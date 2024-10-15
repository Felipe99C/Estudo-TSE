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
with open("partidos2.sql", "r") as open_file:
    query = open_file.read()

# Conexão com o SQLite
engine = sqlalchemy.create_engine("sqlite:///E:/Estudos/Ciência de dados/Projetos/TSE_2024/Estudo-TSE/Data/database.db")

# Executando a query SQL e armazenando o resultado em um DataFrame
df = pd.read_sql_query(query, engine)

df.head()  # Exibindo as primeiras linhas da tabela para verificar os dados
#%%
# 
df.columns
#%%
tx_cor_raca_nao_branca = df["total_cor_raca_nao_branca"].sum() / df["total_candidaturas"].sum() # Taxa de pessoas não brancas
tx_gen_feminino = df["total_gen_feminino"].sum() / df["total_candidaturas"].sum() # Taxa de candidaturas femininas
tx_cor_raca_preta_parda = df["total_cor_raca_preta_parda"].sum() / df["total_candidaturas"].sum() # Taxa de pessoas pretas ou pardas
tx_cor_raca_preta = df["total_cor_raca_preta"].sum() / df["total_candidaturas"].sum() # Taxa de pessoas pretas

#%%

# Grafico 1 analisando a tx de mulheres e pessoas pretas por partido

plt.figure(dpi=500)

# Quadrante dos partidos que possuem pessoas negras e mulheres
sn.scatterplot(data=df,
               x="tx_feminino_BR",  # Eixo X: Taxa de mulheres por partido
               y="tx_cor_raca_preta_BR",  # Eixo Y: Taxa de pessoas pretas por partido
               )

# Adicionando textos ao gráfico, identificando os partidos
texts = []
for i in df["SG_PARTIDO"]:
    data =df[df["SG_PARTIDO"]==i]
    x = data["tx_feminino_BR"].values[0]
    y = data["tx_cor_raca_preta_BR"].values[0]
    texts.append(plt.text(x,y,i,fontsize=9))

# Ajustando as posições dos textos para evitar sobreposição
adjust_text(texts,
            force_points=0.0002,
            force_text=0.4,
            expand_points=(0.5, 0.75), expand_text=(0.5, 0.75),
            arrowprops=dict(arrowstyle="-", color='black', lw=0.2),
            pull_threshold=1000,
            )

plt.grid(True)
plt.title("Partidos: Cor vs Genero - Eleições 2024")  # Título do gráfico
plt.xlabel("Taxa de Mulheres")  # Rótulo do eixo X
plt.ylabel("Taxa de Pessoas Pretas")  # Rótulo do eixo Y


# Adicionando linhas de referência para as taxas gerais de pessoas pretas e mulheres
plt.hlines(y=tx_cor_raca_preta, xmin=0.3, xmax=0.60, colors='black', alpha=0.6, linestyles='--', label=f"Pessoas Pretas Geral: {100*tx_cor_raca_preta:.0f}%")
plt.vlines(x=tx_gen_feminino, ymin=0.05, ymax=0.35, colors='tomato', alpha=0.6, linestyles='--', label=f"Mulheres Geral: {100*tx_gen_feminino:.0f}%")


plt.legend() #plota a legenda do gráfico

plt.savefig("../img/partidos_cor_raca_genero_1.png")

#%%

########################################## Grafico com as bolhas representando o tamanho dos partidos ###########################################################

# Repetindo o processo, agora com tamanho das bolhas representando o total de candidaturas
plt.figure(dpi=360, figsize=(6,5.5))

sn.scatterplot(data=df,
               x="tx_feminino_BR",
               y="tx_cor_raca_preta_BR",
               size="total_candidaturas", # Tamanho das bolhas representa o total de candidaturas
               sizes=(5,300)
)

# Adicionando textos de novo
texts = []
for i in df['SG_PARTIDO']:
    data = df[df['SG_PARTIDO'] == i]
    x = data['tx_feminino_BR'].values[0]
    y = data['tx_cor_raca_preta_BR'].values[0]
    texts.append(plt.text(x, y, i, fontsize=9))

adjust_text(texts,
            force_points=0.0002,
            force_text=0.4,
            expand_points=(0.5, 0.75), expand_text=(0.5, 0.75),
            arrowprops=dict(arrowstyle="-", color='black', lw=0.2),
            pull_threshold=1000,
            )

plt.grid(True)
plt.title("Partidos: Cor vs Genero - Eleições 2024")
plt.xlabel("Taxa de Mulheres")
plt.ylabel("Taxa de Pessoas Pretas")

# Linhas de referência de novo
plt.hlines(y=tx_cor_raca_preta, xmin=0.3, xmax=0.55, colors='black', alpha=0.6, linestyles='--', label=f"Pessoas Pretas Geral: {100*tx_cor_raca_preta:.0f}%")
plt.vlines(x=tx_gen_feminino, ymin=0.05, ymax=0.35, colors='tomato', alpha=0.6, linestyles='--', label=f"Mulheres Geral: {100*tx_gen_feminino:.0f}%")

handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[5:]
labels = labels[5:]

# retira da legenda o tamanho das bolhas
plt.legend(handles=handles, labels=labels)

# Salvando outro gráfico
plt.savefig("../img/partidos_cor_raca_genero_bolha_size.png")

#%%
########################################### Grafico agrupado por cores ###############################################################################
 
# Aplicando um modelo de clustering para agrupar partidos com base nas taxas de gênero e raça
from sklearn import cluster

X = df[["tx_feminino_BR","tx_cor_raca_preta_BR"]]

model = cluster.KMeans(n_clusters=6)  # KMeans para agrupar os partidos em 6 clusters
model.fit(X)

df["clusterBR"] = model.labels_  # Adiciona a coluna com os rótulos dos clusters


#df.groupby(["clusterBR"])["tx_feminino_BR"].count()

#%%

# Criando gráfico de dispersão com os clusters
plt.figure(dpi=360, figsize=(6,5.5))

sn.scatterplot(data=df,
               x="tx_feminino_BR",
               y="tx_cor_raca_preta_BR",
               size="total_candidaturas", # Tamanho das bolhas representa o total de candidaturas
               sizes=(5,300),
               hue="clusterBR",
               palette='viridis'
)

# Adicionando textos de novo
texts = []
for i in df['SG_PARTIDO']:
    data = df[df['SG_PARTIDO'] == i]
    x = data['tx_feminino_BR'].values[0]
    y = data['tx_cor_raca_preta_BR'].values[0]
    texts.append(plt.text(x, y, i, fontsize=9))

adjust_text(texts,
            force_points=0.0002,
            force_text=0.4,
            expand_points=(0.5, 0.75), expand_text=(0.5, 0.75),
            arrowprops=dict(arrowstyle="-", color='black', lw=0.2),
            pull_threshold=1000,
            )

plt.grid(True)
plt.title("Partidos: Cor vs Genero - Eleições 2024")
plt.xlabel("Taxa de Mulheres")
plt.ylabel("Taxa de Pessoas Pretas")

# Linhas de referência de novo
plt.hlines(y=tx_cor_raca_preta, xmin=0.3, xmax=0.55, colors='black', alpha=0.6, linestyles='--', label=f"Pessoas Pretas Geral: {100*tx_cor_raca_preta:.0f}%")
plt.vlines(x=tx_gen_feminino, ymin=0.05, ymax=0.35, colors='tomato', alpha=0.6, linestyles='--', label=f"Mulheres Geral: {100*tx_gen_feminino:.0f}%")

handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[13:]
labels = labels[13:]

# Exibindo a legenda e adicionando o logo
plt.legend(handles=handles, labels=labels)
#plt.legend()

plt.savefig("../img/partidos_cor_raca_genero_cluster.png")


