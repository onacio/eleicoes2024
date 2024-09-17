import streamlit as st
import pandas as pd

# Ocupa a largura total da tela
st.set_page_config(layout='wide')

# Colunas que serão exibidas 
colunas = ['NR_SECAO', 'QT_VOTOS', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO']
#'NM_VOTAVEL', 'NR_VOTAVEL'

# Carregando arquivo com dados
df = pd.read_csv('maragogipe.csv', delimiter=';', encoding='latin1')

st.write("""
    # Eleições de 2020 - Maragogipe - BA
    Dados da eleição de 2020 na cidade de Maragogipe - Ba fornecido pelo TSE
""")

# Menu que seleciona o nome do votável na tela
votavel = st.sidebar.selectbox('Nome do votável', df['NM_VOTAVEL'].unique())

# aqui é feito o filtro pelo nome do votável assim que for selecionado
df_filtrado = df[df['NM_VOTAVEL'] == votavel]
st.sidebar.multiselect('Selecione os votáveis', df_filtrado.columns)

dados_grafico = df_filtrado[['NM_VOTAVEL','QT_VOTOS']]

d = st.dataframe(dados_grafico, hide_index=True)

st.sidebar.write('# Dados do candidato')
st.sidebar.write(f'Nome: {df_filtrado['NM_VOTAVEL'].unique()}')
st.sidebar.write(f'Número: {df_filtrado['NR_VOTAVEL'].unique()}')
st.sidebar.write(f'Total de votos: {df_filtrado['QT_VOTOS'].sum()}')

# Exibe na tela o dataframe com os dados do votável que foi selecionado
st.dataframe(df_filtrado[colunas], hide_index=True)
