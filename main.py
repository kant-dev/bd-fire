import streamlit as st
from utils.data_preprocessing import load_and_prepare_data
from utils.visualization import plot_hypothesis_1, plot_hypothesis_2, plot_hypothesis_3, plot_hypothesis_4

data = load_and_prepare_data()

st.sidebar.header("Filtros")
year = st.sidebar.selectbox("Selecione o Ano", sorted(data['Ano'].unique()))

st.title("Análise de Risco de Queimadas e Sazonalidade")

st.subheader("Hipótese 1: Precipitação vs Risco de Fogo")
fig1 = plot_hypothesis_1(data[data['Ano'] == year])
st.plotly_chart(fig1)

st.subheader("Hipótese 2: Sazonalidade das Queimadas")
fig2 = plot_hypothesis_2(data[data['Ano'] == year])
st.plotly_chart(fig2)

st.subheader("Hipótese 3: Comparação entre Biomas")
fig3 = plot_hypothesis_3(data)
st.plotly_chart(fig3)

st.subheader("Hipotese 4: Distribuição Geográfica das Queimadas")
fig4 = plot_hypothesis_4(data, data["Mes"], data["Ano"])
st.plotly_chart(fig4)