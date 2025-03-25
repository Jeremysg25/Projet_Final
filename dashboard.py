import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go


# Chargement des données
df = pd.read_csv("history.csv", header=None, names=[
    "timestamp", "dette_publique", "dette_habitant", "deficit_secu",
    "dette_pib", "deficit_budget", "deficit_2024"
])

# Dernière ligne pour les valeurs textuelles
latest = df.iloc[-1]

# Création de l'app Dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Dashboard - Données Économiques'),

    html.Div(children=[
        html.H3("Données actuelles :"),
        html.P(f"Dette publique : {latest['dette_publique']} €"),
        html.P(f"Déficit du budget de l'État : {latest['deficit_budget']} €"),
        html.P(f"Dette par habitant : {latest['dette_habitant']}"),
        html.P(f"Déficit sécurité sociale : {latest['deficit_secu']}"),
        html.P(f"Dette publique / PIB : {latest['dette_pib']}"),
        html.P(f"Déficit budgétaire prévu en 2024 : {latest['deficit_2024']}"),
    ]),

    html.Div(children=[
        dcc.Graph(
            id='graph-dette-publique',
            figure={
                'data': [go.Scatter(
                    x=df['timestamp'],
                    y=df['dette_publique'],
                    mode='lines+markers',
                    name='Dette publique'
                )],
                'layout': go.Layout(
                    title='Évolution de la dette publique (€)',
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Montant'}
                )
            }
        ),
        dcc.Graph(
            id='graph-deficit-budget',
            figure={
                'data': [go.Scatter(
                    x=df['timestamp'],
                    y=df['deficit_budget'],
                    mode='lines+markers',
                    name='Déficit du budget de l\'État'
                )],
                'layout': go.Layout(
                    title='Évolution du déficit du budget de l\'État (€)',
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Montant'}
                )
            }
        )
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
