from sys import path
import streamlit as st
import pandas as pd
import numpy as np
import os

def main():
    path_to_dataset = os.path.join(os.getcwd(),os.pardir)+"/pokemon.csv"
    ds = pd.read_csv(path_to_dataset)
    st.title("Data Set")
    st.dataframe(ds,None)
    
if __name__ == '__main__':
    main()
