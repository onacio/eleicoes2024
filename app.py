import streamlit as st
import pandas as pd
import plotly.express as px

# Ocupa a largura total da tela
st.set_page_config(layout='wide')

# Colunas que serão exibidas
colunas = ['NM_VOTAVEL','NR_SECAO', 'QT_VOTOS', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO']

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

# Alteração: Usar multiselect para selecionar vários candidatos
votaveis = st.sidebar.multiselect('Nome do votável (Candidato)', df_cargo['NM_VOTAVEL'].unique())

# Filtro para os candidatos selecionados
if votaveis:
    df_votavel = df_cargo[df_cargo['NM_VOTAVEL'].isin(votaveis)]
else:
    df_votavel = df_cargo

# Localidades únicas para o multiselect
localidade = df_votavel['DS_LOCAL_VOTACAO_ENDERECO'].unique()
localidades = st.sidebar.multiselect('Endereço da seção eleitoral', localidade)

# Filtro para localidades selecionadas
if localidades:
    df_filtrado = df_votavel[df_votavel['DS_LOCAL_VOTACAO_ENDERECO'].isin(localidades)]
else:
    df_filtrado = df_votavel

# Exibindo dados do candidato na barra lateral
if votaveis:
    st.sidebar.write('# Dados dos candidatos selecionados')
    for candidato in votaveis:
        total_votos = df_filtrado[df_filtrado['NM_VOTAVEL'] == candidato]['QT_VOTOS'].sum()
        numero_votavel = df_filtrado[df_filtrado['NM_VOTAVEL'] == candidato]['NR_VOTAVEL'].unique()[0]
        st.sidebar.write(f'Nome: {candidato}')
        st.sidebar.write(f'Número: {numero_votavel}')
        st.sidebar.write(f'Total de votos: {total_votos}')               
else:
    st.sidebar.write('Selecione pelo menos um candidato.')

# Exibe na tela o dataframe filtrado com as localidades selecionadas
st.dataframe(df_filtrado[colunas], hide_index=True, use_container_width=True)

# Agrupar os votos por candidato e ordenar em ordem decrescente
df_votos_por_candidato = df_filtrado.groupby('NM_VOTAVEL')['QT_VOTOS'].sum().reset_index()
df_votos_por_candidato = df_votos_por_candidato.sort_values(by='QT_VOTOS', ascending=False)

# Criar o gráfico de barras vertical para comparar candidatos
fig = px.bar(df_votos_por_candidato, 
             x='NM_VOTAVEL', 
             y='QT_VOTOS', 
             labels={'QT_VOTOS': 'Total de Votos', 'NM_VOTAVEL': 'Candidato'},
             title=f'Comparação de Votos para {cargo}')

# Ajustar o layout para melhorar a exibição
fig.update_layout(xaxis_tickangle=-45)  # Inclinar os nomes dos candidatos

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)