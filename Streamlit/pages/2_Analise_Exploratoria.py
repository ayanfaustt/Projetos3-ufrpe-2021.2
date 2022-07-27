import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os


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

    elif selected_option==option2:
        st.header("Clusterização")
        st.write("Este tópico promove uma análise de correlacional dos atributos com o objetivo de compreender como estes se correlacionam.")


if __name__ == '__main__':
    main()
