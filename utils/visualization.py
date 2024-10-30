import altair as alt
import folium
from folium.plugins import HeatMap
import geopandas as gpd
import plotly.express as px
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium


def plot_hypothesis_1(data):
    monthly_data = data.groupby('Mes')[['Precipitacao', 'RiscoFogo']].mean().reset_index()
    fig = px.line(monthly_data, x='Mes', y=['Precipitacao', 'RiscoFogo'], title="Risco de Fogo vs Precipitação")
    return fig

def plot_hypothesis_2(data):
    monthly_fires = data.groupby('Mes')['RiscoFogo'].count().reset_index()
    avg_fires = monthly_fires['RiscoFogo'].mean()
    monthly_fires['Cor'] = monthly_fires['RiscoFogo'].apply(lambda x: 'red' if x > avg_fires else 'blue')
    
    fig = px.bar(monthly_fires, x='Mes', y='RiscoFogo', color='Cor', title="Queimadas por Mês")
    return fig

def plot_hypothesis_3(data):
    data['Mes'] = pd.to_datetime(data['DataHora']).dt.month
    df_bioma = data.groupby(['Bioma', 'Mes']).agg({
        'RiscoFogo': 'mean',
        'Precipitacao': 'mean',
        'FRP': 'mean',
        'DataHora': 'count'
    }).rename(columns={'DataHora': 'QuantidadeQueimadas'}).reset_index()

    for bioma in df_bioma['Bioma'].unique():
        df_bioma_filtrado = df_bioma[df_bioma['Bioma'] == bioma]
        st.write(f'Análise do Bioma: {bioma}')
        chart = alt.Chart(df_bioma_filtrado).mark_bar().encode(
            x='Mes:O',
            y=alt.Y('QuantidadeQueimadas', title='Queimadas'),
            color='RiscoFogo:Q'
        )
        st.altair_chart(chart, use_container_width=True)


def plot_hypothesis_4(data, month, year):
    filtered_data = data[(data['Mes'] == month) & (data['Ano'] == year)]
    gdf = gpd.GeoDataFrame(filtered_data, geometry=gpd.points_from_xy(filtered_data.Longitude, filtered_data.Latitude))
    fig = gdf.explore(column="RiscoFogo", cmap="OrRd", tooltip="Municipio", popup=True)
    return fig


def plot_hypothesis_5(data):

    data['Mes'] = pd.to_datetime(data['DataHora']).dt.month
    df_agrupado = data.groupby('Mes').agg({
        'DiaSemChuva': 'mean',
        'RiscoFogo': 'mean'
    }).reset_index()


    base = alt.Chart(df_agrupado).encode(x=alt.X('Mes:O', title='Mês'))


    barras_dias_sem_chuva = base.mark_bar(color='steelblue').encode(
        y=alt.Y('DiaSemChuva', title='Dias Sem Chuva')
    )

    barras_risco_fogo = base.mark_bar(color='firebrick').encode(
        y=alt.Y('RiscoFogo', title='Risco de Fogo')
    )

    st.write("Análise de Dias Sem Chuva e Risco de Fogo")
    st.altair_chart(barras_dias_sem_chuva + barras_risco_fogo, use_container_width=True)


def plot_hypothesis_6(data):
    st.write("Relação entre FRP e Risco de Fogo")
    scatter = alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X('FRP', title='FRP (Fire Radiative Power)'),
        y=alt.Y('RiscoFogo', title='Risco de Fogo'),
        color='Bioma',
        tooltip=['FRP', 'RiscoFogo', 'Bioma']
    ).interactive()
    st.altair_chart(scatter, use_container_width=True)

    data['Ano'] = pd.to_datetime(data['DataHora']).dt.year
    df_ano_frp = data.groupby(['Ano', 'Bioma']).agg({
        'FRP': 'mean',
        'RiscoFogo': 'mean'
    }).reset_index()

    line_chart = alt.Chart(df_ano_frp).mark_line().encode(
        x=alt.X('Ano:O', title='Ano'),
        y=alt.Y('FRP', title='Média Anual de FRP'),
        color='Bioma'
    )
    st.write("Variação Anual de FRP por Bioma")
    st.altair_chart(line_chart, use_container_width=True)
    
    
def plot_hypothesis_7(data):

    df_ma = data[data['Estado'] == 'Maranhão']

    maranhao_map = folium.Map(location=[-4.9609, -45.2744], zoom_start=6, tiles='Stamen Terrain')

    from folium.plugins import HeatMap
    heat_data = [[row['Latitude'], row['Longitude']] for index, row in df_ma.iterrows()]
    HeatMap(heat_data, radius=10).add_to(maranhao_map)

    st.write("Densidade de Queimadas no Estado do Maranhão")
    st_folium(maranhao_map, width=700, height=500)