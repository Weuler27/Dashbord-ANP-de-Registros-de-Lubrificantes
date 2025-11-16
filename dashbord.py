#------------------IMPORTAÇÃO DA BIBLIOTECAS----------------------------------------------------------

import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st

#------------------IMPORTAÇÃO DOS DADOS PARA ANÁLISE---------------------------------------------------

dados = pd.read_csv(r'C:\Users\user\OneDrive\Documentos\Projeto_Python\Projeto 1\dados-abertos-registro-produtos.csv' , sep =';' )

#------------------ CONFIG STREAMLIT ---------------------------------------------------

st.set_page_config(page_title='Dashboard ANP', layout='wide') # nome da pagina

st.title('Dashboard de Análise de Registros de Lubrificantes') #titulo do dashbord
st.markdown('Base de Dados ANP') #subtitilo do dashbord

# -------------------- RANGE SLIDER PARA INTERVALO DE ANOS ----------------------------

anos_disponiveis = sorted(dados['ANO'].unique())

ano_min, ano_max = st.sidebar.select_slider(
    "Selecione o intervalo de anos",
    options=anos_disponiveis,
    value=(anos_disponiveis[0], anos_disponiveis[-1])   # valor inicial = todo intervalo
)

# Filtra os dados com base no intervalo selecionado
dados_filtrados = dados[(dados['ANO'] >= ano_min) & (dados['ANO'] <= ano_max)]

#------------------RECALCULA AS MÉTRICAS FILTRANDO PELO INTERVALO-------------------------------------------

registro_por_ano = dados_filtrados['ANO'].value_counts().sort_index() #registros por ano
produtos_por_marca = dados_filtrados['MARCA_COMERCIAL'].value_counts().head(10) # as primeiras 10 mascas com maiores registros
contagem_detentores = dados_filtrados['DETENTOR'].value_counts().head(10) # os primeiros 10 maiores detentores de registros

tipos_empresa = dados_filtrados['TIPO_EMPRESA'].value_counts() #tipos de empresa
dados_porcentagem_empresa = tipos_empresa / tipos_empresa.sum() * 100 # tipos de empresa em porcentagem

tipos_aplicacao = dados_filtrados['APLICACAO'].value_counts().head(15) # os 15 maiores tipos de aplicação

tipos_origem = dados_filtrados['ORIGEM'].value_counts() #tipos de origem
dados_porcentagem_origem = tipos_origem / tipos_origem.sum() * 100 # tipos de origem em porcentagem

#------------------------MONTANDO O DASHBOARD-------------------------------------------------------------

col1, col2 = st.columns(2) # dividindo em 2 colunas para ter 3 gráficos em cada coluna

#----------------------COLUNA 1 ------------------------------------------------------

with col1:

    #Gráfico 1 de linha de Quantidade de Registros por Ano
    st.subheader(f'Registros por Ano ({ano_min} a {ano_max})')
    fig1, ax1 = plt.subplots(figsize=(10,5))
    ax1.plot(registro_por_ano.index, registro_por_ano.values,
             marker='o', linestyle='-', color='blue')
    ax1.set_xlabel('Ano')
    ax1.set_ylabel('Quantidade de Registros', fontsize=14)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True)
    st.pyplot(fig1)

    #Gráfico 3 de barras horizontal de Quantidade de Detentores
    st.subheader(f'Quantidade de Detentores ({ano_min} a {ano_max})')
    fig3, ax3 = plt.subplots(figsize=(10,5))
    contagem_detentores_2 = contagem_detentores.sort_values(ascending=True)
    ax3.barh(contagem_detentores_2.index, 
             contagem_detentores_2.values, 
             color='blue')
    ax3.set_xlabel('Quantidade')
    ax3.set_ylabel('Detentores')
    st.pyplot(fig3)

    #Gráfico 5 de pizza Distribuição Porcentual de Tipos de Empresa
    st.subheader('Distribuição por Tipo de Empresa')
    fig5, ax5 = plt.subplots(figsize=(10,5))
    cmap = plt.get_cmap('winter')
    cores = cmap([i / len(tipos_empresa) for i in range(len(tipos_empresa))])
    ax5.pie(dados_porcentagem_empresa,
            labels=dados_porcentagem_empresa.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=cores,
            wedgeprops={'edgecolor':'white', 'linewidth':2},
            textprops={'color':'black', 'fontsize':10})
    st.pyplot(fig5)

#----------------------COLUNA 2 ------------------------------------------------------

with col2:
    #Gráfico 2 de barras horizontal de Produtos por marca
    st.subheader(f'Produtos por Marca ({ano_min} a {ano_max})')
    fig2, ax2 = plt.subplots(figsize=(10,6))
    produtos_por_marca_2 = produtos_por_marca.sort_values(ascending=True)
    ax2.barh(produtos_por_marca_2.index, 
             produtos_por_marca_2.values, 
             color='blue')
    ax2.set_xlabel('Quantidade')
    ax2.set_ylabel('Marca')
    st.pyplot(fig2)

    #Gráfico 4 de barras horizontal de Tipos de Aplicação
    st.subheader(f'Tipos de Aplicação ({ano_min} a {ano_max})')
    fig4, ax4 = plt.subplots(figsize=(10,5))
    tipos_aplicacao_2 = tipos_aplicacao.sort_values(ascending=True)
    ax4.barh(tipos_aplicacao_2.index, 
             tipos_aplicacao_2.values,
             color='blue')
    ax4.set_xlabel('Quantidade')
    ax4.set_ylabel('Tipos de Aplicação')
    st.pyplot(fig4)

    #Gráfico 6 de pizza de Distribuição Porcentual por Tipo de Origem.
    st.subheader('Distribuição por Tipo de Origem')
    fig6, ax6 = plt.subplots(figsize=(10,3))
    cmap = plt.get_cmap('winter')
    cores = cmap([i / len(tipos_origem) for i in range(len(tipos_origem))])
    ax6.pie(dados_porcentagem_origem,
            labels=dados_porcentagem_origem.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=cores,
            wedgeprops={'edgecolor':'white', 'linewidth':2},
            textprops={'color':'black', 'fontsize':10})
    st.pyplot(fig6)
