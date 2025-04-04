import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def load_data():
    df = pd.read_csv("history.csv", dtype=str)
    df = df.map(lambda x: x.replace('.', '') if isinstance(x, str) else x)
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    df['timestamp'] = pd.to_datetime(df['timestamp']) + pd.Timedelta(hours=2)
    latest = df.iloc[-1]
    return df, latest

app.layout = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col(html.H1("\U0001F4CA Données sur la dette française", className="text-center text-primary mb-4"))
    ]),

    dcc.Interval(id='interval', interval=5*60*1000, n_intervals=0),

    dbc.Row(id='stats', className="mb-4"),
    dbc.Row(id='graphs')
], fluid=True,style={'backgroundColor': '#f0f8ff'})

@app.callback(Output('stats', 'children'), Input('interval', 'n_intervals'))
def update_stats(n):
    df, latest = load_data()

    def stat_card(label, value):
        if isinstance(value, str):
            value = value.replace(".", "")
            if value.isdigit():
                value = int(value)
        if isinstance(value, float):
            value = int(value)
        formatted_value = f"{value:,}".replace(",", ".")
        suffix = " €" if "PIB" not in label and "2024" not in label and "habitant" not in label else (" %" if "PIB" in label else " €")
        return dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6(label, className="card-title"),
                html.H4(f"{formatted_value}{suffix}", className="card-text")
            ])
        ], className="shadow-sm",style={
        'backgroundColor': '#f4f4f9',
        'borderRadius': '15px',
        'padding': '20px'
    }), md=4)

    return [
        html.H3("Données actuelles :", className="mb-4"),
        dbc.Row([
            stat_card("Dette publique", latest['dette_publique']),
            stat_card("Déficit du budget de l'État", latest['deficit_budget']),
            stat_card("Dette par habitant", latest['dette_habitant']),
        ], className="gy-3"),
        html.P(f"Dernière mise à jour : {latest['timestamp']}", className="text-muted mt-3")
    ]

@app.callback(
    Output('graphs', 'children'),
    Input('interval', 'n_intervals')
)
def update_graphs(n):
    df, _ = load_data()
    return [
        html.Div(
            children=[
                dbc.Col(
                    dcc.Graph(
                        figure={
                            'data': [go.Scatter(
                                x=df['timestamp'],
                                y=df['dette_publique'],
                                mode='lines+markers',
                                name='Dette publique',
                                line={'color': '#808080', 'width': 2},
                                marker={'color': '#000000', 'size': 8}
                            )],
                            'layout': go.Layout(
                                title='Évolution de la dette publique (€)',
                                title_font={'size': 20, 'color': '#333'},
                                xaxis={'title': 'Date', 'title_font': {'size': 14, 'color': '#333'}, 'tickangle': 45},
                                yaxis={'tickformat': ',.0f', 'title_font': {'size': 14, 'color': '#333'}},
                                plot_bgcolor='#f0f8ff',
                                paper_bgcolor='#f0f8ff',
                                margin={'l': 175, 'r': 75, 't': 90, 'b': 90},
                                showlegend=False,
                                xaxis_tickangle=45,
                                autosize=True,
                                width=800,
                                height=600
                            )
                        }
                    ),
                    md=6
                ),
            ],
            style={'display': 'flex', 'justify-content': 'flex-start', 'align-items': 'center', 'height': '100vh', 'width': '100%'}
        ),
    ]


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=8080)
