import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import os
from code.toolbox import compare_years_delta

print("Starting dashboard.py...")

# Define the segment and its corresponding file indices
segment_files = {
    "Whole Country": "melted_table_0.csv",
    "Age": "melted_table_1.csv",
    "Degree": "melted_table_2.csv",
    "Partyid": "melted_table_3.csv",
    "Sex": "melted_table_4.csv",
    "Race": "melted_table_5.csv"
}

print(f"Segment files: {segment_files}")

# Sub-segment options based on selection
sub_segment_options = {
    "Age": ["18-34", "35-50", "51-64", "65+"],
    "Degree": ["No High School", "High School", "College+"],
    "Partyid": ["Democrat", "Independent", "Republican"],
    "Sex": ["Male", "Female"],
    "Race": ["White", "Black", "Other Race"]
}

print("Initializing the Dash app...")
# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
print("Dash app initialized.")

# Check if app is callable (important for Gunicorn to recognize it)
print("App is callable:", callable(app))
print("Type of app:", type(app))
print("App.server is callable:", callable(app.server))
print("Type of app.server:", type(app.server))
server = app.server


# Define the app layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Data Analysis Dashboard"), width={'size': 6, 'offset': 3})),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='segment-dropdown',
            options=[{'label': key, 'value': key} for key in segment_files.keys()],
            value='Whole Country',
            clearable=False,
            className='dropdown'
        ), width=3),
        dbc.Col(dcc.Dropdown(
            id='sub-segment-dropdown',
            options=[],
            value=None,
            className='dropdown'
        ), width=3)
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='start-year-dropdown',
            options=[{'label': str(year), 'value': year} for year in range(2000, 2023) if year != 2020 or year == 2021],
            value='2000',
            clearable=False,
            className='dropdown'
        ), width=3),
        dbc.Col(dcc.Dropdown(
            id='end-year-dropdown',
            options=[{'label': str(year), 'value': year} for year in range(2000, 2023) if year != 2020 or year == 2021],
            value='2022',
            clearable=False,
            className='dropdown'
        ), width=3)
    ]),
    dbc.Row(dbc.Col(dcc.Input(
        id='num-rows-input',
        type='number',
        value=10,
        min=1,
        className='input-number'
    ), width=2)),
    dbc.Row(dbc.Col(dcc.Loading(
        id="loading-output",
        type="default",
        children=html.Div(id="table-container")
    ), width=12)),
], fluid=True)

print("Dash layout set up.")

if __name__ == '__main__':
    print("Running the server...")
    app.run_server(debug=True)
