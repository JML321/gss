import dash
from dash import dcc, html, Input, Output, State, callback, dash_table  # Import dash_table directly from dash
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme  # Correct path for Format and Scheme
import pandas as pd
import os
from app_code.toolbox import compare_years_delta, unpickle, modify_answers, tooltip_headers

print("Starting dashboard.py...")

starting_name = "US Overview"

# Define the segment and its corresponding file indices based on the new system
segment_files = {
    starting_name: "melted_table_0.csv",
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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="GSS Data Analysis")

# Check if app is callable (important for Gunicorn to recognize it)
server = app.server

# Define the width for the dropdowns
cohort_width_segment, subcohort_width_segment, dropdown_width = '140px', '145px','70px'

# What Button Name Changes Too
button_labels = [("Show More Rows", 7), ("Show All Rows", 15), ("Show 7 Rows", None)]

# Attributes for dropdowns
dropdown_layout = {
    'Cohort': {'size': 2, 'offset': 3},    # Uses columns 3-4
    'Subcohort': {'size': 2, 'offset': 0}, # Centers it more effectively, uses columns 6-7
    'Timeline': {'size': 1, 'offset': 0},  # Uses columns 9-10
    'End Year': {'size': 2, 'offset': 0}   # Close to Timeline, uses columns 11-12
}



# Get values for hovering over first two columns
labels, answers = (unpickle("own_data_objects/labels.pkl"),
                   unpickle("own_data_objects/answers.pkl"))

# Define the app layout - Biggest Shifts in GSS Survey Over Time/ Largest Shifts in Public Opinion: GSS Data
# Public Opinion of USA: Sorted By Biggest Change
# "How America's Beliefs Have Changed Over Time "
# America's Beliefs: Sorted By Biggest Change Using GSS Data
# Data below sorted by biggest changes in GSS. 
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1([
        "Biggest Shifts in US Public Opinion Over Time",
        html.Span("", style={'font-size': 'small'}) # ,
        # html.A("Github", href="https://gss.norc.org/getthedata/Pages/SAS.aspx", 
        #        target="_blank", style={'font-size': 'small'})
    ], className="text-small"), width={'size': 6, 'offset': 3})),
dbc.Row([
    dbc.Col(
        dbc.Form([
            dbc.Label("Cohort", html_for="segment-dropdown"),
            dcc.Dropdown(
                id='segment-dropdown',
                options=[{'label': key, 'value': key} for key in segment_files.keys()],
                value=starting_name,
                clearable=False,
                className='dropdown',
                style={'width': cohort_width_segment}
            )
        ]), width={'size': dropdown_layout['Cohort']['size'], 'offset': dropdown_layout['Cohort']['offset']}
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
                style={'width': subcohort_width_segment}  # Start invisible
            )
        ]), width={'size': dropdown_layout['Subcohort']['size'], 'offset': dropdown_layout['Subcohort']['offset']},
        id='sub-segment-col', style={'opacity': '0', 'pointerEvents': 'none'}
    ),
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
                style={'width': dropdown_width}
            )
        ]), width={'size': dropdown_layout['Timeline']['size'], 'offset': dropdown_layout['Timeline']['offset']}
    ),
    dbc.Col(
        dbc.Form([
            dbc.Label(" ", html_for="end-year-dropdown"),
            dcc.Dropdown(
                id='end-year-dropdown',
                options=[{'label': str(year), 'value': year} for year in range(2000, 2023)
                         if year % 2 == 0 and year != 2020 or year == 2021],
                value='2022',
                clearable=False,
                className='dropdown',
                style={'position': 'absolute', 'marginTop': '4.1px', 'marginLeft': '-4px', 'width': dropdown_width}  # Positions dropdown absolutely within the form
            )
        ]), width={'size': dropdown_layout['End Year']['size'], 'offset': dropdown_layout['End Year']['offset']}
    )
    ], justify='start'),  # Adjusted justify to 'start' to align items to the left as per your previous feedback

    dbc.Row(dbc.Col(
    dbc.Form([
        dbc.Button(button_labels[0][0], id="row-button", className="me-2", n_clicks=0,
                   style={
                       'backgroundColor': '#f8f9fa',  # A light grey color
                       'color': '#495057',  # A dark grey text color
                       'fontSize': 'small',  # Smaller text
                       'border': '1px solid #ced4da'  # Add border if necessary
                   })
    ]), width=4
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
    if segment == starting_name:
        return {'opacity': '0', 'pointerEvents': 'none'}
    else:
        return {'opacity': '1', 'pointerEvents': 'auto'}

@callback(
    Output('sub-segment-dropdown', 'options'),
    Output('sub-segment-dropdown', 'value'),
    Input('segment-dropdown', 'value')
)
def update_subsegment(segment):
    print(f"Updating sub-segment dropdown for segment: {segment}")
    options = sub_segment_options.get(segment, [])
    return [{'label': opt, 'value': opt} for opt in options], options[0] if options else None

# Adjust the callback function
@callback(
    [Output('table-container', 'children'),
     Output('row-button', 'children')],
    [Input('row-button', 'n_clicks'),
     Input('segment-dropdown', 'value'),
     Input('sub-segment-dropdown', 'value'),
     Input('start-year-dropdown', 'value'),
     Input('end-year-dropdown', 'value')],
    [State('row-button', 'children')]
)
def update_output(n_clicks, segment, sub_segment, start_year, end_year, current_label):
    # Determine row count and label based on button click
    idx = n_clicks % 3
    new_label, num_rows = button_labels[idx]

    # Select the appropriate file based on segment and sub-segment
    filenames = segment_files[segment]
    filename = filenames[sub_segment_options[segment].index(sub_segment)] if isinstance(filenames, list) else filenames

    print(f"Loading data from file: {filename}")
    df = pd.read_csv(f"own_data_objects/melted_tables/{filename}")
    df = compare_years_delta(df, int(start_year), int(end_year))
    modify_answers(df, answers)

    # Generate tooltip data only for the first column
    tooltip_data = [{df.columns[0]: labels.get(df.at[idx, df.columns[0]], '')} for idx in df.index]
    tooltip_headers[2] = f"% in {end_year} - % in {start_year}" 
    tooltip_headers[3] = f"Of respondents who answered this question in {start_year}, what % had this answer"
    tooltip_headers[4] = f"Of respondents who answered this question in {end_year}, what % had the answer"

    # Return the DataTable and the new label for the button
    return (
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=num_rows if num_rows is not None else len(df),
            tooltip_data=tooltip_data,
            tooltip_header={i: j for i, j in zip(df.columns, tooltip_headers)},
            style_table={'overflowX': 'auto'},
            style_cell={
                "text-align": "center",
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
            },
            style_header={
                'fontWeight': 'bold',
                'textAlign': 'center',
                'backgroundColor': 'white',
                'whiteSpace': 'normal',
                'height': 'auto',
                'textDecoration': 'underline',
                'textDecorationStyle': 'dotted',
                'textDecorationColor': '#BEBEBE',
                'textDecorationThickness': '1px'
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgba(250, 250, 250, 1)'},
                {'if': {'row_index': 'even'}, 'backgroundColor': 'rgba(230, 230, 230, 1)'},
                {'if': {'column_id': 'Question'}, 'color': '#68748E'}
            ],
            tooltip_delay=0,
            tooltip_duration=None
        ),
        new_label
    )



if __name__ == '__main__':
    print("Running the server...")
    app.run_server(debug=True)
