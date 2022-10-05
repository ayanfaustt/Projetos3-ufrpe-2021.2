import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

image = Image.open('../img.png')

def main():

    st.set_page_config(
        layout="centered",
        page_title="Home",
        page_icon="🏠"
        )
    st.title("Grupo OCC")
    st.write('Neste sistema será apresentado toda parte visual da análise do dataset "Complete Pokemon Data Set"')
    st.image(image)
    st.write('''Ao lado esquerdo, estão as páginas que representam etapas do tratamento da base de dados, onde
    todos os gráficos ou tabelas possuem uma breve explicação do que está sendo mostrado.''')

if __name__ == '__main__':
    main()




