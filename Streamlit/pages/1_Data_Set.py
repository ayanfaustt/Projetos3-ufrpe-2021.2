from sys import path
import streamlit as st
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px

def main():
    path_to_dataset = os.path.join(os.getcwd(),os.pardir)+"/pokemon.csv"
    ds = pd.read_csv(path_to_dataset)
    st.title("Visualização de dados")
        
    st.write('\n')

    st.write("Esta seção será dedicada a visualização dos dados contidos no dataset.")
    st.write('Abaixo encontra-se mm overview do dataset utilizado:')
    st.write('\n')

    st.dataframe(ds)
    st.write('\n')
    st.dataframe(ds.describe())

    st.write('\n')
    
    st.header('Dados nulos')
    st.write('Rodando o comando "ds.isnull().sum()", obtém-se uma contagem dos resgistros que contém valor nulo para cada coluna.')

    st.dataframe(ds.isnull().sum() )
    st.write('Observa-se que a única coluna que apresenta registros nulos é a "evolves_from". Coluna esta que contém a pré-evolução de cada pokémon.')
    
    st.write('\n')

    st.subheader('Exibição dos dados')
    plt.figure(figsize= (20,10))

    sns.set(font_scale = 2)
    sns.countplot(x = ds['can_evolve'])
    
    plt.xlabel('Evoluível')
    plt.ylabel('Quantidade')
    st.pyplot(plt, clear_figure=True)
    st.write('O gráfico acima exibe a quantidade de pokémons que possuem ou não uma evolução.')
    
    st.write('\n')
    
    sns.countplot(x = ds['genderless'])

    plt.xlabel('Sem Gênero')
    plt.ylabel('Quantidade')
    st.pyplot(plt, clear_figure=True)
    st.write('O gráfico acima exibe a quantidade de pokémons que possuem ou não divisão de gênero')

    st.write('\n')

    plt.hist(x = ds['gen_introduced'])
    plt.xlabel('Geração')
    plt.ylabel('Quantidade')
    st.pyplot(plt,clear_figure=True)

    st.write('\n')
    grafico = px.scatter_matrix(ds, dimensions = ['attack','defense','hp','special_attack','special_defense'], color = 'hp')
    grafico.update_traces(diagonal_visible = False)
    grafico.update_layout(
        title='Status de combate',
        width=1000,
        height=800,
    )
    st.plotly_chart(grafico)

    st.write('O gráfico acima exibe a disbrituíção dos pokémons')
    
    
if __name__ == '__main__':
    main()
