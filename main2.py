import streamlit as st
import pandas as pd
import yfinance as yf


@st.cache_data
def carregar_dados(empresas):
    texto_tickers = ' '.join(empresas)
    dados_acao = yf.Tickers(empresas)
    cotacoes_acao = dados_acao.history(period='1d', start='2024-01-01', end='2024-08-01')
    cotacoes_acao = cotacoes_acao['Close']
    return cotacoes_acao

acoes = ['ITUB4.SA', 'PETR4.SA', 'MGLU3.SA', 'VALE3.SA', 'ABEV3.SAZ', 'GGBR4.SA']

dados = carregar_dados(acoes)

st.write("""
    # App preço de ações
    asdfsdfsdfsdfs sfsdf sdfsdf sdfsdfwef dfsd
""")

lista_acoes = st.multiselect('Escolha as ações', dados.columns)

if lista_acoes:
    dados = dados[lista_acoes]

st.line_chart(dados)