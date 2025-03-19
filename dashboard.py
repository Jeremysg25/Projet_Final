import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import time

# Charger les données
def load_data():
    try:
        with open("data.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            data = {line.split(":")[0]: line.split(":")[1].strip() for line in lines}
        return data
    except:
        return {}

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Layout du Dashboard
app.layout = html.Div([
    html.H1("📊 Dashboard des Données Économiques"),
    
    html.Div(id="live-data"),
    
    dcc.Graph(id="time-series"),
    
    dcc.Interval(
        id="interval-component",
        interval=5*60*1000,  # 5 minutes
        n_intervals=0
    )
])

# Callback pour mettre à jour les données affichées
@app.callback(
    dash.dependencies.Output("live-data", "children"),
    dash.dependencies.Input("interval-component", "n_intervals")
)
def update_data(n):
    data = load_data()
    return html.Ul([html.Li(f"{key}: {value}") for key, value in data.items()])

# Callback pour mettre à jour le graphique
@app.callback(
    dash.dependencies.Output("time-series", "figure"),
    dash.dependencies.Input("interval-component", "n_intervals")
)
def update_graph(n):
    try:
        df = pd.read_csv("history.csv")  # Fichier où l'on stocke l'historique
        figure = go.Figure()
        figure.add_trace(go.Scatter(x=df["time"], y=df["dette_publique"], mode="lines", name="Dette publique"))
        return figure
    except:
        return go.Figure()

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Dash...")
    app.run(debug=True)
