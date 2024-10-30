import altair as alt
import folium
from folium.plugins import HeatMap
import geopandas as gpd
import plotly.express as px
import streamlit as st
import pandas as pd

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


