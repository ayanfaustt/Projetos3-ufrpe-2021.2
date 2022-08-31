from copyreg import constructor
from locale import normalize
from re import A
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score


def typeConversion(dataFrame):
    unique_val = dataFrame["tipo"].unique()

    type_iterator = list()
    for type in unique_val:
        if not ("~" in type):
            type_iterator.append(type)

    for i in range(len(dataFrame)):
        type_aux = type_iterator[:]
        if '~' in dataFrame.loc[i, 'tipo']:
            pokemon_types = dataFrame.loc[i, 'tipo'].split('~')
            dataFrame.loc[i, pokemon_types[0]] = int(1)
            dataFrame.loc[i, pokemon_types[1]] = int(1)
            type_aux.pop(type_aux.index(pokemon_types[0]))
            type_aux.pop(type_aux.index(pokemon_types[1]))
            for j in type_aux:
                dataFrame.loc[i, j] = int(0)
        else:
            mono_type = dataFrame.loc[i, 'tipo']
            dataFrame.loc[i, mono_type] = int(1)
            type_aux.pop(type_aux.index(mono_type))
            for k in type_aux:
                dataFrame.loc[i, k] = int(0)

    dataFrame.drop(['tipo'], axis=1, inplace=True)

    return dataFrame


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
    path_to_dataset = os.path.join(os.getcwd(), os.pardir)+"/pokemon.csv"
    # Dataset completo
    ds = pd.read_csv(path_to_dataset)
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
               'formas_evolucao',
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
    colunas_categorias_nominais = ['tipo',
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
        st.markdown("- nome\n- n_pokedex\n- habilidades\n- formas_evolucao")
    st.write("\n")
    st.write("Para a clusterização, alem da transformação **one-hot-encoding** nas colunas categóricas nominais, foi aplicada a normalização dos valores quantitativos e categóricos ordinais.")
    ds_normalized = ds[colunas_quantitativas_ordinais+colunas_categorias_nominais+colunas_booleanas]
    for column in colunas_quantitativas_ordinais:
            ds_normalized[column] = (ds[column]-ds[column].min()) / (
                ds[column].max()-ds[column].min())
    ds_normalized = typeConversion(ds_normalized)
    colunas_categodicas_but_tipo = colunas_categorias_nominais.copy()
    colunas_categodicas_but_tipo.remove("tipo")
    for coluna in colunas_categodicas_but_tipo:
        ds_normalized = colummConversion(ds_normalized,coluna)
    for coluna in colunas_booleanas:
        ds_normalized[coluna] = ds_normalized[coluna].astype(int)
    st.write("Resumo do dataset após a normalização dos valores:")
    with st.expander("dataset formatado:"):
        st.dataframe(ds_normalized.describe())
    
    wcss = []
    wcss_range = range(2, 25)
    for n in wcss_range:
        cluster_builder = KMeans(n_clusters=n)
        cluster_builder.fit(ds_normalized)
        wcss.append(cluster_builder.inertia_)

    plt.plot(wcss_range, wcss, 'bx-')
    plt.xlabel('Número de clusters')
    plt.ylabel('Inercia')
    plt.title('Metodo do cotovelo usando a inércia')
    st.pyplot(plt, clear_figure=True)

    silh_scores = []
    for n in wcss_range:
        cluster_builder = KMeans(n_clusters=n)
        preds = cluster_builder.fit_predict(ds_normalized)
        silh_scores.append(silhouette_score(ds_normalized, preds))

    plt.plot(wcss_range, silh_scores, 'bx-')
    plt.xlabel('Número de clusters')
    plt.ylabel('Coeficiente de silhueta')
    plt.title('Metodo da silhueta')
    st.pyplot(plt, clear_figure=True)

if __name__ == '__main__':
    main()
