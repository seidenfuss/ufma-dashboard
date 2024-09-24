import streamlit as st
import pandas as pd 
import plotly_express as px
import seaborn as sns

# Configuração de página
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Importar dados
df = pd.read_csv('houses_to_rent_v2.csv', decimal="," )

# Traduzir valores (pode ir para outro arquivo, modificar o documento e salvar como csv...)
df['animal'] = df['animal'].replace('acept', 'Sim')
df['animal'] = df['animal'].replace('not acept', 'Não')
df['mobiliado'] = df['mobiliado'].replace('furnished', 'Sim')
df['mobiliado'] = df['mobiliado'].replace('not furnished', 'Não')

# Título do Dashboard
st.title("Visão Geral de Aluguéis no Brasil por Cidade")


# Caixa de seleção - cidades
cidade = st.sidebar.selectbox("Cidade", df["cidade"].unique())


# Subtítulo I
st.markdown('### Médias de Valores: '+ cidade)

#Filtrar dataframe por cidade
df_filtered = df[df["cidade"] == cidade]

# Template - estilo
template = "simple_white"

# Organizar containers
col1, col2, col3, col4 = st.columns(4)

# Calcular Médias
resultados  = {}
valores = ["condominio (R$)","aluguel (R$)","IPTU (R$)","seguro incendio (R$)"]
for i in valores:
    media = df_filtered[i].mean()
    resultados[i] = "{:.2f}".format(media)

# Mostrar médias
col1.metric("Aluguel", str("R$ " + resultados['aluguel (R$)']))
col2.metric("Condomínio", str("R$ " + resultados['condominio (R$)']) )
col3.metric("Seguro Incêndio", str("R$ " + resultados['seguro incendio (R$)']))
col4.metric("IPTU", str("R$ " + resultados['IPTU (R$)']))

#organizar containers
c1, c2, c3, c4 = st.columns((3,3,2,2))

with c1:
    st.markdown('### Número de Quartos')
    fig_quartos = px.histogram(df_filtered, x='quartos',  template=template )
    fig_quartos


with c2:
    st.markdown('### Valor do Aluguel')
    fig_aluguel = px.histogram(df_filtered, x='aluguel (R$)', nbins=40, template=template )
    fig_aluguel

with c3:
    st.markdown('### Aceita Animais?')
    fig_animal = px.pie(df_filtered, values = df_filtered.groupby("animal")["animal"].count(), names=["Não","Sim"], hole=0.5, template= template)
    fig_animal

with c4:
    st.markdown('### É mobiliado?')
    fig_mobilia = px.pie(df_filtered, values = df_filtered.groupby("mobiliado")["mobiliado"].count(), names=["Não","Sim"], hole=0.5, template=template)
    fig_mobilia

st.markdown('### Relação entre Área e Valor Total (Aluguel + Taxas)')
fig_aluguel_area=px.scatter(df_filtered, x="total (R$)", y="area")
fig_aluguel_area


# RUN
#streamlit run /home/ananeves/Documents/Github/python_UFMA/dashboard/app.py
