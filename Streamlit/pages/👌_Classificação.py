import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


st.set_page_config(
    page_title="CLassificação",
    page_icon="👌",
)

def typeConversion(dataFrame):
            unique_val = dataFrame["typing"].unique()

            type_iterator = list()
            for type in unique_val:
                if not ("~" in type):
                    type_iterator.append(type)

            for i in range(len(dataFrame)):
                type_aux = type_iterator[:]
                if '~' in dataFrame.loc[i, 'typing']:
                    pokemon_types = dataFrame.loc[i, 'typing'].split('~')
                    dataFrame.loc[i, pokemon_types[0]] = int(1)
                    dataFrame.loc[i, pokemon_types[1]] = int(1)
                    type_aux.pop(type_aux.index(pokemon_types[0]))
                    type_aux.pop(type_aux.index(pokemon_types[1]))
                    for j in type_aux:
                        dataFrame.loc[i, j] = int(0)
                else:
                    mono_type = dataFrame.loc[i, 'typing']
                    dataFrame.loc[i, mono_type] = int(1)
                    type_aux.pop(type_aux.index(mono_type))
                    for k in type_aux:
                        dataFrame.loc[i, k] = int(0)

            dataFrame.drop(['typing'], axis=1, inplace=True)

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

def convertBoleanValues(dataFrame):
    # dataFrame
    boolcolumns = ['genderless', 'baby_pokemon',
                    'mythical', 'is_default', 'forms_switchable', 'can_evolve']

    for i in range(len(boolcolumns)):
        dataFrame[boolcolumns[i]
                  ] = dataFrame[boolcolumns[i]].astype(int)

    return dataFrame

def pokeId(ds):
    listaId = []
    cont = -1
    for i in ds['pokedex_number']:
        cont += 1
        if len(listaId) >= 1:
            if listaId[cont - 1].count('.') > 0:
                if listaId[cont - 1][:listaId[cont-1].index('.')] != str(i):
                    listaId.append(str(i))
                else:
                    proxIndex = 0
                    proxIndex = int(listaId[cont - 1][listaId[cont-1].index('.') + 1:]) + 1
                    r = str(i).replace(str(i), '{}.{}'.format(i, proxIndex))
                    listaId.append(r)
            else:
                if listaId[cont - 1] == str(i):
                    r = str(i).replace(str(i), '{}.1'.format(i))
                    listaId.append(r)
                else:
                    listaId.append(str(i))
        else:
            listaId.append(str(i))

    ds['id'] = listaId
    
    return ds

def main():
    path_to_dataset = os.path.join(os.getcwd(), os.pardir)+"/pokemon.parquet"
    ds = pd.read_parquet(path_to_dataset)

    st.title("Classificação")   
    st.markdown(
        """
        ## Visualização de dados
        """
    )

    st.write('\n')
    st.write("As colunas categóricas nominais foram reajustadas utilizando **one-hot-encoding**, que transforma todos os valores unicos de uma coluna categórica em novas colunas com valor 1 ou 0.")
    st.write("Ocorrências que apresentavam o valor categórico terão o valor 1 na nova coluna e 0, caso não.")
    st.write("Em nossos testes, não foi possível executar utilizando todas colunas devido ao tamanho do dataset e o tempo de execução para agrupar os dados após a transformação das colunas categóricas (one-hot-encoding).")
    st.write("Removemos as colunas categóricas com maior quantidade de valores unicos, assim como algumas colunas de identificadores unicos que não entram no escopo de agrupamento")
    # st.write(
    #         "Para realizar a classificação dos dados será necessário aplicar o One Hot Encoding ao Dataset")
    with st.expander("Colunas removidas:"):
        st.markdown("- nome\n- n_pokedex\n- tipo\n- evolui_de\n- pode_evoluir\n- habilidades\n- grupo_de_ovos")
    st.write("\n")
    ds_class = ds.copy()

    ds_class['ml'] = ds_class['legendary'] + ds_class['mythical']
    ds_class = pokeId(ds_class)
    ds_class = typeConversion(ds_class)
    ds_class = colummConversion(ds_class, 'genus')
    ds_class = colummConversion(ds_class, 'shape')
    ds_class = colummConversion(ds_class, 'primary_color')
    ds_class = convertBoleanValues(ds_class)
 
    ds_class.drop(['abilities', 'can_evolve', 'evolves_from', 'name', 'egg_groups'], axis=1, inplace=True)

    st.dataframe(ds_class.iloc[0:25])
    st.write('\n')
    st.markdown(
        """
        ### Matriz de confusão
        """
    )

    st.write(
            "A matriz de confusão é uma tabela que representa os acertos e erros de uma classificação. Dessa forma é possível fazer cálculos de performance através destes resultados obtidos como vamos ver a seguir.")



    x = ds_class.drop(columns = ['legendary', 'mythical','pokedex_number', 'ml'])
    y = ds_class.ml

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.8)

    x_number = x.id

    # Criando modelo e treinando com os dados de treino
    dtc = DecisionTreeClassifier()
    dtc.fit(x_train, y_train)
    # Fazendo a predição nos dados de treino
    resultado_dtc = dtc.predict(x)
   
    # st.write(classification_report(y, resultado_dtc))

    # print heatmap
    labels = list(dtc.classes_)

    fig, ax = plt.subplots(figsize=(10,10))
    matriz = confusion_matrix(y, resultado_dtc, labels=labels)
    sns.heatmap(matriz, annot=True, linewidths=.5, ax=ax, xticklabels=labels, yticklabels=labels, vmax= 900, fmt='d')

    st.write(fig)
    st.write('\n')

if __name__ == '__main__':
    main()
