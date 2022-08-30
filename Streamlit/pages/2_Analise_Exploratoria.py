<<<<<<< HEAD
from copyreg import constructor
=======
from locale import normalize
from re import A
>>>>>>> e68f54f (Ajustes de tipos na tela principal)
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score



def main():
    option1 = "Análise Correlacional"
    option2 = "Análise basica"
    option3 = "Clusterização"
    option4 = "Analisando os dados"

    option_list = [option1, option2, option3, option4]

    # Layout callouts
    st.title("Análise Exploratória")
    selected_option = st.selectbox('Selecione uma opção', option_list)
    st.text("\n")
    #
    # Page persistent data
    status = ['hp',
              'attack',
              'defense',
              'special_attack',
              'special_defense',
              'speed']

    effects = ['normal_attack_effectiveness',
               'fire_attack_effectiveness',
               'water_attack_effectiveness',
               'electric_attack_effectiveness',
               'grass_attack_effectiveness',
               'ice_attack_effectiveness',
               'fighting_attack_effectiveness',
               'poison_attack_effectiveness',
               'ground_attack_effectiveness',
               'fly_attack_effectiveness',
               'psychic_attack_effectiveness',
               'bug_attack_effectiveness',
               'rock_attack_effectiveness',
               'ghost_attack_effectiveness',
               'dragon_attack_effectiveness',
               'dark_attack_effectiveness',
               'steel_attack_effectiveness',
               'fairy_attack_effectiveness']

    skills = status+effects

    path_to_dataset = os.path.join(os.getcwd(), os.pardir)+"/pokemon.csv"
    # Dataset completo
    ds = pd.read_csv(path_to_dataset)
<<<<<<< HEAD
    
=======
    # Dataset apenas com as colunas de interesse
    ds_relevant = ds[skills]
