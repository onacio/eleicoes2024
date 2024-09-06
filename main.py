import streamlit as st
import pandas as pd

# Ocupa a largura total da tela
st.set_page_config(layout='wide')

# Colunas que serão exibidas 
colunas = ['NM_VOTAVEL', 'NR_VOTAVEL', 'NR_SECAO', 'QT_VOTOS', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO']

# Carregando arquivo com dados
df = pd.read_csv('maragogipe.csv', delimiter=';', encoding='latin1')

# Menu que seleciona o nome do votável na tela
votavel = st.sidebar.selectbox('Nome do candidato', df['NM_VOTAVEL'].unique())

st.title('Eleição de 2020 - Maragogipe')

# aqui é feito o filtro pelo nome do votável assim que for selecionado
df_filtrado = df[df['NM_VOTAVEL'] == votavel]

# Exibe na tela o dataframe com os dados do votável que foi selecionado
st.dataframe(df_filtrado[colunas], hide_index=True)
