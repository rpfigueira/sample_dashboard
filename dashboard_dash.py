import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('data/portugal_municipalities.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Portugal Municipalities Dashboard"),

    dcc.Graph(
        id='population-graph',
        figure=px.bar(df, x='municipality', y='population', title='Population by Municipality')
    ),

    dcc.Graph(
        id='area-graph',
        figure=px.bar(df, x='municipality', y='area_km2', title='Area by Municipality (km²)')
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
