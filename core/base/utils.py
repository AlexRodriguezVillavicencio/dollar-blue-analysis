import numpy as np
import plotly.graph_objects as go
import pandas as pd
from scipy.signal import find_peaks


def join_url(url:str,base:str) -> str:
    if list(url)[-1] == '/':
        new_url = url +base
    else:
        new_url = url +'/' +base
    return new_url


def data_cleaning(df,feature:str):
    drop_list = []
    for i in list(zip(*np.where(df[feature].isna()))):
        ii = i[0]
        drop_list.append(ii)
    df.drop(drop_list, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def get_peaks(df,feature:str, prominence:int) -> tuple:
    peak_blue, _ = find_peaks(df[feature], prominence=prominence)

    listd = []
    listv = []
    for i in peak_blue:
        d = list(df[df.index == i].date)[0]
        v = list(df[df.index == i][feature])[0]
        listd.append(d)
        listv.append(v)

    df_top = pd.DataFrame()
    df_top['date'] =listd
    df_top['top'] =listv
    list_top = list(df_top['date'])
    return df_top,list_top


def plot_goHistorical(xl,yl,namel, xp,yp,namep, list_top):
    fig= go.Figure()
    fig.add_trace(go.Scatter(x=xl,
                                y=yl,
                                mode='lines',
                                name=namel))
    fig.add_trace(go.Scatter(x=xp,
                                y=yp,
                                mode='markers + text',
                                name=namep,
                                marker=dict(color='red',size=12),
                                text = list_top,
                                textposition="top center"))
    fig.update_xaxes(
            rangeselector=dict(
                    buttons=list([
                            dict(count=1, label='Ultimo Mes', step='month', stepmode='backward'),
                            dict(count=6, label='Ultimos 6 Meses', step='month', stepmode='backward'),
                            dict(label='Ultimos 12 Meses' , step='all')
                    ])
            ))
#     fig.update_layout(
#         plot_bgcolor='#111111',
#         paper_bgcolor= '#111111',
#         font_color='#cee3e1',
#         xaxis=dict(showgrid=False,showline=True,linecolor='rgb(255,255,255)'),
#         yaxis=dict(showgrid=False),
# )
    return fig