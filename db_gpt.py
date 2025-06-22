import pandas as pd
import plotly.express as px
import json

# Load your data
df = pd.read_csv("data/portugal_municipalities.csv")

# Aggregate by district and year
df_agg = df.groupby(['district', 'year'], as_index=False)['value_construction_type'].sum()
df_agg = df_agg.dropna(subset=['year', 'value_construction_type'])
df_agg['year'] = df_agg['year'].astype(int)

# Create mock GeoJSON
with open("data/district_pt.geojson") as f:
    real_geojson = json.load(f)



# Plot
fig = px.choropleth(
    df_agg,
    geojson=real_geojson,
    locations='district',
    featureidkey="properties.name",
    color='value_construction_type',
    animation_frame='year',
    projection="mercator",
    title="Construction Activity by District Over Time",
    labels={'value_construction_type': 'Construction Value'},
    color_continuous_scale="Viridis"
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
fig.show()