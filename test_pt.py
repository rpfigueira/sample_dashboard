

import plotly.express as px
import pandas as pd
import json



# df = px.data.election()
df = pd.read_csv('data/portugal_municipalities.csv')

print(df.head())


#geojson = px.data.election_geojson()

# Load GeoJSON file for municipalities
with open('data/Portugal_Municipalities.geojson') as f:
    geojson = json.load(f)

# print(geojson["features"][0])

fig = px.choropleth(df, geojson=geojson, color="year",
                    locations="municipality", featureidkey="properties.Concelho",
                    projection="mercator"
                   )
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()