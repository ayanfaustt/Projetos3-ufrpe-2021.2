import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from itertools import cycle
from contextlib import contextmanager, redirect_stdout
from io import StringIO

st.set_page_config(
    page_title="Classificação",
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

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        
        stdout.write = new_write
        yield

def main():
    path_to_dataset = os.path.join(os.getcwd(), os.pardir)+"/pokemon.parquet"
    ds = pd.read_parquet(path_to_dataset)


    
    st.title("Classificação")   

    st.write(
            "Esse algoritmo foi utilizado para verificar se pokémons lendários podem ser comparados a pokemóns que são considerados como “comuns”, ou seja, se um pokémon “comum” pode ser comparado à um nível de poder de um pokémon lendário, sendo ele considerado um pseudo-lendário, ou se um pokémon lendário pode ter o mesmo nível de poder que um pokémon “comum”.")
    
    st.markdown(
        """
        ## Tratamento dos dados
        """
    )

    st.write('\n')
    st.write("As colunas categóricas nominais foram reajustadas utilizando **one-hot-encoding**, que transforma todos os valores unicos de uma coluna categórica em novas colunas com valor 1 ou 0.")
    st.write("Ocorrências que apresentavam o valor categórico terão o valor 1 na nova coluna e 0, caso não.")
    # Refatorar linha abaixo
    st.write("Foi adicionada uma coluna “ml” que soma a coluna de pokemóns legendários e míticos, pois, pokemóns míticos são considerados tipos de pokémons lendários.") 
    st.write("Removemos as colunas categóricas com maior quantidade de valores unicos, assim como algumas colunas de identificadores unicos que não entram no escopo de agrupamento, além de colunas poderiam facilmente identifcar pokémons lendários através de seus dados.")
    # st.write(
    #         "Para realizar a classificação dos dados será necessário aplicar o One Hot Encoding ao Dataset")
    with st.expander("Colunas removidas:"):
        st.markdown("- nome\n- n_pokedex\n- tipo\n- evolui_de\n- pode_evoluir\n- habilidades\n- grupo_de_ovos\n- lendário\n- mítico")
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

    with st.expander('Resumo do dataset após a após a transformação dos dados e remoção das colunas:'):
        st.dataframe(ds_class.iloc[0:25])
    st.write('\n')
    st.markdown(
        """
        ## Algoritmo de Classificação Por Árvore de Decisão
        """
    )
    
    x = ds_class.drop(columns = ['legendary', 'mythical','pokedex_number', 'ml'])
    y = ds_class.ml
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.8)
    x_number = x.id

    dtc = DecisionTreeClassifier()
    dtc.fit(x_train, y_train)
    resultado_dtc = dtc.predict(x)

    st.markdown(
        """
        ### Classification Report
        """
    )
    output = st.empty()
    with st_capture(output.code):
        print(classification_report(y, resultado_dtc))

    st.markdown(
        """
        ### Matriz de confusão
        """
    )

    st.write(
            "A matriz de confusão é uma tabela que representa os acertos e erros de uma classificação. Dessa forma é possível fazer cálculos de performance através destes resultados obtidos como vamos ver a seguir.")

    labels = list(dtc.classes_)
    fig, ax = plt.subplots(figsize=(10,10))
    matriz = confusion_matrix(y, resultado_dtc, labels=labels)
    sns.heatmap(matriz, annot=True, linewidths=.5, ax=ax, xticklabels=labels, yticklabels=labels, vmax= 900, fmt='d')
    st.write(fig)
    st.write('\n')

    st.write('\n')
    st.markdown(
        """
        ### Curva ROC
        """
    )

    st.markdown(
        """
        A Curva Característica de Operação do Receptor (Receiver Operating Characteristic Curve), ou, simplesmente, curva ROC é uma representação gráfica do desempenho do classificador.

        A curva ROC bem como a matriz de confusão e suas métricas servem para ajudar a se aproximar do modelo ideal para aquele problema.
        """
    )

    y_score = dtc.predict_proba(x)
    y_test_roc = pd.get_dummies(y).values
    n_classes = 2
    lw = 2
    # Calculando a curva ROC para cada classe
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_roc[:,i], y_score[:,i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    # Gerando a curva ROC para cada classe, com cores diferentes para cada classe
    plt.figure()
    colors = cycle(['darkorange', 'cornflowerblue'])
    for i, color, classes in zip(range(n_classes), colors, dtc.classes_):
        plt.plot(fpr[i], tpr[i], color=color, lw=lw, label='{0} (area = {1:0.3f})'.format(classes, roc_auc[i]))
    # Configurações de eixos, legenda e título
    plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Especificidade', fontsize=20)
    plt.ylabel('Sensibilidade', fontsize=20)
    plt.title('Curva ROC Árvore de Decisão')
    plt.legend(loc="lower right", fontsize=20) 
    st.pyplot(plt, clear_figure=True)

    st.text("\n")

    st.markdown(
        """
        ### Outros métodos de Classificação
        """
    )

    st.write('O algoritmo de classificação arvore binária foi escolhido por ser o que teve mais eficácia, com a finalidade de avaliar dos modelos de classificação KNN e Regressão logísitca veremos adiante os avaliadores de desempenho dos classificadores.')

    # Variaveis dos nomes das telas
    # Tela que promove um resumo das colunas e dos dados
    # Tela que exibe a Classificação Regressão Logística
    option1 = "Classificação por Regressão Logística"
    # Tela que exibe a Classificação KNN
    option2 = "Classificação KNN"

    option_list = [option1, option2]

    # Cabeçalho de analise dos dados
    # st.markdown(
    #     """
    #     ## Analise dos dados
    #     """
    # )

    selected_view = st.selectbox('Selecione uma opção', option_list)
    st.text("\n")

    if selected_view == option1:
        # with st.expander("Resultados:"):
        # Criando modelo e treinando com os dados de treino
        clr = LogisticRegression()
        clr.fit(x_train, y_train)
        # Fazendo a predição nos dados de treino
        resultado_clr = clr.predict(x)

        st.markdown(
        """
        ### Matriz de confusão
        """
        )

        # Gerando plot da matriz de confusão
        labels = list(clr.classes_)
        fig, ax = plt.subplots(figsize=(10,10))
        matriz = confusion_matrix(y, resultado_clr, labels=labels)
        sns.heatmap(matriz, annot=True, xticklabels=labels, yticklabels=labels,vmax= 900, fmt='d')
        st.write(fig)

        st.markdown(
        """
        ### Curva ROC
        """
        )

        # Definindo algumas variáveis para cálculo da curva ROC
        y_score = clr.predict_proba(x_test)
        y_test_roc = pd.get_dummies(y_test).values
        n_classes = 2
        lw = 2
        # Calculando a curva ROC para cada classe
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test_roc[:,i], y_score[:,i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        # Gerando a curva ROC para cada classe, com cores diferentes para cada classe
        plt.figure()
        colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
        for i, color, classes in zip(range(n_classes), colors, clr.classes_):
            plt.plot(fpr[i], tpr[i], color=color, lw=lw, label='{0} (area = {1:0.3f})'.format(classes, roc_auc[i]))
        # Configurações de eixos, legenda e título
        plt.plot([0, 1], [0, 1], 'k--', lw=lw)
        plt.xlim([-0.05, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Especificidade', fontsize=20)
        plt.ylabel('Sensibilidade', fontsize=20)
        plt.title('Curva ROC Regressão Logística')
        plt.legend(loc="lower right", fontsize=20)
        st.pyplot(plt, clear_figure=True)

    if selected_view == option2:
        # with st.expander("Resultados:"):
        st.markdown(
        """
        ### Matriz de confusão
        """
        )
        # Criando modelo e treinando com os dados de treino
        knn = KNeighborsClassifier()
        knn.fit(x_train, y_train)
        # Fazendo a predição nos dados de treino
        resultado_knn = knn.predict(x)

        labels = list(knn.classes_)
        fig, ax = plt.subplots(figsize=(10,10))
        matriz = confusion_matrix(y, resultado_knn, labels=labels)
        sns.heatmap(matriz, annot=True, xticklabels=labels, yticklabels=labels, vmax= 900, fmt='d')
        st.write(fig)

        st.markdown(
        """
        ### Curva ROC
        """
        )
        
        y_score = knn.predict_proba(x)
        y_test_roc = pd.get_dummies(y).values
        n_classes = 2
        lw = 2
        # Calculando a curva ROC para cada classe
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test_roc[:,i], y_score[:,i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        # Gerando a curva ROC para cada classe, com cores diferentes para cada classe
        plt.figure()
        colors = cycle(['darkorange', 'cornflowerblue'])
        for i, color, classes in zip(range(n_classes), colors, knn.classes_):
            plt.plot(fpr[i], tpr[i], color=color, lw=lw, label='{0} (area = {1:0.3f})'.format(classes, roc_auc[i]))
        # Configurações de eixos, legenda e título
        plt.plot([0, 1], [0, 1], 'k--', lw=lw)
        plt.xlim([-0.05, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Especificidade', fontsize=20)
        plt.ylabel('Sensibilidade', fontsize=20)
        plt.title('Curva ROC KNN')
        plt.legend(loc="lower right", fontsize=20) 
        st.pyplot(plt, clear_figure=True)

if __name__ == '__main__':
    main()
