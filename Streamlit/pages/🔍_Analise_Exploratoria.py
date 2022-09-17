from copyreg import constructor
from locale import normalize
from logging.handlers import RotatingFileHandler
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

st.set_page_config(
    page_title="Análise Exploratória",
    page_icon="🔍",
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

    st.title("Analise exploratória")   
    st.markdown(
        """
        ## Visualização de dados
        """
    )

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
        ## Estatísticas descritivas
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

    # Lista das Colunas de Status
    status = ['hp',
              'attack',
              'defense',
              'special_attack',
              'special_defense',
              'speed']
    # Lista das Colunas de Vulnerabilidade
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

    # Variaveis dos nomes das telas
    # Tela que promove um resumo das colunas e dos dados
    # Tela que exibe o pré-processamento
    option1 = "Analisando os dados Categóricos nominais"
    # Tela que exibe as analíses exploratorias feitas
    option2 = "Analisando os dados Quantitativos e Categóricos Ordinais"
    # Tela que exibe a distribuiíção das ocorrências
    option3 = "Analisando a distribuição de ocorrencias"
    # Lista com nomes das telas
    option_list = [option1, option2, option3]

    # Cabeçalho de analise dos dados
    st.markdown(
        """
        ## Analise dos dados
        """
    )

    selected_view = st.selectbox('Selecione uma opção', option_list)
    st.text("\n")

    if selected_view == option1:
        colunas_categorias = ['nome',
                              'habilidades',
                              'tipo',
                              'genero',
                              'geracao',
                              'sem_genero',
                              'bebe_pokemon',
                              'lendario',
                              'mitico',
                              'padrao',
                              'forma_temporaria',
                              'grupo_de_ovo',
                              'evoluivel',
                              'evolui_de',
                              'cor_primaria',
                              'forma']

        markdown_categorias_string = ''
        for coluna in colunas_categorias:
            markdown_categorias_string += "- " + coluna + "\n"
        st.subheader(option1)
        st.write("Os dados categoricos do dataset são:")
        st.markdown(markdown_categorias_string)
        st.subheader("Verificando os atributos correlacionados")
        st.write("Vamos verificar se um grupo de pokemons com um mesmo valor de uma coluna categorica sempre vão apresentar um valor unico em alguma outra coluna.")
        select_coluna_1 = st.selectbox(
            'Seleciona uma coluna', colunas_categorias)
        coluna_valores_unicos = ds[select_coluna_1].unique()
        select_valor_unico = st.selectbox(
            'Selecione um dos valores unicos', coluna_valores_unicos, key=1)
        with st.expander("Resultados:"):
            loc = ds.loc[ds[select_coluna_1] == select_valor_unico]
            lista_colunas_similares = []
            lista_valor_similar = []
            for coluna in loc.columns:
                if coluna != select_coluna_1:
                    unicos = loc[coluna].unique()
                    if len(unicos) == 1:
                        lista_colunas_similares.append(coluna)
                        lista_valor_similar.append(unicos[0])

            if len(lista_colunas_similares) > 0:
                st.write("As colunas a seguir sempre apresentam o mesmo valor quando o valor da coluna: " +
                         str(select_coluna_1) + " é " + str(select_valor_unico))
                markdown_colunas_valores_similares = ''
                for i in range(len(lista_colunas_similares)):
                    markdown_colunas_valores_similares += "- " + \
                        str(lista_colunas_similares[i]) + " : " + \
                        str(lista_valor_similar[i]) + "\n"
                st.markdown(markdown_colunas_valores_similares)
            else:
                st.write("Não existe nenhuma coluna que apresente sempre o mesmo valor quando a coluna: " +
                         str(select_coluna_1) + " tem o valor: " + str(select_valor_unico))

            st.write("\n")
            st.write("Dataframe de todas ocorrências que apresentam o valor: " +
                     str(select_valor_unico)+" na coluna: " + str(select_coluna_1))
            st.dataframe(loc)

        st.write("\n")

        st.write("Vamos verificar se todos os valores de uma coluna categorica apresentam uma ou mais colunas em comum que sempre terão um mesmo valor, dado o valor da coluna categórica sendo analisada.")
        select_coluna_2 = st.selectbox(
            'Seleciona uma coluna', colunas_categorias, key=2)
        with st.expander("Resultados:"):
            # Pegando todas as colunas com valores unicos dado o valor unico de uma coluna categorica
            matriz_controle_colunas = []
            lista_valores_unicos = ds[select_coluna_2].unique()
            for valor_unico in lista_valores_unicos:
                unico_ds = ds.loc[ds[select_coluna_2] == valor_unico]
                lista_colunas_valores_unicos = []
                for coluna in unico_ds.columns:
                    if coluna != select_coluna_2:
                        coluna_unique = unico_ds[coluna].unique()
                        if len(coluna_unique) == 1:
                            lista_colunas_valores_unicos.append(coluna)
                matriz_controle_colunas.append(lista_colunas_valores_unicos)

            # Verificando colunas presentes em todas ocorrências
            colunas_sempre_presentes = []
            matriz_valores_unicos_by_unique = []
           # valores_associados_sempre_diferentes = True

            if len(matriz_controle_colunas) > 1:
                conjunto_referencia = matriz_controle_colunas[0]
                for coluna in conjunto_referencia:
                    coluna_bool = True
                    for conjunto in matriz_controle_colunas:
                        if conjunto.count(coluna) == 0:
                            coluna_bool = False
                    if coluna_bool == True:
                        colunas_sempre_presentes.append(coluna)

            if len(colunas_sempre_presentes) > 0:
                # for valor_unico in lista_valores_unicos:
                #     unico_ds = dsParquet.loc[dsParquet[select_coluna_2] == valor_unico]
                #     lista_valores_unicos = []
                #     for coluna in colunas_sempre_presentes:
                #         lista_valores_unicos.append(unico_ds[coluna].unique())
                #     matriz_valores_unicos_by_unique.append(lista_valores_unicos)

                # for i in range(len(matriz_valores_unicos_by_unique)):
                #     for j in range(i+1,len(matriz_valores_unicos_by_unique)):
                #         if matriz_valores_unicos_by_unique[i] == matriz_valores_unicos_by_unique[j]:
                #             print(matriz_valores_unicos_by_unique[i])
                #             print(matriz_valores_unicos_by_unique[j])
                #             valores_associados_sempre_diferentes = False
                st.write("Todas os valores unicos da coluna: " +
                         select_coluna_2 + " tem um valor unico associado nas colunas:")
                # if valores_associados_sempre_diferentes == True:
                #     st.write("A combinação dos valores associados é unica para cada valor da coluna: "+ select_coluna_2)
                markdown_colunas_sempre_presentes = ''
                for coluna in colunas_sempre_presentes:
                    markdown_colunas_sempre_presentes += "- " + coluna + "\n"
                st.markdown(markdown_colunas_sempre_presentes)
            else:
                st.write(
                    "Não existem valores associados aos valores unicos na coluna: " + select_coluna_2)

    elif selected_view == option2:
        colunas_quantitativas = ['vida',
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
                                 'vulnerabilidade_fada']
        # st.dataframe(dsParquet)
        colunas_ordinais = ['geracao']
        colunas_ordinais_quantitativas = colunas_ordinais + colunas_quantitativas
        markdown_quantitativos_string = ''
        markdown_ordinais_string = ''
        for coluna in colunas_quantitativas:
            markdown_quantitativos_string += "- " + coluna + "\n"
        for coluna in colunas_ordinais:
            markdown_ordinais_string += "- " + coluna + "\n"
        st.subheader(option2)
        st.write("Os dados quantitativos do dataset são:")
        st.markdown(markdown_quantitativos_string)
        st.write("Os dados ordinais do dataset são:")
        st.markdown(markdown_ordinais_string)
        st.subheader("Verificando os outliers")
        st.write("É importante explicar que os outliers no contexto no contexto deste projeto devem ser interpretados como Pokemons que simplesmente estão acima da média e portanto não deve haver um tratamento para esses casos.")
        colunas_pairplot = st.multiselect(
            'Selecione até 4 colunas para o Boxplot', colunas_ordinais_quantitativas, key=1)
        usar_dados_normalizados = st.checkbox('Usar dados normalizados')
        if st.button('Gerar Boxplot'):
            with st.expander("Resultados:"):
                n_colunas = len(colunas_pairplot)
                if n_colunas > 4 or n_colunas < 1:
                    st.write("Selecione entre 1 e 4 colunas!")
                else:
                    plt.rcParams.update({'font.size': 6})
                    plt.figure(figsize=(6, 6))

                    ds_local = ds.copy()
                    if usar_dados_normalizados:
                        for coluna in colunas_pairplot:
                            ds_local[coluna] = (ds[coluna]-ds[coluna].min()) / (
                                ds[coluna].max()-ds[coluna].min())

                    pairplot_data = pd.melt(
                        ds_local, id_vars=['n_pokedex'], value_vars=colunas_pairplot)
                    sns.boxplot(x='value', y='variable', data=pairplot_data, color='skyblue')
                    plt.title("BoxPlot")
                    plt.ylabel("Colunas")
                    plt.xlabel("Valor")
                    st.pyplot(plt, clear_figure=True)

        st.write("\n")
        st.subheader("Verificando os coeficientes correlacionais")
        st.write("Utilizando o heatmap:")
        colunas_heatmap = st.multiselect(
            'Selecione entre 5 e 10 colunas para o HeatMap', colunas_ordinais_quantitativas, key=2)
        if st.button('Gerar HeatMap'):
            with st.expander("Resultados:"):
                n_colunas = len(colunas_heatmap)
                if n_colunas > 10 or n_colunas < 5:
                    st.write("Selecione entre 1 e 4 colunas!")
                else:
                    plt.rcParams.update({'font.size': 6})
                    plt.figure(figsize=(5, 5))
                    sns.heatmap(ds[colunas_heatmap].corr(),
                                cmap="Blues", annot=True)
                    st.pyplot(plt, clear_figure=True)

        st.write("\n")
        st.write("Filtrando dentro de uma amplitude:")
        filter_range = st.slider(
            'Selecione uma amplitude para filtragem', -1.0, 1.0, (-0.5, 0.5))
        if st.button('Encontrar coeficientes'):
            with st.expander("Resultados:"):
                range_min = filter_range[0]
                range_max = filter_range[1]
                result_matrix = []
                colunas_controler = colunas_ordinais_quantitativas.copy()
                for coluna_ref in colunas_ordinais_quantitativas:
                    colunas_controler.remove(coluna_ref)
                    for coluna_comp in colunas_controler:
                        coef_corr = ds[coluna_ref].corr(ds[coluna_comp])
                        if coef_corr >= range_min and coef_corr <= range_max:
                            result_matrix.append(
                                [coluna_ref, coluna_comp, coef_corr])

                def keyFunc(e):
                    return e[2]
                result_matrix.sort(reverse=True, key=keyFunc)
                markdown_result_corr = ''
                for i in result_matrix:
                    markdown_result_corr += "- " + \
                        str(i[0]) + " : " + str(i[1]) + \
                        "  =  " + str(i[2]) + "\n"
                st.markdown(markdown_result_corr)

    elif selected_view == option3:
        colunas_quantitativas = ['nome',
                                 'vida',
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
                                 'vulnerabilidade_fada']
        st.subheader(option3)
        ds_ocorrencia = ds.copy()
        # st.dataframe(ds_ocorrencia.iloc[0:25,0:13])
        st.write(
            "Para analisar a dispersão de ocorrência dos dados será necessário aplicar o One Hot Encoding ao Dataset")

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

        # def colummConversion(dataFrame, col):

        #     unique_val = dataFrame[col].unique()
        #     teste = pd.DataFrame(columns= unique_val)

        #     var_iterator = [itemlist for itemlist in unique_val]
        #     for index in range(len(dataFrame)):
        #         varIterator_aux = var_iterator[:]
        #         current_val = dataFrame.loc[index,col]
        #         dataFrame.loc[index, current_val] = 1
        #         varIterator_aux.pop(varIterator_aux.index(current_val))
        #         for index_i in varIterator_aux:
        #             # print(dataFrame.loc[index,index_i]
        #             dataFrame.loc[index,index_i] = 0

        #     dataFrame.drop([col], axis=1, inplace=True)

        #     return dataFrame

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

        def convertBoleanValues(dataFrame):
            # dataFrame
            boolcolumns = ['sem_genero', 'bebe_pokemon', 'lendario',
                           'mitico', 'padrao', 'forma_temporaria', 'evoluivel']

            for i in range(len(boolcolumns)):
                dataFrame[boolcolumns[i]
                          ] = dataFrame[boolcolumns[i]].astype(int)

            return dataFrame

        ds_ocorrencia = typeConversion(ds_ocorrencia)
        ds_ocorrencia = colummConversion(ds_ocorrencia, 'genero')
        ds_ocorrencia = colummConversion(ds_ocorrencia, 'forma')
        ds_ocorrencia = colummConversion(ds_ocorrencia, 'cor_primaria')
        ds_ocorrencia = convertBoleanValues(ds_ocorrencia)

        ds_ocorrencia.drop(['habilidades', 'evoluivel'], axis=1, inplace=True)

        st.dataframe(ds_ocorrencia.iloc[0:25])

        st.write("")
        colunas_pairplot = st.multiselect(
            'Selecione até 4 colunas para o Pairplot', colunas_quantitativas, key=1)
        usar_dados_normalizados = st.checkbox('Usar dados normalizados')

        if st.button('Gerar Pairplot'):
            with st.expander("Resultados:"):
                n_colunas = len(colunas_pairplot)
                if n_colunas > 4 or n_colunas < 1:
                    st.write("Selecione entre 1 e 4 colunas!")
                else:
                    plt.rcParams.update({'font.size': 6})
                    plt.figure(figsize=(5, 5))
                    ds_local = ds_ocorrencia.copy()

                    pairplot_data = pd.melt(
                        ds_local, id_vars=['n_pokedex'], value_vars=colunas_pairplot)
                    fig = px.scatter_matrix(
                        ds_local, dimensions=colunas_pairplot)
                    fig.update_traces(diagonal_visible=False)
                    fig.update_layout(
                        title='Dispersão',
                    )
                    plt.title("Pairplot")
                    plt.xlabel("Colunas")
                    plt.ylabel("Valor")
                    st.plotly_chart(fig)

    # elif selected_view == option3:
if __name__ == '__main__':
    main()
