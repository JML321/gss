import dash
from dash import dcc, html, Input, Output, callback, dash_table  # Import dash_table directly from dash
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme  # Correct path for Format and Scheme
import pandas as pd
import os
from app_code.toolbox import compare_years_delta, unpickle, modify_answers

print("Starting dashboard.py...")

# Define the segment and its corresponding file indices based on the new system
segment_files = {
    "Whole Country": "melted_table_0.csv",
    "Age": ["melted_table_1.csv", "melted_table_2.csv", "melted_table_3.csv", "melted_table_4.csv"],
    "Degree": ["melted_table_5.csv", "melted_table_6.csv", "melted_table_7.csv"],
    "Partyid": ["melted_table_8.csv", "melted_table_9.csv", "melted_table_10.csv"],
    "Sex": ["melted_table_11.csv", "melted_table_12.csv"],
    "Race": ["melted_table_13.csv", "melted_table_14.csv", "melted_table_15.csv"]
}

# Sub-segment options based on selection
sub_segment_options = {
    "Age": ["18-34", "35-49", "50-64", "65+"],
    "Degree": ["No High School", "High School", "College+"],
    "Partyid": ["Democrat", "Independent/ Other", "Republican"],
    "Sex": ["Male", "Female"],
    "Race": ["White", "Black", "Other"]
}

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Yo")

# Check if app is callable (important for Gunicorn to recognize it)
server = app.server

# Define the width for the dropdowns
dropdown_width_segment, dropdown_width = '150px', '80px'

# Get values for hovering over first two columns
labels, answers = (unpickle("own_data_objects/labels.pkl"),
                   unpickle("own_data_objects/answers.pkl"))

# Define the app layout - Biggest Shifts in GSS Survey Over Time
# Data below sorted by biggest changes in GSS. 
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Largest Shifts in Public Opinion: GSS Data"), width={'size': 6, 'offset': 3})),
    # dbc.Row(dbc.Col(html.H6("Choose demographics and timeline"), width={'size': 6, 'offset': 3})),
    dbc.Row([
        dbc.Col(
            dbc.Form([
                dbc.Label("Cohort", html_for="segment-dropdown"), # "Demographic"
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
                dbc.Label("Subcohort", html_for="sub-segment-dropdown"),
                dcc.Dropdown(
                    id='sub-segment-dropdown',
                    options=[],
                    value=None,
                    clearable=False,
                    className='dropdown',
                    style={'width': dropdown_width_segment}
                )
            ]), width=3, id='sub-segment-col', style={'display': 'none'}
        ),

    # ], justify='center'),
    # dbc.Row([

        dbc.Col(
            dbc.Form([
               dbc.Label("Timeline", html_for="start-year-dropdown"),
                dcc.Dropdown(
                    id='start-year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in range(2000, 2023)
                             if year % 2 == 0 and year != 2020 or year == 2021],
                    value='2000',
                    clearable=False,
                    className='dropdown',
                    style={'width': dropdown_width, 'marginBottom': '0px'}  # Removes the bottom margin
                )
            ]), width=1
        ),
        dbc.Col(
            dbc.Form([
                dbc.Label("", html_for="end-year-dropdown"),
                dcc.Dropdown(
                    id='end-year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in range(2000, 2023)
                             if year % 2 == 0 and year != 2020 or year == 2021],
                    value='2022',
                    clearable=False,
                    className='dropdown',
                    style={'width': dropdown_width, 'marginTop': '8px'}  # Removes the top margin
                )
            ]), width=3
        )
    ], justify='center'),
    dbc.Row(dbc.Col(
        dbc.Form([
            dbc.Label("Rows", html_for="num-rows-input"),
            dcc.Input(
                id='num-rows-input',
                type='number',
                value=5,
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
], fluid=True, style={'backgroundColor': '#f4f4f9'})


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
    filenames = segment_files[segment]
    # If there are multiple files for the segment, choose based on the sub_segment
    if isinstance(filenames, list):
        # Find the index of the sub_segment in the options list
        sub_index = sub_segment_options[segment].index(sub_segment)
        filename = filenames[sub_index]
    else:
        filename = filenames  # Use single filename directly if not a list

    print(f"Loading data from file: {filename}")
    df = pd.read_csv(f"own_data_objects/melted_tables/{filename}")
    print(f"Data loaded, performing year comparison for years {start_year} and {end_year}")
    df = compare_years_delta(df, int(start_year), int(end_year))
    # df.iloc[:, -3:] = df.iloc[:, -3:] / 100
    modify_answers(df, answers)

    # Generate tooltip data only for the first column
    tooltip_data = [
        {df.columns[0]: labels.get(df.at[idx, df.columns[0]], '')}
        for idx in df.index
    ]

    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
           # {
             #   'name': i, 'id': i, 'type': 'numeric', 
             #'format': Format(precision=1, scheme=Scheme.percentage)} if i in df.columns[-3:] 
            # else 
            {'name': i, 'id': i}
            for i in df.columns
        ],
        tooltip_data=tooltip_data,
        page_size=num_rows,
        style_table={'overflowX': 'auto'},
        style_cell={
            "text-align": "center",
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
        },
        style_header={
        'fontWeight': 'bold',  # Adds bold font style to headers
        'textAlign': 'center',
        'backgroundColor': 'white',
        'whiteSpace': 'normal',  # Allow header texts to wrap
        'height': 'auto' 
        },
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgba(250, 250, 250, 1)'
        },
        {
            'if': {'row_index': 'even'},
            'backgroundColor': 'rgba(230, 230, 230, 1)'
        }
        ],
        tooltip_delay=0,
        tooltip_duration=None
    )



if __name__ == '__main__':
    print("Running the server...")
    app.run_server(debug=True)
