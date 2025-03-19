import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import datetime

# Charger l'historique des données
def load_history():
    try:
        df = pd.read_csv("history.csv", names=["time", "dette_publique", "dette_habitant", "deficit_secu"])
        df["time"] = pd.to_datetime(df["time"])
        return df
    except Exception as e:
        print(f"Erreur lors du chargement de l'historique: {e}")
        return pd.DataFrame(columns=["time", "dette_publique", "dette_habitant", "deficit_secu"])

# Charger les dernières valeurs depuis data.txt
def load_latest_data():
    try:
        with open("data.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            data = {line.split(":")[0]: line.split(":")[1].strip() for line in lines}
        return data
    except:
        return {}

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

# Callback pour afficher les dernières valeurs scrappées
@app.callback(
    dash.dependencies.Output("live-data", "children"),
    dash.dependencies.Input("interval-component", "n_intervals")
)
def update_live_data(n):
    data = load_latest_data()
    return html.Ul([html.Li(f"{key}: {value}") for key, value in data.items()])

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

# Générer un rapport quotidien à 20h
def generate_daily_report():
    df = load_history()
    if df.empty:
        return
    
    latest = df.iloc[-1]
    report_content = f"""
    📅 Rapport du {datetime.datetime.now().strftime("%Y-%m-%d")}
    ---------------------------------------------------
    ➜ Dette publique: {latest["dette_publique"]} €
    ➜ Dette par habitant: {latest["dette_habitant"]} €
    ➜ Déficit Sécurité sociale: {latest["deficit_secu"]} €
    """

    with open("daily_report.txt", "w", encoding="utf-8") as file:
        file.write(report_content)

    print("📄 Rapport quotidien généré.")

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Dash...")
    generate_daily_report()  # Générer le rapport chaque lancement
    app.run(debug=True)

