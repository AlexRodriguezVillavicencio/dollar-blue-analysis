from cfg import TOKEN
from db import get_connection
from base import etl
from base.utils import  plot_goHistorical, get_peaks

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

def blue_vs_official():
    #Dólar oficial vs Dólar Blue:
    engine = get_connection()
    df = pd.read_sql('datablue',con=engine)
    df.drop(['international_reserves','event','event_type',' inflation'], axis=1, inplace=True)
    df = df[-405:]
    df = df.reset_index(drop=True)
    va = df['usd_blue'].pct_change()
    m = va.rolling(40).std()*100*(260)**0.5
    df['volatility_blue'] = m
    va = df['usd_official'].pct_change()
    m = va.rolling(40).std()*100*(260)**0.5
    df['volatility_official'] = m
    df.dropna(inplace=True)
    df['gap'] = ((df['usd_blue']/df['usd_official']) -1)*100
    df.reset_index(drop=True, inplace=True)
    return df

def report_day_week(df):
            df['date'] = pd.to_datetime(df['date'])
            df['day'] = df['date'].dt.strftime('%A')
            df['week'] = df['date'].dt.strftime('%U')
            return df

class Fig:
    
    # 1. Día con mayor variación en la brecha
    def report1(self):
        df = blue_vs_official()
        get_peaks(df,'gap',10)
        df_top = get_peaks()[0]
        list_top = get_peaks()[1]

        fig = plot_goHistorical(df['date'],df['gap'],'variación', 
                        df_top['date'],df_top['gap_top'],'picos', list_top)
        return fig

    # 2. Top 5 días con mayor volatilidad
    def report2(self):
        df = blue_vs_official()
        get_peaks(df,'volatility_blue',2)
        df_top = get_peaks()[0]
        list_top = get_peaks()[1]

        fig = plot_goHistorical(df['date'],df['volatility_blue'],'volatilidad', 
                        df_top['date'],df_top['top'],'picos', list_top)
        return fig

    # 3. .Semana con mayor variación en la brecha
    def report3(self):
        df = blue_vs_official()
        df = report_day_week(df)
        df_week= df.groupby(['week']).mean()
        fig = px.bar(df_week, x=df_week.index, y="gap", title="Long-Form Input")
        return fig


    # 4. Día de la semana donde hay mayor variación en la brecha
    def report4(self):
        df = blue_vs_official()
        df = report_day_week(df)
        df_day= df.groupby(['day']).mean()
        fig = px.bar(df_day, x=df_day.index, y="gap", title="Long-Form Input")
        return fig