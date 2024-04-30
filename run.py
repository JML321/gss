import dash, dash_table
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import os
from app_code.toolbox import compare_years_delta, unpickle

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

# Sub-segment options based on selection
sub_segment_options = {
    "Age": ["18-34", "35-50", "51-64", "65+"],
    "Degree": ["No High School", "High School", "College+"],
    "Partyid": ["Democrat", "Independent", "Republican"],
    "Sex": ["Male", "Female"],
    "Race": ["White", "Black", "Other Race"]
}

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Check if app is callable (important for Gunicorn to recognize it)
server = app.server

# Define the width for the dropdowns
dropdown_width_segment, dropdown_width = '150px', '80px'

# Get values for hovering over first two columns
labels, answers = (unpickle("own_data_objects/labels.pkl"),
                   unpickle("own_data_objects/answers.pkl"))

# Define the app layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Data Analysis Dashboard"), width={'size': 6, 'offset': 3})),
    dbc.Row([
        dbc.Col(
            dbc.Form([
                dbc.Label("Segment", html_for="segment-dropdown"),
                dcc.Dropdown(
                    id='segment-dropdown',
                    options=[{'label': key, 'value': key} for key in segment_files.keys()],
                    value='Whole Country',
                    clearable=False,
                    className='dropdown',
                    style={'width': dropdown_width_segment}
                )
            ]), width=3
        ),
        dbc.Col(
            dbc.Form([
                dbc.Label("Sub-segment", html_for="sub-segment-dropdown"),
                dcc.Dropdown(
                    id='sub-segment-dropdown',
                    options=[],
                    value=None,
                    className='dropdown',
                    style={'width': dropdown_width_segment}
                )
            ]), width=3, id='sub-segment-col', style={'display': 'none'}
        )
    ], justify='center'),
    dbc.Row([
        dbc.Col(
            dbc.Form([
                dbc.Label("Start Year", html_for="start-year-dropdown"),
                dcc.Dropdown(
                    id='start-year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in range(2000, 2023)
                             if year % 2 == 0 and year != 2020 or year == 2021],
                    value='2000',
                    clearable=False,
                    className='dropdown',
                    style={'width': dropdown_width}
                )
            ]), width=3
        ),
        dbc.Col(
            dbc.Form([
                dbc.Label("End Year", html_for="end-year-dropdown"),
                dcc.Dropdown(
                    id='end-year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in range(2000, 2023)
                             if year % 2 == 0 and year != 2020 or year == 2021],
                    value='2022',
                    clearable=False,
                    className='dropdown',
                    style={'width': dropdown_width}
                )
            ]), width=3
        )
    ], justify='center'),
    dbc.Row(dbc.Col(
        dbc.Form([
            dbc.Label("Number of Rows", html_for="num-rows-input"),
            dcc.Input(
                id='num-rows-input',
                type='number',
                value=10,
                min=1,
                className='input-number',
                style={'width': '100px'}
            )
        ]), width=2
    )),
    dbc.Row(dbc.Col(dcc.Loading(
        id="loading-output",
        type="default",
        children=html.Div(id="table-container")
    ), width=12)),
], fluid=True)

@callback(
    Output('sub-segment-col', 'style'),
    Input('segment-dropdown', 'value')
)
def toggle_subsegment(segment):
    if segment == 'Whole Country':
        return {'display': 'none'}
    else:
        return {'display': 'block'}

@callback(
    Output('sub-segment-dropdown', 'options'),
    Output('sub-segment-dropdown', 'value'),
    Input('segment-dropdown', 'value')
)
def update_subsegment(segment):
    print(f"Updating sub-segment dropdown for segment: {segment}")
    options = sub_segment_options.get(segment, [])
    return [{'label': opt, 'value': opt} for opt in options], options[0] if options else None

@callback(
    Output('table-container', 'children'),
    [Input('segment-dropdown', 'value'),
    Input('sub-segment-dropdown', 'value'),
    Input('start-year-dropdown', 'value'),
    Input('end-year-dropdown', 'value'),
    Input('num-rows-input', 'value')]
)
def update_output(segment, sub_segment, start_year, end_year, num_rows):
    filename = segment_files[segment]
    print(f"Loading data from file: {filename}")
    df = pd.read_csv(f"own_data_objects/melted_tables/{filename}")
    print(f"Data loaded, performing year comparison for years {start_year} and {end_year}")
    df = compare_years_delta(df, int(start_year), int(end_year))

    # Assuming the last three columns contain the percentage values
    # Update these columns to format as percentages with one decimal place
    percentage_columns = df.columns[-3:]  # Adjust index as necessary based on your DataFrame
    for col in percentage_columns:
        df[col] = df[col].apply(lambda x: f"{x:.1f}%")

    return dbc.Table.from_dataframe(df.head(num_rows), striped=True, bordered=True, hover=True, className='table data-table')



if __name__ == '__main__':
    print("Running the server...")
    app.run_server(debug=True)
