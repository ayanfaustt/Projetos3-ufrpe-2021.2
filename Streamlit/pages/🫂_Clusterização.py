from copyreg import constructor
from locale import normalize
from re import A
from click import style
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import StandardScaler

st.set_page_config(
    page_title="Clusterização",
    page_icon="🫂",
)

# def typeConversion(dataFrame):
#     unique_val = dataFrame["tipo"].unique()

#     type_iterator = list()
#     for type in unique_val:
#         if not ("~" in type):
#             type_iterator.append(type)

#     for i in range(len(dataFrame)):
#         type_aux = type_iterator[:]
#         if '~' in dataFrame.loc[i, 'tipo']:
#             pokemon_types = dataFrame.loc[i, 'tipo'].split('~')
#             dataFrame.loc[i, pokemon_types[0]] = int(1)
#             dataFrame.loc[i, pokemon_types[1]] = int(1)
#             type_aux.pop(type_aux.index(pokemon_types[0]))
#             type_aux.pop(type_aux.index(pokemon_types[1]))
#             for j in type_aux:
#                 dataFrame.loc[i, j] = int(0)
#         else:
#             mono_type = dataFrame.loc[i, 'tipo']
#             dataFrame.loc[i, mono_type] = int(1)
#             type_aux.pop(type_aux.index(mono_type))
#             for k in type_aux:
#                 dataFrame.loc[i, k] = int(0)

#     dataFrame.drop(['tipo'], axis=1, inplace=True)

#     return dataFrame


def typeConversion(dataFrame):
    unique_val = dataFrame["habilidades"].copy()

    type_iterator = list()
    for type in unique_val:
        habilidades = type.split('~')
        for habilidade in habilidades:
            if not (habilidade in type_iterator):
                type_iterator.append(habilidade)

    for i in range(len(dataFrame)):
        type_aux = type_iterator[:]
        if '~' in dataFrame.loc[i, 'habilidades']:
            pokemon_habilidades = dataFrame.loc[i, 'habilidades'].split('~')
            if len(pokemon_habilidades) == 3:
                dataFrame.loc[i, pokemon_habilidades[0]] = int(1)
                dataFrame.loc[i, pokemon_habilidades[1]] = int(1)
                dataFrame.loc[i, pokemon_habilidades[2]] = int(1)
                type_aux.pop(type_aux.index(pokemon_habilidades[0]))
                type_aux.pop(type_aux.index(pokemon_habilidades[1]))
                type_aux.pop(type_aux.index(pokemon_habilidades[2]))
            else:
                dataFrame.loc[i, pokemon_habilidades[0]] = int(1)
                dataFrame.loc[i, pokemon_habilidades[1]] = int(1)
                type_aux.pop(type_aux.index(pokemon_habilidades[0]))
                type_aux.pop(type_aux.index(pokemon_habilidades[1]))
            for j in type_aux:
                dataFrame.loc[i, j] = int(0)
        else:
            mono_habilidade = dataFrame.loc[i, 'habilidades']
            dataFrame.loc[i, mono_habilidade] = int(1)
            type_aux.pop(type_aux.index(mono_habilidade))
            for k in type_aux:
                dataFrame.loc[i, k] = int(0)

    dataFrame.drop(['habilidades'], axis=1, inplace=True)

    return dataFrame


# def colummConversion(dataFrame, col):
#     unique_val = dataFrame[col].unique()
#     ds_aux = pd.DataFrame(columns=unique_val)
#     var_iterator = [itemlist for itemlist in unique_val]
#     for index in range(len(dataFrame)):
#         dataAux = list()
#         current_val = dataFrame.loc[index, col]
#         for index_i in var_iterator:
#           if current_val == index_i:
#             dataAux.append(1)
#           else:
#             dataAux.append(0)
#         ds_aux.loc[index] = dataAux

#     new_dataFrame = pd.concat([dataFrame, ds_aux], axis= 1)
#     new_dataFrame.drop([col], axis=1, inplace=True)
#     return new_dataFrame