>>>>>>> e68f54f (Ajustes de tipos na tela principal)

    # types = ds['typing']

    # mono_type = list()
    # multi_type = list()
    # for i in types:
    #     if '~' in i:
    #         multi_type.append(i)
    #     else:
    #         mono_type.append(i)
    # mono_type_ = pd.DataFrame(mono_type)
    # multi_type_ = pd.DataFrame(multi_type)

    # if selected_option == option1:

    # st.header("Análise Correlacional")
    # st.write("Este tópico promove uma análise de correlacional dos atributos com o objetivo de compreender como estes se correlacionam.")
    # st.write("Os atributos selecionados para essa análise foram:")
    # st.markdown(
    #     "- Vida\n- Ataque\n- Defesa \n- Ataque Especial\n- Defesa Especial\n- Velocidade\n")

    # st.subheader("PairPlot dos atributos")
    # st.write("O PairPlot é composto por diversos 'sub-gráficos'. Cada um destes apresenta uma combinação de 2 atributos, um para casa eixo e exibe um mapeamento dos itens(Pokemons) dispostos segundo seus valores para os atributos pertinentes.")
    # st.write(
    #     "O PairPlot serve para plotar distribuições bivariadas de pares em um conjunto de dados")

    # plt.rcParams.update({'font.size': 18})
    # sns.pairplot(ds[skills])
    # st.pyplot(plt, clear_figure=True)
    # with st.expander("Insights"):
    #     st.caption("No plot é possível identificar onde a maior parte das ocorrências está baseando-se na densidade em diferentes regiões, também é possível visualizar algumas ocorrências que estão completamente fora da densidade.")
    #     st.caption("Também é possível identificar relações nas distribuições de diversos pares de dados através da forma que a distribuição de ocorrências está.")
    #     st.caption("Casos em que as ocorrências tendem a ter um valor maior de x para um valor maior de y, o par possui uma correlação de maior magnitude. Em casos que as ocorrências apresentam um padrão onde o valor de x tende a ser maior quando y for menor, o par possui uma correlação de menor magnitude.")
    #     st.caption("Considerando as plotagens acima, é possível reparar que alguns pares apresentam distribuições que apresentam maior magnitude de correçalação em consideração a outros, destacam-se:")
    #     st.markdown(
    #         "- Defesa x Defesa especial\n - Defesa especial x Ataque especial")
    #     st.write("\n")
    #     st.caption("É possível identificar também casos em que a magnitude da correlação é baixa, como por exemplo o par Defesa x Velocidade. Onde fica evidente que as ocorrências com maior velocidade apresentam menor defesa e vice-versa.")
    # st.write("\n")

    # st.subheader("HeatMap da correlação de pares")
    # st.write("O HeatMap é uma tecnica de visualização de dados que mostra a magnitude de um fênomeno correlacionando esta com a itensidade das cores.")
    # st.write("Este heatmap exibe a magnitude da correlação de um par de dados")
    # plt.rcParams.update({'font.size': 5})
    # plt.figure(figsize=(3, 2))
    # sns.heatmap(ds[skills].corr(), cmap="Blues", annot=True)
    # st.pyplot(plt)
    # with st.expander("insights"):
    #     st.caption("É interessante comparar os resultados do heatmap com a análise feita no Pairplot. As correlações entrepares identificadas no PairPlot se tornam evidentes aqui.")
    #     st.caption("As correlações de maior magnitude são:")
    #     st.markdown(
    #         "- Defesa x Defesa especial\n - Defesa especial x Ataque especial \n- Defesa x Ataque \n- Ataque x Vida")
    #     st.write("\n")
    #     st.caption("A relação de menor magnitude é, como previsto no pairplot, Defesa x Velocidade. Ressalva aos pares: Defesa Especial x Velocidade e Velocidade x Vida que também apresenta baixa correlação.")

    # st.write("\n")

    # elif selected_option == option2:
    # ds_teste = ds[skills]
    # ds_teste['gen_introduced'] = ds['gen_introduced']
    # sum_status = list()

    # for j in range(len(ds_teste)):
    #     sum = ds_teste['hp'][j] + ds_teste['attack'][j] + ds_teste['defense'][j] + \
    #         ds_teste['special_attack'][j] + \
    #         ds_teste['special_defense'][j] + ds_teste['speed'][j]
    #     sum_status.append(sum)
    # ds_teste['sum'] = sum_status
    # st.subheader("Disbribuição dos Pokémons por Tipos")
    # st.write("Pokémons com um tipo")
    # mono_type_df = mono_type_.rename(columns={0: 'typing'})
    # plt.figure(figsize=(3, 2))
    # plt.rcParams.update({'font.size': 8})
    # sns.displot(data=mono_type_df, x='typing', kde=True)
    # plt.xticks(rotation=90)

    # st.pyplot(plt, clear_figure=True)
    # st.write('\n')

    # st.subheader("Status por geração")
    # plt.rcParams.update({'font.size': 7})
    # sns.displot(data=ds_teste, x='gen_introduced', y='sum')
    # st.pyplot(plt, clear_figure=True)

    #st.pyplot(px.scatter(x=ds_teste['sum'], y=ds_teste['gen_introduced']))

    # elif selected_option == option3:
    # st.header("Clusterização")
    # st.write("Este tópico promove uma análise de correlacional dos atributos com o objetivo de compreender como estes se correlacionam.")

    if selected_option == option4:
        st.header("Analisando os dados")
        st.write("Este topico promove uma análise dos dados do dataset")
        st.write("Tendo em vista que no escopo do nosso projeto vamos trabalhar apenas no contexto de batalhas entre pokemons, vamos selecionar as colunas com atributos que são relevantes para tal contexto. Sendo estas:")
        st.markdown("- Vida\n- Ataque\n- Defesa \n- Ataque Especial\n- Defesa Especial\n- Velocidade\n- Efetividade de ataques do tipo normais\n- Efetividade de ataques do tipo fogo\n- Efetividade de ataques do tipo água\n- Efetividade de ataques do tipo elétrico\n- Efetividade de ataques do tipo planta\n- Efetividade de ataques do tipo gelo\n- Efetividade de ataques do tipo lutador\n- Efetividade de ataques do tipo veneno\n- Efetividade de ataques do tipo terra\n- Efetividade de ataques do tipo voador\n- Efetividade de ataques do tipo psicico\n- Efetividade de ataques do tipo inseto\n- Efetividade de ataques do tipo pedra\n- Efetividade de ataques do tipo fantasma\n- Efetividade de ataques do tipo dragão\n- Efetividade de ataques do tipo sombra\n- Efetividade de ataques do tipo aço\n- Efetividade de ataques do tipo fada\n")
        st.write('Os valores de efetividade são valores que multiplicam o dano que o pokemon vai receber dependendo do tipo que o atacou.')
        st.write('Por exemplo: Considere um pokemon com efetividade de ataques do tipo pedra no valor 2.0. Este pokemon recebera o dobro de dano de um ataque de um pokemon tipo pedra.')
        st.write(ds_relevant.describe())
        with st.expander("insights"):
            st.caption('A planilha exibe diversos valores relevantes. Nosso ponto de interesse esta nos valores minimos e maximos que indicam a amplitude destes atributos. Tendo em vista que o algoritmo de clusterização K-means faz uso de distancia euclidiana como valor para critério de agrupamento, valores com maior amplitude promoveram "maiores distancias" e portanto serão mais relevantes na clusterização. Para lidarmos com isso vamos normalizar todos atributos para que estes tenham a mesma amplitude e sejam, portanto, equivalentes no critério de agrupamento.')

