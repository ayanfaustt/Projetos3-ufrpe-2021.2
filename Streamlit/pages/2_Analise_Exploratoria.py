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
    # Dataset apenas com as colunas de interesse
    ds_relevant = ds[skills]

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

    elif selected_option==option2:

        
        
        st.write('\n')



        st.subheader("Status por geração")

        
        #st.pyplot(px.scatter(x=ds_type_iterator['sum'], y=ds_type_iterator['gen_introduced']))
        
    elif selected_option==option3:
        st.header("Clusterização")
        st.write("Este tópico promove uma análise de correlacional dos atributos com o objetivo de compreender como estes se correlacionam.")    
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

if __name__ == '__main__':
    main()