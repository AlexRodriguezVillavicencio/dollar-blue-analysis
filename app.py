from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from core.main import report1, report2, report3, report4
import pandas as pd
# from core.db import get_connection

# engine = get_connection()
# df = pd.read_sql('datablue',con=engine)                
df = pd.read_csv("data/dolarblue.csv")
# colors = {
#     'background_box': '#111111',
#     'background_body': '#383636',
#     'text': '#7FDBFF'
# }
app = Dash(__name__,title='Analisis Dolar Blue')

app.layout = html.Div([ 
    html.Div(
        className="app-header",
        children=[
            html.Div('Dólar Blue VS Dólar Oficial', className="app-header--title")
        ]),

    html.Div([
        html.Div([
            dcc.RadioItems(id='radioitems',
                            labelStyle={'display':'flex', 'margin':'10px',},
                            options=[
                                {'label':'Día con mayor variación en la brecha',
                                'value':'dia_brecha'},
                                {'label':'Top 5 días con mayor volatilidad',
                                'value':'dia_volatilidad'},
                                {'label':'Semana con mayor variación en la brecha',
                                'value':'variacion_semanal'},
                                {'label':'Día de la semana donde hay mayor variación en la brecha',
                                'value':'variacion_diaria'}
                            ], value='dia_brecha',
                            style={'text-align':'center','color':'white'})
        ], className='container_options')  
    ], className='container'),

    html.Div([
        html.Div(id='text',
                children=[html.Div([
                    html.P([{}], style={'font-size': '25px'}),
                    html.P([{}])
                ])
            ])
        ]),

    html.Div([
        html.Div([
            dcc.Graph(
                id='example-graph1',
                figure = {})
            ])
        ],className='container_fig'),  
])

@app.callback(
    Output(component_id='example-graph1', component_property='figure'),
    Input(component_id='radioitems', component_property='value')
)

def update_graph(value):

    if value == 'dia_brecha':
        fig = report1(df)
    elif value == 'dia_volatilidad':
        fig = report2(df)
    elif value == 'variacion_semanal':
        fig = report3(df)
    else:
        fig= report4(df)
    return fig

@app.callback(
    Output(component_id='text', component_property='children'),
    Input(component_id='radioitems', component_property='value')
)

def update_text(value):
    
    if value == 'dia_brecha':
        text = text = html.Div([
                html.P(['1. Día con mayor variación en la brecha'], style={'font-size': '25px'}),
                 html.P([
                    '''
                    Podemos apreciar en la gráfica los días de mayor variación, donde
                    el día 27 de Enero 2022 es el de mayor variación con un gap de 112.39 % 
                    '''
                    ], style={'font-size': '15px'})
                ], className='container_options')  
    elif value == 'dia_volatilidad':
        text = html.Div([
                html.P(['2. Top 5 días con mayor volatilidad'], style={'font-size': '25px'}),
                 html.P([
                    '''
                    Mostramos a continuación los 5 días de mayor volatilidad en %
                    '''
                    ], style={'font-size': '15px'})
                ], className='container_options')
    elif value == 'variacion_semanal':
        text = html.Div([
                html.P(['3 .Semana con mayor variación en la brecha'], style={'font-size': '25px'}),
                 html.P([
                    '''
                    En este cuadro de barras notamos que la semana 45 es la de mayor variación, 
                    esta semana comienza  el 7 de Noviembre y termina el 13 de Noviembre, con un gap de 101.71 %
                    '''
                    ], style={'font-size': '15px'})
                ], className='container_options')
    else:
        text = html.Div([
                html.P(['4. Día de la semana donde hay mayor variación en la brecha'], style={'font-size': '25px'}),
                 html.P([
                    '''
                    Los días miercoles es el resultado con mayor variación en la brecha con: 81.93 %s
                    '''
                    ], style={'font-size': '15px'})
                ], className='container_options')
    
    return text

if __name__ == '__main__':
    app.run_server(debug=True)