def colummConversion(dataFrame, col):

    unique_val = dataFrame[col].unique()

    var_iterator = [itemlist for itemlist in unique_val]
    for index in range(len(dataFrame)):
        varIterator_aux = var_iterator[:]
        current_val = dataFrame.loc[index, col]
        dataFrame.loc[index, current_val] = 1
        varIterator_aux.pop(varIterator_aux.index(current_val))
        for index_i in varIterator_aux:
            dataFrame.loc[index, index_i] = 0

    dataFrame.drop([col], axis=1, inplace=True)

    return dataFrame


def main():
    path_to_dataset = os.path.join(os.getcwd(), os.pardir)+"/pokemon.parquet"
    # Dataset completo
    ds = pd.read_parquet(path_to_dataset)
    colunas = ['nome',
               'n_pokedex',
               'habilidades',
               'tipo',
               'vida',
               'ataque',
               'defesa',
               'ataque_especial',
               'defesa_especial',
               'velocidade',
               'altura',
               'peso',
               'genero',
               'geracao',
               'taxa_de_femeas',
               'sem_genero',
               'bebe_pokemon',
               'lendario',
               'mitico',
               'padrao',
               'forma_temporaria',
               'xp_basico',
               'taxa_de_captura',
               'grupo_de_ovo',
               'ciclo_de_ovo',
               'felicidade_base',
               'evoluivel',
               'evolui_de',
               'cor_primaria',
               'forma',
               'total_pokemons_do_mesmo_tipo',
               'vulnerabilidade_normal',
               'vulnerabilidade_fogo',
               'vulnerabilidade_agua',
               'vulnerabilidade_eletrico',
               'vulnerabilidade_planta',
               'vulnerabilidade_gelo',
               'vulnerabilidade_lutador',
               'vulnerabilidade_venenoso',
               'vulnerabilidade_terrestre',
               'vulnerabilidade_voador',
               'vulnerabilidade_pisiquico',
               'vulnerabilidade_inseto',
               'vulnerabilidade_pedra',
               'vulnerabilidade_fantasma',
               'vulnerabilidade_dragao',
               'vulnerabilidade_sombrio',
               'vulnerabilidade_aco',
               'vulnerabilidade_fada']
    ds.columns = colunas
    st.header("Clusterização")
    st.write(
        "Foram criados 2 clusters experimentais baseados nas propostas do nosso projeto.")
    st.write("Para ambos foi usado o algoritmo K-means.")
    st.subheader("Cluster 1")
    st.write(
        "Este cluster foi criado utilizando a maioria das colunas do dataset, sendo elas: ")
    colunas_cluster_all = ['tipo',
                           'vida',
                           'ataque',
                           'defesa',
                           'ataque_especial',
                           'defesa_especial',
                           'velocidade',
                           'altura',
                           'peso',
                           'genero',
                           'geracao',
                           'taxa_de_femeas',
                           'sem_genero',
                           'bebe_pokemon',
                           'lendario',
                           'mitico',
                           'padrao',
                           'forma_temporaria',
                           'xp_basico',
                           'taxa_de_captura',
                           'grupo_de_ovo',
                           'ciclo_de_ovo',
                           'felicidade_base',
                           'evoluivel',
                           'cor_primaria',
                           'forma',
                           'total_pokemons_do_mesmo_tipo',
                           'vulnerabilidade_normal',
                           'vulnerabilidade_fogo',
                           'vulnerabilidade_agua',
                           'vulnerabilidade_eletrico',
                           'vulnerabilidade_planta',
                           'vulnerabilidade_gelo',
                           'vulnerabilidade_lutador',
                           'vulnerabilidade_venenoso',
                           'vulnerabilidade_terrestre',
                           'vulnerabilidade_voador',
                           'vulnerabilidade_pisiquico',
                           'vulnerabilidade_inseto',
                           'vulnerabilidade_pedra',
                           'vulnerabilidade_fantasma',
                           'vulnerabilidade_dragao',
                           'vulnerabilidade_sombrio',
                           'vulnerabilidade_aco',
                           'vulnerabilidade_fada']
    colunas_quantitativas_ordinais = ['vida',
                                      'ataque',
                                      'defesa',
                                      'ataque_especial',
                                      'defesa_especial',
                                      'velocidade',
                                      'altura',
                                      'peso',
                                      'taxa_de_femeas',
                                      'xp_basico',
                                      'taxa_de_captura',
                                      'ciclo_de_ovo',
                                      'felicidade_base',
                                      'total_pokemons_do_mesmo_tipo',
                                      'vulnerabilidade_normal',
                                      'vulnerabilidade_fogo',
                                      'vulnerabilidade_agua',
                                      'vulnerabilidade_eletrico',
                                      'vulnerabilidade_planta',
                                      'vulnerabilidade_gelo',
                                      'vulnerabilidade_lutador',
                                      'vulnerabilidade_venenoso',
                                      'vulnerabilidade_terrestre',
                                      'vulnerabilidade_voador',
                                      'vulnerabilidade_pisiquico',
                                      'vulnerabilidade_inseto',
                                      'vulnerabilidade_pedra',
                                      'vulnerabilidade_fantasma',
                                      'vulnerabilidade_dragao',
                                      'vulnerabilidade_sombrio',
                                      'vulnerabilidade_aco',
                                      'vulnerabilidade_fada',
                                      'geracao']
    colunas_categorias_nominais = ['habilidades',
                                   'genero',
                                   'grupo_de_ovo',
                                   'cor_primaria',
                                   'forma']
    colunas_booleanas = ['sem_genero',
                         'evoluivel',
                         'bebe_pokemon',
                         'lendario',
                         'mitico',
                         'padrao',
                         'forma_temporaria', ]
    markdown_colunas_string = ''
    for coluna in colunas:
        markdown_colunas_string += "- " + coluna + "\n"
    with st.expander("Colunas utilizadas:"):
        st.markdown(markdown_colunas_string)
    st.write("As colunas categóricas nominais foram reajustadas utilizando **one-hot-encoding**, que transforma todos os valores unicos de uma coluna categórica em novas colunas com valor 1 ou 0.")
    st.write("Ocorrências que apresentavam o valor categórico terão o valor 1 na nova coluna e 0, caso não.")
    st.write("Em nossos testes, não foi possível executar utilizando todas colunas devido ao tamanho do dataset e o tempo de execução para agrupar os dados após a transformação das colunas categóricas (one-hot-encoding).")
    st.write("Removemos as colunas categóricas com maior quantidade de valores unicos, assim como algumas colunas de identificadores unicos que não entram no escopo de agrupamento")
    with st.expander("Colunas removidas:"):
        st.markdown("- nome\n- n_pokedex\n- tipo\n- evolui_de")
    st.write("\n")
    st.write("Para a clusterização, alem da transformação **one-hot-encoding** nas colunas categóricas nominais, foi aplicada a normalização dos valores quantitativos e categóricos ordinais.")
    ds_normalized = ds[colunas_quantitativas_ordinais +
                       colunas_categorias_nominais+colunas_booleanas]
    ds_com_cluster = ds[colunas_quantitativas_ordinais +
                        colunas_categorias_nominais+colunas_booleanas]
    for column in colunas_quantitativas_ordinais:
        ds_normalized[column] = (ds[column]-ds[column].min()) / (
            ds[column].max()-ds[column].min())
    ds_normalized = typeConversion(ds_normalized)
    colunas_categodicas_but_tipo = colunas_categorias_nominais.copy()
    colunas_categodicas_but_tipo.remove("habilidades")

    # ds_normalized = colummConversion(ds_normalized, 'forma')
    # st.dataframe(ds_normalized)

    for coluna in colunas_categodicas_but_tipo:
        print(coluna)
        ds_normalized = colummConversion(ds_normalized, coluna)
    for coluna in colunas_booleanas:
        ds_normalized[coluna] = ds_normalized[coluna].astype(int)

    st.write("Resumo do dataset após a normalização dos valores:")
    with st.expander("dataset formatado:"):
        st.dataframe(ds_normalized.describe())

    scale = StandardScaler()
    wcss = []
    wcss_range = range(2, 50)
    for n in wcss_range:
        cluster_builder = KMeans(
            n_clusters=n, init='k-means++', random_state=10)
        cluster_builder.fit(ds_normalized)
        wcss.append(cluster_builder.inertia_)

    plt.plot(wcss_range, wcss, 'bx-')
    plt.xlabel('Número de clusters')
    plt.ylabel('Inercia')
    plt.title('Metodo do cotovelo usando a inércia')
    st.pyplot(plt, clear_figure=True)

    # silh_scores = []
    # for n in wcss_range:
    #     cluster_builder = KMeans(n_clusters=n, init='k-means++', random_state=10)
    #     preds = cluster_builder.fit_predict(ds_normalized)
    #     silh_scores.append(silhouette_score(ds_normalized, preds))

    # plt.plot(wcss_range, silh_scores, 'bx-')
    # plt.xlabel('Número de clusters')
    # plt.ylabel('Coeficiente de silhueta')
    # plt.title('Metodo da silhueta')
    # st.pyplot(plt, clear_figure=True)
    range_n_clusters = [2,3,4,5,6,7,8,9]
    for n in range_n_clusters:
        plt.xlim((-0.1, 1))
        plt.ylim([0, len(ds_normalized)+(n + 1)*10])
        plt.figure(figsize=(15, 15))
        clusterer = KMeans(n, init='k-means++', random_state=10)
        cluster_labels = clusterer.fit_predict(ds_normalized)
        silhouette_avg = silhouette_score(ds_normalized, cluster_labels)
        st.write(silhouette_avg)

        sample_silhouette_values = silhouette_samples(
            ds_normalized, cluster_labels)

        y_lower = 10
        for i in range(n):
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
            ith_cluster_silhouette_values.sort()
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.nipy_spectral(float(i)/n)
            plt.fill_betweenx(np.arange(y_lower, y_upper),
                            0,
                            ith_cluster_silhouette_values,
                            color=color,
                            alpha=0.7)
            # /
            plt.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
            y_lower = y_upper + 10
        plt.yticks([])
        plt.title("Gráfico da silhueta para "+str(n)+" clusters")
        plt.xlabel("Valores do coeficiente de silhueta")
        plt.ylabel("Clusters")
        plt.axvline(x=silhouette_avg, color='red', linestyle='--')
        plt.savefig('fig'+str(n))
    # st.pyplot(plt, clear_figure=True)

    kmeans_f = KMeans(n_clusters=15, init='k-means++', random_state=10)
    kmeans_f.fit(ds_normalized)
    ds_normalized['clusters'] = kmeans_f.labels_
    ds_com_cluster['clusters'] = kmeans_f.labels_

    # range_colunas = ds_normalized.columns
    # centroids = pd.DataFrame(scale.inverse_transform(kmeans_f.cluster_centers_))
    # centroids.columns = range_colunas
    # centroids['clusters'] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    st.write('\n')
    st.header('Informações sobre os clusters')
    sns.set(font_scale=2)
    st.write("\n")
    sns.pairplot(ds_com_cluster[['vida', 'ataque', 'defesa', 'ataque_especial',
                 'defesa_especial', 'velocidade', 'clusters']], hue="clusters")
    plt.title('Dispersão dos Status Básicos entre os clusters')
    st.pyplot(plt, clear_figure=True)
    st.write("\n")

    sns.countplot(x=ds_com_cluster['clusters'], palette=["#0B50E3", "#0075FA"])
    plt.title('Quantidade de Pokémons por cluster')
    plt.xlabel('Cluster')
    plt.ylabel('Quantidade')
    st.pyplot(plt, clear_figure=True)
    st.write("""
        O gŕafico acima exibe a quantidade de pokémons distribuídos em cada cluster. Observa-se 
        que os clusters 1 e 6 possuem a maior quantidade de pokémons.
    """)

    cluster_mean = pd.DataFrame(ds_com_cluster.groupby(['clusters']).agg({
        'vida': 'mean',
        'ataque': 'mean',
        'defesa': 'mean',
        'ataque_especial': 'mean',
        'defesa_especial': 'mean',
        'velocidade': 'mean',
    }))
    st.dataframe(cluster_mean)
    st.write('\n')
    st.write("""
        Na tabela acima consta as médias dos atributos vida, ataque, defesa, ataque_especial, defesa_especial e velocidade.
        De maneira geral, observa-se que os clusters apresentam valores semelhantes.
        Porém há clusters que apresentam dados mais expressivos como o 3 que não apresenta nenhum atributo com média inferior a 90,
        isso implica que, neste cluster, há pokémons lendários. O cluster 10 também apresenta dados significativos,
        apesar de inferiores em relação aos primeiros. O cluster 2 apresenta as menores médias em quase todos os campos, indicando
        que a maioria das suas ocorrências são pokémon de estágio 0.
    """)


if __name__ == '__main__':
    main()
