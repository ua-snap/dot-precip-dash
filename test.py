from dash import Dash
import dash_leaflet as dl
import dash_html_components as html

app = Dash(__name__)
app.layout = html.Div(
    [
        dl.Map(
            style={"width": "1000px", "height": "500px"},
            center=[56.05, 10.25],
            zoom=10,
            children=dl.TileLayer(),
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=False)
