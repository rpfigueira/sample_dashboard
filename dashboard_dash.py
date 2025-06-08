import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('data/portugal_municipalities.csv')


# Get unique values for dropdowns
available_columns = ['construction_type', 'dwelling_type', 'type']

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
 html.H1("Portugal Municipalities Dashboard"),

 html.Div([
 html.Label("Select Data Column:"),
 dcc.Dropdown(
 id='data-column-dropdown',
 options=[{'label': i, 'value': i} for i in available_columns],
 value='construction_type', # Default value
 clearable=False
 )
 ], style={'width': '30%', 'display': 'inline-block'}),

 html.Div([
 # Map on the left
 html.Div([
 dcc.Graph(id='portugal-map', style={'height': '90vh'})
 ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}),

 # Panels with bar charts on the right
 html.Div([
 # First bar chart panel
 html.Div([
 html.H3("Bar Chart 1"),
 dcc.Graph(id='bar-chart-1')
 ], style={'height': '45vh', 'border': '1px solid black', 'marginBottom': '10px'}),

 # Second bar chart panel
 html.Div([
 html.H3("Bar Chart 2"),
 dcc.Graph(id='bar-chart-2')
 ], style={'height': '45vh', 'border': '1px solid black'})
 ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '2%'})
 ])
])

# Callback to update the first bar chart
@app.callback(
    Output('bar-chart-1', 'figure'),
    [Input('data-column-dropdown', 'value')]
)
def update_bar_chart_1(selected_column):
    """
    Updates the bar chart based on the selected data column from the dropdown.
    The chart displays values per year, categorized by the selected column.
    """
    value_col_to_sum = None
    if selected_column == 'construction_type':
        value_col_to_sum = 'value_construction_type'
    elif selected_column == 'dwelling_type':
        # 'dwelling_type' is from the same source as 'construction_type' and uses its value column
        value_col_to_sum = 'value_construction_type'
    elif selected_column == 'type': # This 'type' is from the dwelling dataset
        value_col_to_sum = 'value_dwelling_type'
    else:
        # Fallback for an unexpected column, though dropdown is not clearable and has fixed options
        return px.bar(title=f"Invalid column selected: {selected_column}")

    if value_col_to_sum not in df.columns:
        return px.bar(title=f"Required value column '{value_col_to_sum}' not found.")

    # Prepare data for the chart
    dff = df.copy()
    # Ensure the value column is numeric, converting errors to NaN
    dff[value_col_to_sum] = pd.to_numeric(dff[value_col_to_sum], errors='coerce')

    # Remove rows where essential data for grouping or summing is missing
    dff_chart = dff.dropna(subset=['year', selected_column, value_col_to_sum])

    if dff_chart.empty:
        return px.bar(title=f"No data to display for {selected_column} after filtering.")

    # Group by year and the selected column's categories, then sum the values
    grouped_data = dff_chart.groupby(['year', selected_column], as_index=False)[value_col_to_sum].sum()

    fig = px.bar(grouped_data, x='year', y=value_col_to_sum, color=selected_column,
                 title=f'Value of {selected_column} per Year', barmode='group')
    fig.update_xaxes(type='category') # Treat 'year' as a categorical axis
    return fig

# Run the app
if __name__ == '__main__':
 app.run(debug=True)
