from urllib.request import urlopen
import json

# Load GeoJSON file for municipalities
with open('data/geojson-counties-fips.json') as f:
    counties = json.load(f)

import pandas as pd
df = pd.read_csv("data/fips-unemp-16.csv",
                   dtype={"fips": str})

import plotly.express as px

fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()