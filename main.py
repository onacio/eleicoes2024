import streamlit as st
import pandas as pd

import plotly.express as px

# Ocupa a largura total da tela
st.set_page_config(layout='wide')

# Colunas que serão exibidas 
colunas = ['NR_SECAO', 'QT_VOTOS', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO']

# Carregando arquivo com dados
df = pd.read_csv('maragogipe.csv', delimiter=';', encoding='latin1')

st.write("""
    # Eleições de 2020 - Maragogipe - BA
    Dados da eleição de 2020 na cidade de Maragogipe - Ba fornecido pelo TSE
""")

# Menu que seleciona o nome do votável na tela
st.sidebar.title('Filtrar dados')

cargo = st.sidebar.selectbox('Cargo', df['DS_CARGO'].unique())
df_cargo = df[df['DS_CARGO'] == cargo]

votavel = st.sidebar.selectbox('Nome do votável (Candidato)', df_cargo['NM_VOTAVEL'].unique())
df_votavel = df_cargo[df_cargo['NM_VOTAVEL'] == votavel]

# Localidades únicas para o multiselect
localidade = df_votavel['DS_LOCAL_VOTACAO_ENDERECO'].unique()
localidades = st.sidebar.multiselect('Endereço da seção eleitoral', localidade)

# Filtro para localidades selecionadas
if localidades:
    df_filtrado = df_votavel[df_votavel['DS_LOCAL_VOTACAO_ENDERECO'].isin(localidades)]
else:
    df_filtrado = df_votavel

# Exibindo dados do candidato na barra lateral
st.sidebar.write('# Dados do candidato')
st.sidebar.write(f'Nome: {df_votavel["NM_VOTAVEL"].unique()[0]}')
st.sidebar.write(f'Número: {df_votavel["NR_VOTAVEL"].unique()[0]}')
st.sidebar.write(f'Total de votos: {df_filtrado["QT_VOTOS"].sum()}')

# Exibe na tela o dataframe filtrado com as localidades selecionadas
st.dataframe(df_filtrado[colunas], hide_index=True, use_container_width=True)

# Agrupar os votos por candidato e ordenar em ordem decrescente
df_votos_por_candidato = df_cargo.groupby('NM_VOTAVEL')['QT_VOTOS'].sum().reset_index()
df_votos_por_candidato = df_votos_por_candidato.sort_values(by='QT_VOTOS', ascending=False)

# Definir a altura do gráfico com base na quantidade de candidatos
altura_grafico = len(df_votos_por_candidato) * 40  # Ajuste o multiplicador conforme necessário

# Criar o gráfico de barras horizontal com rolagem
fig = px.bar(df_votos_por_candidato, 
             x='QT_VOTOS', 
             y='NM_VOTAVEL', 
             orientation='h', 
             labels={'QT_VOTOS': 'Total de Votos', 'NM_VOTAVEL': 'Candidato'},
             title=f'Total de Votos por Candidato para {cargo}')

# Ajustar a altura do gráfico para caber todos os candidatos
fig.update_layout(height=altura_grafico, yaxis={'categoryorder': 'total ascending'})

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)