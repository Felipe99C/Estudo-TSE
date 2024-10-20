
#%%
import matplotlib.pyplot as plt        # Criação de gráficos
import seaborn as sn                   # Visualização de dados
from matplotlib.offsetbox import OffsetImage, AnnotationBbox  # Adicionar imagens e textos em posições customizadas nos gráficos
from adjustText import adjust_text      # Ajuste automático da posição de textos nos gráficos
from sklearn import cluster
from sklearn import preprocessing
from matplotlib.ticker import PercentFormatter  # Para formatar os eixos em porcentagem

def make_scatter(data, x , y, x_label, y_label, cluster=False, size=False):

    config = {
        "data":data,
        "x":x,
        "y":y,
        "size":"total_candidaturas", # Tamanho das bolhas representa o total de candidaturas
        "sizes":(5,300),
        "hue":"cluster",
        "palette":'viridis',
        "alpha":0.6,
    }

    if not cluster:
        del config['hue']
        del config['palette']
    
    if not size:
        del config['size']
        del config['sizes']

    # Criando gráfico de dispersão com os clusters
    fig, ax = plt.subplots(dpi=360, figsize=(6,5.5))
    #fig = plt.figure(dpi=360, figsize=(6,5.5))

    #calculando as taxas gerais
    #tx_cor_raca_nao_branca = data["total_cor_raca_nao_branca"].sum() / data["total_candidaturas"].sum() # Taxa de pessoas não brancas
    #tx_cor_raca_preta_parda = data["total_cor_raca_preta_parda"].sum() / data["total_candidaturas"].sum() # Taxa de pessoas pretas ou pardas

    sn.scatterplot(**config)


    # Adicionando textos de novo
    texts = []
    for i in data['SG_PARTIDO']:
        data_tmp = data[data['SG_PARTIDO'] == i]
        x_pos = data_tmp[x].values[0]
        y_pos = data_tmp[y].values[0]
        texts.append(plt.text(x_pos, y_pos, i, fontsize=9))

    adjust_text(texts,
                force_points=0.0002,
                force_text=0.4,
                expand_points=(0.5, 0.75), expand_text=(0.5, 0.75),
                arrowprops=dict(arrowstyle="-", color='black', lw=0.2),
                pull_threshold=1000,
                )

    plt.grid(True)
    plt.suptitle(f"Partidos: {x_label.title()} VS {y_label.title()} - Eleições 2024")

    if size:
        plt.title("Maior a bolha, maior o tamanho do partido", fontdict={"size":9})

    plt.xlabel(x_label.title())
    plt.ylabel(y_label.title())

     # Formatando os eixos em porcentagem
    #ax.xaxis.set_major_formatter(PercentFormatter(1))  # 1 significa que os valores são de 0 a 1
    #ax.yaxis.set_major_formatter(PercentFormatter(1))

    if x == 'tx_gen_feminino' and y == 'tx_cor_raca_preta':
        tx_gen_feminino = data["total_gen_feminino"].sum() / data["total_candidaturas"].sum() # Taxa de candidaturas femininas
        tx_cor_raca_preta = data["total_cor_raca_preta"].sum() / data["total_candidaturas"].sum() # Taxa de pessoas pretas

        # Linhas de referência

        plt.hlines(y=tx_cor_raca_preta,
                   xmin=data["tx_gen_feminino"].min(),
                   xmax=data["tx_gen_feminino"].max(),
                   colors='black', alpha=0.6, linestyles='--', label=f"Pessoas Pretas Geral: {100*tx_cor_raca_preta:.0f}%")

        plt.vlines(x=tx_gen_feminino,
                   ymin=data["tx_cor_raca_preta"].min(),
                   ymax=data["tx_cor_raca_preta"].max(),
                   colors='tomato', alpha=0.6, linestyles='--', label=f"Mulheres Geral: {100*tx_gen_feminino:.0f}%")

        handles, labels = plt.gca().get_legend_handles_labels()
        handles = handles[-2:]
        labels = labels[-2:]

        # Exibindo a legenda e adicionando o logo
        plt.legend(handles=handles, labels=labels)
    else:
        legend = plt.legend()
        legend.remove()    

    return fig

def make_clusters(data, features, n=6):
    norm = preprocessing.MinMaxScaler()
    data_norm = norm.fit_transform(data[features])
    model = cluster.KMeans(n_clusters=n, random_state=42, max_iter=10000)
    model.fit(data_norm)
    data["cluster"] = model.labels_
    return data
