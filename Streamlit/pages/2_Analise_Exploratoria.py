import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px


def main():
    option1 = "Análise Correlacional"
    option2 = "Análise basica"
    option3 = "Clusterização"

    option_list = [option1,option2,option3]
    # Layout callouts
    st.title("Análise Exploratória")
    selected_option = st.selectbox('Selecione uma opção',option_list)
    st.text("\n")
    #
    # Page persistent data
    skills = ['hp', 'attack', 'defense',
              'special_attack', 'special_defense', 'speed']
    path_to_dataset = os.path.join(os.getcwd(), os.pardir)+"/pokemon.csv"
    ds = pd.read_csv(path_to_dataset)
    types = ds['typing']
    
    mono_type = list()
    multi_type = list()
    for i in types:
        if '~' in i:
            multi_type.append(i)
        else:
            mono_type.append(i) 
    mono_type_ = pd.DataFrame(mono_type)
    multi_type_ = pd.DataFrame(multi_type)


    if selected_option==option1:

        st.header("Análise Correlacional")
        st.write("Este tópico promove uma análise de correlacional dos atributos com o objetivo de compreender como estes se correlacionam.")
        st.write("Os atributos selecionados para essa análise foram:")
        st.markdown("- Vida\n- Ataque\n- Defesa \n- Ataque Especial\n- Defesa Especial\n- Velocidade\n")
       
        st.subheader("PairPlot dos atributos")
        st.write("O PairPlot é composto por diversos 'sub-gráficos'. Cada um destes apresenta uma combinação de 2 atributos, um para casa eixo e exibe um mapeamento dos itens(Pokemons) dispostos segundo seus valores para os atributos pertinentes.")
        st.write("O PairPlot serve para plotar distribuições bivariadas de pares em um conjunto de dados")

        plt.rcParams.update({'font.size': 18})
        sns.pairplot(ds[skills])
        st.pyplot(plt,clear_figure=True)
        with st.expander("Insights"):
            st.caption("No plot é possível identificar onde a maior parte das ocorrências está baseando-se na densidade em diferentes regiões, também é possível visualizar algumas ocorrências que estão completamente fora da densidade.")
            st.caption("Também é possível identificar relações nas distribuições de diversos pares de dados através da forma que a distribuição de ocorrências está.")
            st.caption("Casos em que as ocorrências tendem a ter um valor maior de x para um valor maior de y, o par possui uma correlação de maior magnitude. Em casos que as ocorrências apresentam um padrão onde o valor de x tende a ser maior quando y for menor, o par possui uma correlação de menor magnitude.")
            st.caption("Considerando as plotagens acima, é possível reparar que alguns pares apresentam distribuições que apresentam maior magnitude de correçalação em consideração a outros, destacam-se:")
            st.markdown("- Defesa x Defesa especial\n - Defesa especial x Ataque especial")
            st.write("\n")
            st.caption("É possível identificar também casos em que a magnitude da correlação é baixa, como por exemplo o par Defesa x Velocidade. Onde fica evidente que as ocorrências com maior velocidade apresentam menor defesa e vice-versa.")
        st.write("\n")

        st.subheader("HeatMap da correlação de pares")
        st.write("O HeatMap é uma tecnica de visualização de dados que mostra a magnitude de um fênomeno correlacionando esta com a itensidade das cores.")
        st.write("Este heatmap exibe a magnitude da correlação de um par de dados")
        plt.rcParams.update({'font.size': 5})
        plt.figure(figsize=(3,2))
        sns.heatmap(ds[skills].corr(), cmap="Blues", annot=True)
        st.pyplot(plt)
        with st.expander("insights"):
            st.caption("É interessante comparar os resultados do heatmap com a análise feita no Pairplot. As correlações entrepares identificadas no PairPlot se tornam evidentes aqui.")
            st.caption("As correlações de maior magnitude são:")
            st.markdown("- Defesa x Defesa especial\n - Defesa especial x Ataque especial \n- Defesa x Ataque \n- Ataque x Vida")
            st.write("\n")
            st.caption("A relação de menor magnitude é, como previsto no pairplot, Defesa x Velocidade. Ressalva aos pares: Defesa Especial x Velocidade e Velocidade x Vida que também apresenta baixa correlação.")
        
        st.write("\n")

    elif selected_option==option2:
        ds_teste = ds[skills]
        ds_teste['gen_introduced'] = ds['gen_introduced']
        sum_status = list()

        for j in range(len(ds_teste)):
            sum = ds_teste['hp'][j] + ds_teste['attack'][j] + ds_teste['defense'][j] + ds_teste['special_attack'][j] + ds_teste['special_defense'][j] + ds_teste['speed'][j]
            sum_status.append(sum)
        ds_teste['sum'] = sum_status
        st.subheader("Disbribuição dos Pokémons por Tipos")
        st.write("Pokémons com um tipo")
        mono_type_df = mono_type_.rename(columns={0: 'typing'})
        plt.figure(figsize=(3,2))
        plt.rcParams.update({'font.size': 4.5})
        sns.displot(data=mono_type_df, x='typing', kde=True)
        st.pyplot(plt,clear_figure=True)
        st.write('\n')
        
        st.subheader("Status por geração")
        plt.rcParams.update({'font.size': 7})
        sns.displot(data=ds_teste, x='gen_introduced', y='sum')
        st.pyplot(plt,clear_figure=True)
        
        #st.pyplot(px.scatter(x=ds_teste['sum'], y=ds_teste['gen_introduced']))
        
    elif selected_option==option3:
        st.header("Clusterização")
        st.write("Este tópico promove uma análise de correlacional dos atributos com o objetivo de compreender como estes se correlacionam.")
        
if __name__ == '__main__':
    main()
