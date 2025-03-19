import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Charger l'historique des données
def load_history():
    try:
        df = pd.read_csv("history.csv", names=["time", "dette_publique", "dette_habitant", "deficit_secu"])
        df["time"] = pd.to_datetime(df["time"])
        return df
    except Exception as e:
        print(f"Erreur lors du chargement de l'historique: {e}")
        return pd.DataFrame(columns=["time", "dette_publique", "dette_habitant", "deficit_secu"])

# Initialiser Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Dashboard des Données Économiques"),
    
    html.Div(id="live-data"),
    
    # Graphique des séries temporelles
    dcc.Graph(id="time-series"),
    
    # Mise à jour auto toutes les 5 minutes
    dcc.Interval(
        id="interval-component",
        interval=5*60*1000,  # 5 minutes
        n_intervals=0
    )
])

# Callback pour actualiser le graphique
@app.callback(
    dash.dependencies.Output("time-series", "figure"),
    dash.dependencies.Input("interval-component", "n_intervals")
)
def update_graph(n):
    df = load_history()
    figure = go.Figure()
    
    if not df.empty:
        figure.add_trace(go.Scatter(x=df["time"], y=df["dette_publique"], mode="lines+markers", name="Dette publique"))
        figure.add_trace(go.Scatter(x=df["time"], y=df["dette_habitant"], mode="lines+markers", name="Dette par habitant"))
        figure.add_trace(go.Scatter(x=df["time"], y=df["deficit_secu"], mode="lines+markers", name="Déficit Sécu"))

    figure.update_layout(title="Évolution des Données Économiques", xaxis_title="Temps", yaxis_title="Valeurs (€)")
    
    return figure

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Dash...")
    app.run(debug=True)
