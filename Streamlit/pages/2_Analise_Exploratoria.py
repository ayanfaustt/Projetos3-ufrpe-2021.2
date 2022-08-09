import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px


def main():
    option1 = "Análise Correlacional"
    option2 = "Clusterização"
    option_list = [option1,option2]
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

    ds_status = pd.read_csv(path_to_dataset)
    ds_teste = ds[skills]
    ds_teste['gen_introduced'] = ds['gen_introduced']
    sum_status = list()

    for j in range(len(ds_teste)):
        sum = ds_teste['hp'][j] + ds_teste['attack'][j] + ds_teste['defense'][j] + ds_teste['special_attack'][j] + ds_teste['special_defense'][j] + ds_teste['speed'][j]
        sum_status.append(sum)
    ds_teste['sum'] = sum_status




    

    #
    if selected_option==option1:

        st.header("Análise Correlacional")
        st.write("Este tópico promove uma análise de correlacional dos atributos com o objetivo de compreender como estes se correlacionam.")
        st.write("Os atributos selecionados para essa análise foram:")
        st.markdown("- Vida\n- Ataque\n- Defesa \n- Ataque Especial\n- Defesa Especial\n- Velocidade\n")
       
        st.subheader("PairPlot dos atributos")
        st.write("O PairPlot é composto por diversos sub-gráficos. Cada um destes apresenta uma combinação de 2 atributos, um para casa eixo e exibe um mapeamento dos itens(Pokemons) dispostos segundos seus valores para os atributos pertinentes.")
        plt.rcParams.update({'font.size': 18})
        sns.pairplot(ds[skills])
        st.pyplot(plt,clear_figure=True)
        with st.expander("insights"):
            st.caption("isso e aquilo")
            st.write("")

        st.write("\n")

        st.subheader("HeatMap correlacional dos atributos")
        st.write("O HeatMap....")
        plt.figure(figsize=(3,2))
        plt.rcParams.update({'font.size': 5})
        sns.heatmap(ds[skills].corr(), cmap="Blues", annot=True)
        st.pyplot(plt)
        with st.expander("insights"):
            st.caption("isso e aquilo")
            st.write("")
        
        st.write("\n")

        st.subheader("Disbribuição dos Pokémons por Tipos")
        st.write("Pokémons com um tipo")
        mono_type_df = mono_type_.rename(columns={0: 'typing'})
        sns.displot(data=mono_type_df, x='typing', kde=True)
        st.pyplot(plt)

        # st.write("Pokémons com dois tipos")
        # middle = int(abs(len(multi_type_)/2))
        # multi_type_df1 = multi_type_[0:middle]
        # multi_type_df2 = multi_type_[middle: -1]
        # multi_type_df1 = multi_type_df1.rename(columns={0: 'typing'})
        # multi_type_df2 = multi_type_df2.rename(columns={0: 'typing'})

        # sns.displot(data=multi_type_df1, x='typing', kde=True)
        # st.pyplot(plt)
        # sns.displot(data=multi_type_df2, x='typing', kde=True)
        # st.pyplot(plt)

        st.write('\n')

        st.subheader("Status por geração")
        grafico_sum_status_gen = px.scatter_matrix(ds_teste, dimensions=['gen_introduced'], color='sum')
        # grafico_sum.write_image(file = './grafico_sum.png', format='png')
        sns.displot(data=ds_teste, x='gen_introduced', y='sum')
        st.pyplot(plt)
        
        st.pyplot(px.scatter(x=ds_teste['sum'], y=ds_teste['gen_introduced']))






    elif selected_option==option2:
        st.header("Clusterização")
        st.write("Este tópico promove uma análise de correlacional dos atributos com o objetivo de compreender como estes se correlacionam.")


if __name__ == '__main__':
    main()
