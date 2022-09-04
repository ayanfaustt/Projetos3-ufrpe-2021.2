from sys import path
from tkinter.tix import DirSelectBox
import streamlit as st
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px



def main():
    path_to_dataset = os.path.join(os.getcwd(),os.pardir)+"/pokemon.parquet"
    ds = pd.read_parquet(path_to_dataset)

    listaColuna = ['name','hp', 'attack', 'defense']
    colunas =['name',
    'pokedex_number',
    'abilities',
    'typing',
    'hp',
    'attack',
    'defense',
    'special_attack',
    'special_defense',
    'speed',
    'height',
    'weight',
    'genus',
    'gen_introduced',
    'female_rate',
    'genderless',
    'baby_pokemon',
    'legendary',
    'mythical',
    'is_default',
    'forms_switchable',
    'base_experience',
    'capture_rate',
    'egg_groups',
    'egg_cycles',
    'base_happiness',
    'can_evolve',
    'evolves_from',
    'primary_color',
    'shape',
    'number_pokemon_with_typing',
    'normal_attack_effectiveness',
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
    'fairy_attack_effectiveness'
    ]

    st.title("Visualização de dados")
    

    st.write('\n')

    st.write("Esta seção será dedicada a visualização dos dados contidos no dataset.")
    st.write('Abaixo encontra-se um overview do dataset utilizado:')
    st.write('\n')

    st.dataframe(ds.iloc[0:25,0:13])
    
    colunasSelecionadas = st.multiselect(
            'Selecione colunas para serem exibidas', colunas)

    if st.button('Gerar tabela'):
            with st.expander("Resultados:"):
                st.dataframe(ds[colunasSelecionadas])

    st.write('\n')
    st.dataframe(ds[listaColuna].describe())

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

    st.write('O gráfico acima exibe a disbrituíção dos pokémons por geração')
    
    
if __name__ == '__main__':
    main()
