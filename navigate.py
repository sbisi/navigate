# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_deck

from urllib.request import urlopen
import json
from deck_gl_example import r

# import vars
data = {
    "description": "A minimal deck.gl example rendering a circle with text",
    "initialViewState": {"longitude": -122.45, "latitude": 37.8, "zoom": 12},
    "layers": [
        {
            "@@type": "TextLayer",
            "data": [{"position": [-122.45, 37.8], "text": "Hello World"}],
        },
    ],
}
# vars.execute()
# print("*"*50, __name__)
app = Dash(__name__)
server = app.server

# GEojson file
# this file
with open("./data/geojson-counties-fips.json") as response:
    counties = json.load(response)

# map dataframe
map_df = pd.read_csv(
    "./data/fips-unemp-17.csv",
    dtype={"fips": str},
)

print(map_df)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)
print(df)

# visualisation
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
line_fig = px.line(df, x="Fruit", y="Amount", color="City")
map_fig = px.choropleth_mapbox(
    map_df,
    geojson=counties,
    locations="fips",
    color="unemp",
    color_continuous_scale="bluered",
    range_color=(0, 12),
    mapbox_style="carto-positron",
    zoom=3,
    center={"lat": 37.0902, "lon": -95.7129},
    opacity=0.5,
    labels={"unemp": "unemployment rate"},
)
map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# deck_component = dash_deck.DeckGL(r.to_json(), id="deck-gl")

# frontend
app.layout = html.Div(
    children=[
        html.H1(["Hello Dash", "another-child"]),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="example-graph", figure=fig),
        dcc.Graph(id="map", figure=map_fig),
        dcc.Graph(id="line", figure=line_fig),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
