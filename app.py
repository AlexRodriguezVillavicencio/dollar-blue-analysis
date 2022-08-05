from dash import Dash, html, dcc
from core.main import Fig


app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig = Fig()
fig1 = fig.bar_example()

fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    showlegend=False,
    height=500,
    xaxis=dict(showgrid=False,showline=True,linecolor='rgb(255,255,255)'),
    yaxis=dict(showgrid=False)
)


app.layout = html.Div([ 
    html.Div(
        children=[
            html.Label('Dropdown'),
            dcc.Dropdown(['Dólar Blue', 'Dólar Oficial'], 'Dólar Blue'),

            html.H2(
                children='Volatilidad historica del Dólar blue',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),

            html.Div(children='calculo de 40 ruedas para los últimos 365 días', style={
                'textAlign': 'center',
                'color': colors['text']
            }),
            
            dcc.Graph(
                id='example-graph-2',
                figure=fig1
            )
        ],
        style={'backgroundColor': colors['background']}
    ),
])


if __name__ == '__main__':
    app.run_server(debug=True)