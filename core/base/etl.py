import pandas as pd
from core.base.utils import join_url, data_cleaning
import requests

#extracción de datos
def get_data(url:str,data:list,header) -> dict:
    data_dict = {}
    for i in data:
        url2 = join_url(url,i)        
        response = requests.get(url2, headers=header)

        if response.status_code == 200:
            payload = response.json()
            data_dict[i] = payload
    return data_dict

#transformacion de datos
def data_transform(datos):
    df_usd = pd.json_normalize(datos['usd'])
    df_usdof = pd.json_normalize(datos['usd_of'])
    df_r = pd.json_normalize(datos['reservas'])
    df_s = pd.json_normalize(datos['milestones'])
    df_i = pd.json_normalize(datos['inflacion_interanual_oficial'])
    df = df_usd.merge(df_usdof, on="d", how="left")
    df = df.merge(df_r, on='d', how='left')
    df.rename(columns= {'v_x':'usd_blue',
                        'v_y':'usd_official',
                        'v':'international_reserves'},
                        inplace=True)
    df = df.merge(df_s, on='d', how='left')
    df.rename(columns= {'e':'event',
                        't':'event_type'},
                        inplace=True)
    df.drop(df.index[0:442],inplace=True)
    df.reset_index(drop=True, inplace=True)

    #Reemplazamos los valores nulos
    df.fillna({'event':'ninguno', 'event_type':'ninguno'}, inplace=True)
    data_cleaning(df,'usd_official')
    data_cleaning(df,'international_reserves')

    df['d'] = pd.to_datetime(df['d'])

    df_f = pd.date_range(start='2002-03-04', end='2022-08-01', freq='D')
    dfp = pd.DataFrame(df_f , columns=['d'])
    df_i['d'] = pd.to_datetime(df_i['d'])
    m = dfp.merge(df_i, on='d', how='left')
    m['month'] = m['d'].dt.strftime('%Y-%m')
    for d in list(m.month.unique()):
        new_df = m[m.month == d]
        m.loc[new_df.index,'v']= m.v[m.month == d].mean()

    df = df.merge(m, on='d', how='left')
    df.drop(['month'], axis=1, inplace=True)
    df.dropna(inplace=True)
    df.rename(columns= {'d':'date',
                        'v':'inflation'},
                        inplace=True)
    return df

# carga de datos
def load_db(df,con,name):
    try:
        df.to_sql(name=name,con=con, index=False)
    except:
        print("la tabla ya existe")