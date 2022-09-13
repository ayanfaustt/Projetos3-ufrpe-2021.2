# from sys import path
# from tkinter.tix import DirSelectBox
import streamlit as st
import pandas as pd
# import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px

st.set_page_config(
    page_title="Dataset",
    page_icon="📚",
)

def main():
    path_to_dataset = os.path.join(os.getcwd(),os.pardir)+"/pokemon.parquet"
    ds = pd.read_parquet(path_to_dataset)

    listaColuna = ['nome','n_pokedex', 'vida', 'tipo', 'ataque', 'defesa', 'velocidade']
    listaNulos = ['ciclo_de_ovo', 'felicidade_base', 'evoluivel', 'evolui_de', 'cor_primaria']
    listaVulnerabilidades = ['vulnerabilidade_normal',
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

    st.title("Visualização de dados")
    

    st.write('\n')

    st.write("Esta seção será dedicada a visualização dos dados contidos no dataset.")
    st.write('Abaixo encontra-se um overview do dataset utilizado:')
    st.write('\n')

    st.dataframe(ds.iloc[0:26,0:13])
    
    st.markdown(
        """
        Selecionamos apenas as primeiras 25 linhas e 13 colunas do dataset original.
        As colunas escolhidas para essa exibição foram as que contém informações
        consideradas básicas sobre os pokemons.

        Para ver mais colunas do dataset, basta usar o botão abaixo!
        """
    )

    colunasSelecionadas = st.multiselect(
            'Selecione colunas para serem exibidas', colunas)

    if st.button('Gerar tabela'):
            with st.expander("Resultados:"):
                st.dataframe(ds[colunasSelecionadas])

    st.markdown(
        """
        ### Estatísticas descritivas
        """
    )

    st.dataframe(ds[listaColuna].describe())

    st.markdown(
        """
        Dados estatísticos do dataset utilizado
        """
    )

    st.write('\n')
    
    st.header('Dados nulos')
    st.write('Rodando o comando "ds.isnull().sum()", obtém-se uma contagem dos resgistros que contém valor nulo para cada coluna.')

    st.dataframe(ds[listaNulos].isnull().sum())
    st.markdown(
        """
        A única coluna que apresenta registro nulos no dataset utilizado é a "evolui_de". Fato esse que ocorre porque nem todos os pokémons são evoluções de outro.
        """
    )
    
    st.write('\n')

    st.subheader('Exibição de alguns dados qualificativos')
    plt.figure(figsize= (20,10))

    sns.set(font_scale = 2)
    sns.countplot(x = ds['evoluivel'])
    
    plt.title('Pokémons que apresentam evoluções')
    plt.xlabel('Evoluível')
    plt.ylabel('Quantidade')
    st.pyplot(plt, clear_figure=True)
    st.write('O gráfico acima exibe a quantidade de pokémons que possuem ou não uma evolução.')
    
    st.write('\n')

    sns.countplot(x=ds['forma_temporaria'])
    plt.title("Pokémons com formas temporárias")
    plt.xlabel('Possui forma temporária')
    plt.ylabel('Quantidade')
    st.pyplot(plt, clear_figure=True)
    st.write("""
    O gráfico acima exibe a quantidade de pokémons que possuem formas temporárias (mega evoluções e Gigantamax).É possível observar
    que a quantidade de pokémons que contém esta mecânica é consiravelmente menor, uma vez que esse artifício foi introduzido pela 
    primeira vez na sexta geração dos jogos (mega evoluções) e surgiram novamente na oitava geração (Gigantamax).
    Esta informação é útil porque a mecânica de formas temporárias pode contribuir para o fator surpresa ao elaborar um time.
    """)


    st.write('\n')

    ds_lendario = ds[ds['lendario'] == True]
    st.dataframe(ds_lendario)
    
    plt.hist(x = ds_lendario['geracao'])

    plt.title("Quantidade de pokémons lendários por geração")
    plt.xlabel('Geração')
    plt.ylabel('Quantidade de Lendários')
    st.pyplot(plt, clear_figure=True)
    st.write("""
        O gráfico acima exibe a quantidade de pokémons lendários e suas variações. Os pokémons lendários são pokémons raros com valores de status
        acima da média caracterísca esta que é a causa dos poucos exemplares desses pokémons. Há uma grande variação entre a quantidade de pokémons
        por geração e, devido ao fato de pokémon ser uma franquia de jogos muita extensa, a variação pode dar-se que questões criativas e de mercado.
        Um dos objetivos dos jogos é completar a pokedex e ter noção da quantidade de lendarios existentes é de grande utilidade.
    """)

    st.write('\n')
    
    ds_mitico = ds[ds['mitico'] == True]

    plt.hist(x = ds_mitico['geracao'])

    plt.title("Quantidade de pokémons Míticos")
    plt.xlabel('Mítico')
    plt.ylabel('Quantidade')
    st.pyplot(plt, clear_figure=True)
    st.write("""
        O gráfico acima exibe a quantidade de pokémons míticos. Pokémons míticos são pokemons extremamente raros que não podem ser capturados na 'in game' 
        sendo possível pegá-los apenas em eventos específicos. Com este grupo de pokémons ocorre algo semelhante aos lendários quanto a sua distribuição
        pelas gerações. 
    """)

    st.write('\n')

    plt.hist(x = ds['geracao'])
    plt.xlabel('Geração')
    plt.ylabel('Quantidade')
    st.pyplot(plt,clear_figure=True)
    st.write("""
        O gráfico acima exibe a quantidade de pokémons por geração. A primeira geração de pokémons apresenta a maior quantidade de pokémons sendo uma das
        gerações mais populares da franquia.
    """)

    st.markdown(
        """
        ### Vulnerabilidade à ataques
        Os gráficos abaixo servem para termos uma visualização dos tipos de pokémon que mais causam dano em ataques.
        """
    )

    tipoSelecionado = st.multiselect(
            'Selecione tipo para ser exibido', listaVulnerabilidades)
    if st.button('Gerar'):
            with st.expander("Resultados:"):
                plt.hist(x = ds[tipoSelecionado])
                plt.xlabel('Quantidade de dano recebido em ataque')
                plt.ylabel('Quantidade de pokemons')
                st.pyplot(plt,clear_figure=True)
                st.write('O gráfico acima exibe a quantidade de pokémons vulneráveis ao ataque de pokémons do tipo selecionado')
    
    st.markdown(
        """
        È possível observar que, apesar de balanceados, os tipos *fogo*, *grama*, *gelo*, *lutador*, *terra* e *pedra* são os que apresentam um maior indice
        de pokemons que sofrem dano acima de 3,5.
        """
    )
    
if __name__ == '__main__':
    main()