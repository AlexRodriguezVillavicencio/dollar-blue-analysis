from core.cfg import TOKEN
from core.db import get_connection
from core.base import etl
from core.base.utils import  plot_goHistorical, get_peaks
from core.base.financial import variation, volatility, gap
import pandas as pd
import plotly.express as px


def update_db():
    url = 'https://api.estadisticasbcra.com'
    data = ['usd','usd_of','reservas','milestones','inflacion_interanual_oficial']
    header = {
        "Content-Type": "application/json",
        'Authorization': TOKEN
        }
    datos = etl.get_data(url,data,header)
    df = etl.data_transform(datos)
    etl.load_db(df,get_connection(),'datablue')

def blue_vs_official(df):
    df = df[-405:]
    df = df.reset_index(drop=True)
    va = variation(df['usd_blue'])
    m = volatility(va)
    df['volatility_blue'] = m
    va = variation(df['usd_official'])
    m = volatility(va)
    df['volatility_official'] = m
    df.dropna(inplace=True)
    df['gap'] = gap(df)
    df.reset_index(drop=True, inplace=True)
    return df

# 1. Día con mayor variación en la brecha
def report1(df):
    df =  blue_vs_official(df)
    dft = get_peaks(df,'gap',10)
    df_top = dft[0]
    list_top = dft[1]
    return plot_goHistorical(df['date'],df['gap'],'variación', 
            df_top['date'],df_top['top'],'picos', list_top)

# 2. Top 5 días con mayor volatilidad
def report2(df):
    df =  blue_vs_official(df)
    dft = get_peaks(df,'volatility_blue',2)
    df_top = dft[0]
    list_top = dft[1]
    return plot_goHistorical(df['date'],df['volatility_blue'],'volatilidad', 
                    df_top['date'],df_top['top'],'picos', list_top)

# 3 .Semana con mayor variación en la brecha
def report3(df):
    df = blue_vs_official(df)
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.strftime('%A')
    df['week'] = df['date'].dt.strftime('%U')
    df_week= df.groupby(['week']).mean()
    return px.bar(df_week, x=df_week.index, y="gap")

# 4. Día de la semana donde hay mayor variación en la brecha
def report4(df):
    df = blue_vs_official(df)
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.strftime('%A')
    df['week'] = df['date'].dt.strftime('%U')
    df_day= df.groupby(['day']).mean()
    return px.bar(df_day, x=df_day.index, y="gap")