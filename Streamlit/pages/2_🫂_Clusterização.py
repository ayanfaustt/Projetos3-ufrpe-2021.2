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
import statsmodels.api as sm

st.set_page_config(
    page_title="Clusterização",
    page_icon="🫂",
)

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


def colummConversion(dataFrame, col):
    unique_val = dataFrame[col].unique()
    ds_aux = pd.DataFrame(columns=unique_val)
    var_iterator = [itemlist for itemlist in unique_val]
    for index in range(len(dataFrame)):
        dataAux = list()
        current_val = dataFrame.loc[index, col]
        for index_i in var_iterator:
          if current_val == index_i:
            dataAux.append(1)
          else:
            dataAux.append(0)
        ds_aux.loc[index] = dataAux

    new_dataFrame = pd.concat([dataFrame, ds_aux], axis= 1)
    new_dataFrame.drop([col], axis=1, inplace=True)
    return new_dataFrame

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
        """Aplicação do algoritmo Kmeans para a formação dos clusters de Pokémon"""
    )
    st.subheader("Preparação da Base de Dados")
    st.write(
        "Para a criação dos cluster serão utilizados os seguintes atributos: ")
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
    for coluna in colunas_cluster_all:
        markdown_colunas_string += "- " + coluna + "\n"
    with st.expander("Atributos utilizados:"):
        st.markdown(markdown_colunas_string)
    st.write("As colunas categóricas nominais foram reajustadas utilizando **one-hot-encoding**, que transforma todos os valores unicos de uma coluna categórica em novas colunas com valor 1 ou 0.")
    st.write("Ocorrências que apresentavam o valor categórico terão o valor 1 na nova coluna e 0, caso não.")
    st.write("Em nossos testes, não foi possível executar utilizando todas colunas devido ao tamanho do dataset e o tempo de execução para agrupar os dados após a transformação das colunas categóricas (one-hot-encoding).")
    st.write("Removemos as colunas categóricas com maior quantidade de valores unicos, assim como algumas colunas de identificadores unicos que não entram no escopo de agrupamento")
    with st.expander("Colunas removidas:"):
        st.markdown("- nome\n- n_pokedex\n- tipo\n- evolui_de")
    st.write("\n")
    st.markdown("""Para a clusterização, além da transformação **one-hot-encoding** nas colunas categórias nominais, realizamos testes de distribuição nas colunas quantitativas a fim de descobrir se
                seria necessário normalizar os dados contidos nelas ou não. Para isso, plotamos gráficos q-q e histogramas, para descobrirmos se esses dados eram gaussianos ou não. E descobrimos que a grande
                parte não era, portanto, foi necessário optarmos pela **normalização** desses dados.
                
                A baixo você pode observar a distribuição de cada coluna quantitativa:""")
    

    colunaSelecionada = st.multiselect(
            'Selecione coluna para ver sua distribuição', colunas_quantitativas_ordinais)

    if st.button('Gerar gráficos'):
        plt.title(f"Histograma dos dados da coluna {colunaSelecionada[0]}")
        plt.hist(ds[colunaSelecionada], rwidth=0.9)
        st.pyplot(plt, clear_figure=True)

        sm.qqplot(ds[colunaSelecionada[0]], line = "r")
        st.pyplot(plt, clear_figure=True)
    
    #Criação dos Clusters
    ds_normalized = ds[colunas_quantitativas_ordinais+colunas_categorias_nominais+colunas_booleanas]
    ds_com_cluster = ds[colunas]
    
    #Normalização dos Dados
    for column in colunas_quantitativas_ordinais:
        ds_normalized[column] = (ds[column]-ds[column].min()) / (
            ds[column].max()-ds[column].min())
    ds_normalized = typeConversion(ds_normalized)
    colunas_categodicas_but_tipo = colunas_categorias_nominais.copy()
    colunas_categodicas_but_tipo.remove("habilidades")

    #One Hot Encoding
    for coluna in colunas_categodicas_but_tipo:
        ds_normalized = colummConversion(ds_normalized,coluna) 
    #Conversão de booleano
    for coluna in colunas_booleanas:
        ds_normalized[coluna] = ds_normalized[coluna].astype(int)

    st.write("Resumo do dataset após a normalização dos valores:")
    with st.expander("dataset transformado:"):
        st.dataframe(ds_normalized.describe())
    

    wcss = []
    wcss_range = range(2, 50)
    for n in wcss_range:
        cluster_builder = KMeans(
            n_clusters=n, init='k-means++', random_state=10)
        cluster_builder.fit(ds_normalized)
        wcss.append(cluster_builder.inertia_)

    #Gráfico do Cotovelo
    plt.plot(wcss_range, wcss, 'bx-')
    plt.xlabel('Número de clusters')
    plt.ylabel('Inercia')
    plt.title('Metodo do cotovelo usando a inércia')
    st.pyplot(plt, clear_figure=True)


    range_n_clusters = [2,3,4,5,6,7,8,9,15,25,50]
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
        plt.clf()
    # st.pyplot(plt, clear_figure=True)

    #Formação dos Clusters
    kmeans_f = KMeans(n_clusters=15, init='k-means++', random_state=10)
    kmeans_f.fit(ds_normalized)
    ds_normalized['clusters'] = kmeans_f.labels_
    ds_com_cluster['clusters'] = kmeans_f.labels_

    st.write('\n')
    st.header('Informações sobre os clusters')
    sns.set(font_scale=2)
    st.write("\n")

    st.write("\n")

    sns.countplot(x=ds_com_cluster['clusters'], palette=["#0B50E3", "#0075FA"])
    plt.title('Quantidade de Pokémons por cluster')
    plt.xlabel('Cluster')
    plt.ylabel('Quantidade')
    st.pyplot(plt, clear_figure=True)
    st.write("""
        O gŕafico acima exibe a quantidade de pokémons distribuídos em cada cluster. Observa-se 
        que o cluster 5 apresenta a maior quantidade de Pokémon e enquanto o 10 é o oposto.
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
        Na tabela acima consta as médias dos atributos **vida**, **ataque**, **defesa**, **ataque_especial**, **defesa_especial** e **velocidade**.
        De maneira geral, observa-se que os clusters apresentam valores semelhantes.
        Porém há clusters que apresentam dados mais expressivos como o 5 que não apresenta nenhum atributo com média inferior a 90,
        isso implica que, neste cluster, há pokémons lendários pelos menos em sua maioria, porém faz-se necessária uma investigação para 
        validar isto, uma vez que este cluster é o que apresenta a maior quantidade de pokémon. 
        O cluster 13 também apresenta dados significativos,
        apesar de inferiores em relação aos primeiros. O cluster 11 apresenta todas as suas médias abaixo de 60, indicando
        que a maioria das suas ocorrências são pokémon de estágio 0.
    """)

    option_cluster = [5,10,11,13]
    st.write('\n')
    st.subheader('Analisando Clusters')
    selected_view = st.selectbox('Selecione uma opção', option_cluster)

    colunas_do_cluster=['vida','ataque','defesa','defesa_especial','ataque_especial','velocidade']

    #Cluster 5
    if selected_view == 5:

        st.subheader('Cluster 5')
        st.write("""
            Para averiguar as suposições levantas anteriorimente quanto aos pokémons lendários contidos neste cluster.
            Será realizada a contagem dos Pokémon lendários.
        """)
        st.write('\n')
        cluster5 = ds_com_cluster[ds_com_cluster['clusters'] == 5].copy()
        sns.countplot(x=cluster5['lendario'], palette=["#0B50E3","#0075FA"])
        plt.title('Pokémon lendários no Cluster 5')
        plt.ylabel('Quantidade')
        st.pyplot(plt, clear_figure=True)
        st.write("""
            O Gráfico acima confirma a existência de pokémom lendários, sendo estes a maioria que compõe o cluster e este fato explica 
            a ocorrência de médias mais altas em relação aos demais agrupamentos.
        """)
        st.write('\n')
        sns.countplot(x=cluster5['forma_temporaria'], palette=["#0B50E3", "#0075FA"])
        plt.title('Pokémon com forma temporária no Cluster 5')
        plt.ylabel('Quantidade')
        st.pyplot(plt, clear_figure=True)
        st.write("""
            O gráfico acima exibe os pokémon que são formas temporárias. Eles correspondem a uma parte considerável do cluster.
        """)
        st.write('\n')
        st.write("""
            O dois gráficos acima, além de comprovar a existência dos pokémons lendários neste cluster, também 
            mostra que há pokémon que são tão fortes que chegam perto dos pokémons lendarios
        """)
        
        cluster5['lendario'] = cluster5['lendario'].astype(int)
        cluster5['mitico'] = cluster5['mitico'].astype(int)
        cluster5['forma_temporaria'] = cluster5['forma_temporaria'].astype(int)

        st.write('\n')
        colunas_pairplot = st.multiselect('Selecione até 4 colunas para o Pairplot', colunas_do_cluster, key=1)
        

        if st.button('Gerar Pairplot'):
            with st.expander("Resultados:"):
                n_colunas = len(colunas_pairplot)
                if n_colunas > 4 or n_colunas < 1:
                    st.write("Selecione entre 1 e 4 colunas!")
                else:
                    plt.rcParams.update({'font.size': 6})
                    plt.figure(figsize=(5, 5))
                    pairplot_data = pd.melt(
                        cluster5, id_vars=['n_pokedex'], value_vars=colunas_pairplot)
                    fig = px.scatter_matrix(
                        cluster5, dimensions=colunas_pairplot, color='lendario')
                    fig.update_traces(diagonal_visible=False)
                    fig.update_layout(
                        title='Dispersão',
                    )
                    plt.title("Pairplot")
                    plt.xlabel("Colunas")
                    plt.ylabel("Valor")
                    st.plotly_chart(fig)

    #Cluster 10
    elif selected_view == 10:

        st.subheader('Cluster 10')
        st.write("""
            Este Cluster além de ter as médias consideravelmente baixas, apresenta o menor número de pokémon.
        """)
        st.write('\n')
        cluster10 = ds_com_cluster[ds_com_cluster['clusters'] == 10]
        st.dataframe(cluster10.iloc[0:18,0:13])
        st.write('\n')
        st.write("""
            Devido ao fato de ser um cluster pequeno, é possível obter uma visualização simples dos pokémon integrantes.
            Observa-se que o Cluster é composto por Pikachu e suas variantes além das evoluções.
            Este Cluster originou-se devido ao fato de existir uma grande variedade de Pikachu, criando um cluster próprio.
        """)

        st.write('\n')
        colunas_pairplot = st.multiselect('Selecione até 4 colunas para o Pairplot', colunas_do_cluster, key=1)

        if st.button('Gerar Pairplot'):
            with st.expander("Resultados:"):
                n_colunas = len(colunas_pairplot)
                if n_colunas > 4 or n_colunas < 1:
                    st.write("Selecione entre 1 e 4 colunas!")
                else:
                    plt.rcParams.update({'font.size': 6})
                    plt.figure(figsize=(5, 5))
                    pairplot_data = pd.melt(
                        cluster10, id_vars=['n_pokedex'], value_vars=colunas_pairplot)
                    fig = px.scatter_matrix(
                        cluster10, dimensions=colunas_pairplot)
                    fig.update_traces(diagonal_visible=False)
                    fig.update_layout(
                        title='Dispersão',
                    )
                    plt.title("Pairplot")
                    plt.xlabel("Colunas")
                    plt.ylabel("Valor")
                    st.plotly_chart(fig)

    #Cluster 11
    elif selected_view == 11:

        st.subheader('Cluster 11')
        st.write("""
            O cluster 11 destacou-se por ser o agrupamento com as menores médias em seus atributos.
        """)
        cluster11 = ds_com_cluster[ds_com_cluster['clusters'] == 11]
        filtro_1_cluster11 = cluster11[(cluster11['evoluivel'] == True) & cluster11['evolui_de'].isnull()] #pokémon estágio 0
        
        filtro_2_cluster11 = cluster11[(cluster11['evoluivel'] == False) & cluster11['evolui_de'].isnull()] # pokémon que não evolui
        #Pokémon estágio 1 ou 2
        filtro_3_cluster11 = cluster11.drop(filtro_1_cluster11.index)
        filtro_3_cluster11 = filtro_3_cluster11.drop(filtro_2_cluster11.index)
        st.write('\n')
        x = [1,2,3]
        plt.title('Estágios dos pokémon')
        plt.bar(x, height=[filtro_1_cluster11['nome'].count(),filtro_2_cluster11['nome'].count(),filtro_3_cluster11['nome'].count()])
        plt.xticks(x, ('Estágio 0','Pokémon sem evolução','Estágio 1'))
        st.pyplot(plt, clear_figure=True)
        st.write("""
            O gráfico acima exibe a quantidade de pokémon que estão no estágio 0, sem evolução e outros.
            É notório que os pokémons de estágio 0 são a maioria no cluster, jogando assim as médias gerais para baixo.
        """)

        st.write('\n')
        colunas_pairplot = st.multiselect('Selecione até 4 colunas para o Pairplot', colunas_do_cluster, key=1)

        if st.button('Gerar Pairplot'):
            with st.expander("Resultados:"):
                n_colunas = len(colunas_pairplot)
                if n_colunas > 4 or n_colunas < 1:
                    st.write("Selecione entre 1 e 4 colunas!")
                else:
                    plt.rcParams.update({'font.size': 6})
                    plt.figure(figsize=(5, 5))
                    pairplot_data = pd.melt(
                        cluster11, id_vars=['n_pokedex'], value_vars=colunas_pairplot)
                    fig = px.scatter_matrix(
                        cluster11, dimensions=colunas_pairplot)
                    fig.update_traces(diagonal_visible=False)
                    fig.update_layout(
                        title='Dispersão',
                    )
                    plt.title("Pairplot")
                    plt.xlabel("Colunas")
                    plt.ylabel("Valor")
                    st.plotly_chart(fig)

    #Cluster 13
    elif selected_view == 13:

        st.subheader('Cluster 13')
        st.write("""
            Este Cluster apresenta médias semelhantes as do cluster 5 e, devido a isso, vamos
            exibir algumas informações do agrupamento a fim de entender o porque da semelhança entre os clusters.
        """)
        st.write('\n')
        cluster13 = ds_com_cluster[ds_com_cluster['clusters'] == 13]
        sns.countplot(x=cluster13['forma_temporaria'], palette=["#0B50E3", "#0075FA"])
        plt.title('Pokémon com forma temporária no Cluster 13')
        plt.ylabel('Quantidade')
        st.pyplot(plt, clear_figure=True)
        st.write("""
            O gŕafico acima por si só já aponta a principal diferença em relação ao cluster 5. Pokémon em forma temporária
            recebem, em geral, um grande aumento em seus status, assemelhando-se, em alguns casos, aos Pokémon lendários.
        """)

       

        colunas_pairplot = st.multiselect('Selecione até 4 colunas para o Pairplot', colunas_do_cluster, key=1)

        if st.button('Gerar Pairplot'):
            with st.expander("Resultados:"):
                n_colunas = len(colunas_pairplot)
                if n_colunas > 4 or n_colunas < 1:
                    st.write("Selecione entre 1 e 4 colunas!")
                else:
                    plt.rcParams.update({'font.size': 6})
                    plt.figure(figsize=(5, 5))
                    pairplot_data = pd.melt(
                        cluster13, id_vars=['n_pokedex'], value_vars=colunas_pairplot)
                    fig = px.scatter_matrix(
                        cluster13, dimensions=colunas_pairplot)
                    fig.update_traces(diagonal_visible=False)
                    fig.update_layout(
                        title='Dispersão',
                    )
                    plt.title("Pairplot")
                    plt.xlabel("Colunas")
                    plt.ylabel("Valor")
                    st.plotly_chart(fig)
    st.text("\n")


if __name__ == '__main__':
    main()