<<<<<<< HEAD
    elif selected_option==option2:

        
        
        st.write('\n')



        st.subheader("Status por geração")

        
        #st.pyplot(px.scatter(x=ds_type_iterator['sum'], y=ds_type_iterator['gen_introduced']))
        
    elif selected_option==option3:
        st.header("Clusterização")
        st.write("Este tópico promove uma análise de correlacional dos atributos com o objetivo de compreender como estes se correlacionam.")
=======
    
        st.write(ds.describe())


        ds_normalized = ds_relevant.copy()

        for column in ds_normalized.columns:
            ds_normalized[column] = (ds_normalized[column]-ds_normalized[column].min()) / (
                ds_normalized[column].max()-ds_normalized[column].min())

        st.write('A tabela normalizada determinou os valores maximos para 1 e minimos para 0, ajustando os valores nesse intervalo preservando suas proporções.')
        st.write(ds_normalized.describe())

        ds_ajust = ds_normalized.copy()
        for effect in effects:
            ds_ajust[effect] = 1 - ds_ajust[effect]

        st.write(
            'Outro problema é a maneira como esses atributos escalam. Todos os atributos de efetividade escalam inversamente em beneficio do pokemon, ou seja, quanto maior for a efetividade, pior para o pokemon. Vamos "negativar" esses valores para que expressem uma escala compativel com os outros atributos. Tendo em vista que a tabela esta normalizada(todos os valores no intervalor [0,1]), basta passar a função f(x) = 1-x para todos atributos de efetividade.')
        st.write(ds_ajust.describe())
        
        plt.rcParams.update({'font.size': 3})
        plt.figure(figsize=(5, 5))
        sns.heatmap(ds_ajust[skills].corr(), cmap="Blues", annot=True)
        st.pyplot(plt, clear_figure=True)

        wcss = []
        wcss_range = range(2, 20)
        for n in wcss_range:
            cluster_builder = KMeans(n_clusters=n)
            cluster_builder.fit(ds_ajust)
            wcss.append(cluster_builder.inertia_)

        plt.plot(wcss_range, wcss, 'bx-')
        plt.xlabel('Número de clusters')
        plt.ylabel('Inercia')
        plt.title('Metodo do cotuvelo usando a inércia')
        st.pyplot(plt, clear_figure=True)

        silh_scores = []
        for n in wcss_range:
            cluster_builder = KMeans(n_clusters=n)
            preds = cluster_builder.fit_predict(ds_ajust)
            silh_scores.append(silhouette_score(ds_ajust,preds))
            
        plt.plot(wcss_range, silh_scores, 'bx-')
        plt.xlabel('Número de clusters')
        plt.ylabel('Coeficiente de silhueta')
        plt.title('Metodo da silhueta')
        st.pyplot(plt, clear_figure=True)
>>>>>>> e68f54f (Ajustes de tipos na tela principal)
        

if __name__ == '__main__':
    main()