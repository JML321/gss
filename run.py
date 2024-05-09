import dash
from dash import dcc, html, Input, callback_context, Output, ClientsideFunction, State, callback, dash_table  # Import dash_table directly from dash
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme  # Correct path for Format and Scheme
from dash_extensions import EventListener
from dash.exceptions import PreventUpdate
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
big_width_segment, small_width_segment = '100%','27%'
label_size = '1.55vw'
font_size = '1.5vw'
footer_size = '13px'

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

    # detect when tooltip has been activated
     html.Div(id='tooltip-store', style={'display': 'none'}),
     # Inside your layout definition, add this line:
     dcc.Store(id='label-index-store', data={'index': 0}),
     dcc.Store(id='memory', data={'index': False}),
     html.Div([
        dcc.Input(id='store', type='hidden', value=-3),
        EventListener(
            id='tooltip-listener',
            events=[{'event': 'custom-tooltip-detected', 'props': ['srcElement.id']}],
            children=html.Div(id="tooltip-detector")  # Placeholder for the event listener
        )
    ]),
    # Header
    dbc.Row(dbc.Col(html.H1([
        "Biggest Shifts in US Public Opinion Over Time",
        html.Span("", style={'fontSize': 'small'}) # ,
        # html.A("Github", href="https://gss.norc.org/getthedata/Pages/SAS.aspx", 
        #        target="_blank", style={'font-size': 'small'})
    ], className="text-small"), width={'size': 6, 'offset': 3})),

    # Four buttons
    dbc.Row([
        dbc.Col(
            dbc.Form([  
                dbc.Label("Cohort", id="Cohort", 
                          html_for="segment-dropdown", style={'fontSize': label_size}),
                dcc.Dropdown(
                    id='segment-dropdown',
                    options=[{'label': key, 'value': key} for key in segment_files.keys()],
                    value=starting_name,
                    clearable=False,
                    searchable=False,
                    style={'width': big_width_segment, 'fontSize': font_size, 
                        'marginLeft': '-1px'}
                )
            ]), width={'size': dropdown_layout['Cohort']['size'], 
                       'offset': dropdown_layout['Cohort']['offset']},
        ),
        dbc.Col(
            dbc.Form([
                dbc.Label("Subcohort", id="SubCohort",
                          html_for="sub-segment-dropdown", style={'fontSize': label_size}),
                dcc.Dropdown(
                    id='sub-segment-dropdown',
                    options=[],
                    value=None,
                    clearable=False,
                    className = 'show-arrow',
                    searchable=False,
                    style={'width': big_width_segment, 
                         'fontSize': font_size}  
                )
            ]), width={'size': dropdown_layout['Subcohort']['size'], 
                       'offset': dropdown_layout['Subcohort']['offset']},
                id='sub-segment-col', 
                style={'opacity': '0', 'pointerEvents': 'none', 'marginLeft': '-50px'}
        ),
        dbc.Col(
            dbc.Form([
                dbc.Label("Timeline", id="Timeline",
                          html_for="start-year-dropdown", style={'fontSize': label_size}),
                dcc.Dropdown(
                    id='start-year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in range(2000, 2023)
                            if year % 2 == 0 and year != 2020 or year == 2021],
                    value='2000',
                    clearable=False,
                    className='dropdown', #dropdown_width
                    style={'width': small_width_segment,'position': 'absolute', 'marginLeft': '0px',
                        'fontSize': font_size}
                )
            ]), width={'size': dropdown_layout['Timeline']['size'], 
                       'offset': dropdown_layout['Timeline']['offset']}
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
                    className='dropdown', # dropdown_width
                    style={'position': 'absolute', 'marginTop': '4.1px', 
                        'marginLeft': '-4px', 'width': small_width_segment,
                        'fontSize': font_size}  # Positions dropdown absolutely within the form
                )
            ]), width={'size': dropdown_layout['End Year']['size'], 'offset': dropdown_layout['End Year']['offset']}
        )
        ], justify='start'),  # Adjusted justify to 'start' to align items to the left as per your previous feedback
    
    # Button that each time click, different thing shows. Controls rows
    dbc.Row(dbc.Col(
    dbc.Form([
        dbc.Button(button_labels[0][0], id="row-button", className="me-2", n_clicks=0,
                   style={
                       'backgroundColor': '#f8f9fa',  # A light grey color
                       'border': '1px solid #ced4da',  # Add border if necessary
                       'fontSize': "3.0vw"
                    })
        ]), width=4, 
    ), style={'marginTop': '5px'}),

    # Creating a Table
    dbc.Row(dbc.Col(dcc.Loading(
        id="loading-output",
        type="default",
        children=html.Div(id="table-container")
    ), width=12)),

    # For JavaScript to manipulate styles based on screen width
    html.Div(id='screen-width-storage', style={'display': 'none'}),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),

    # Footer
    dbc.Row(
        dbc.Col(
            html.Footer(
                [
                    "Data Source: ",
                    html.A("GSS", href="https://gss.norc.org/getthedata/Pages/SAS.aspx", style={'fontSize': footer_size}),
                ],
                style={'fontSize': footer_size}
            ),
            width=12
        )
    )

], fluid=True, style={'backgroundColor': '#f4f4f9'})

first_message = "Hover Over Question or Header for More Info"
@app.callback(
    [Output('row-button', 'children'),
     Output('row-button', 'style'),
     Output('label-index-store', 'data'),
     Output('memory', 'data')],  # Update store data
    [Input('tooltip-listener', 'n_events'),
     Input('row-button', 'n_clicks')],
    [State('label-index-store', 'data'),
     State('memory', 'data')]  # Get current index from store
)
def handle_tooltip_activation(n_events, n_clicks, store_data, memory):
    font_size_rowButton = "1.4vw"
    default_style = {'backgroundColor': 'f8f9fa', 'color': 'blue', 'fontSize': font_size_rowButton, "width": "70%"}
    first_message = "Hover Over Question or Header for More Info"
    print("n_events ", n_events)
    memory_value = memory.get('index', False)
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigger == 'tooltip-listener' and n_events >=2:
        raise PreventUpdate

    if n_events == 0 or n_events is None:
        # Reset index when no events are active
        store_data['index'] = 0
        return (first_message, default_style, store_data, memory)

    new_style = {'backgroundColor': '#f8f9fa', 'color': '#495057', 'fontSize': font_size_rowButton, 'border': '1px solid #ced4da'}
    # Extract the current index from the store data
    current_index = store_data.get('index', 0)

    # Check if n_clicks has changed
    if trigger == 'row-button':
        # Get label and increment index
        label, _ = button_labels[current_index]
        current_index = (current_index + 1) % len(button_labels)  # Cycle through labels

        # Update store with new index
        store_data['index'] = current_index

    # If n_clicks hasn't changed, return the current label and style
    label, _ = button_labels[current_index]
    if memory_value == False:
        if n_events is not None and n_events >= 1 and store_data['index'] >= 1:
            memory['index']=True
    return (label, new_style, store_data, memory)

# Callback to manage sub-segment dropdown
@callback(
        Output('sub-segment-dropdown', 'className'),
        Output('sub-segment-dropdown', 'disabled'),
        Input('segment-dropdown', 'value')
    )
def update_subsegment_dropdown(segment):
        if segment == starting_name:
            return 'hide-arrow', True
        else:
            return 'show-arrow', False

# Single callback to handle both the visibility and options of the sub-segment dropdown
@callback(
    [
        Output('sub-segment-col', 'style'),  # Adjusts the visibility of the column
        Output('sub-segment-dropdown', 'options'),  # Adjusts the options in the dropdown
        Output('sub-segment-dropdown', 'value'),
    ],
    [Input('segment-dropdown', 'value')]  # Triggered by changes in the cohort dropdown
)
def update_subsegment_visibility_and_options(segment):
    if segment == starting_name:
        # When the "US Overview" is selected
        return {'opacity': '1', 'pointerEvents': 'auto'}, \
               [{'label': '(None)', 'value': 'none'}], \
               'none'
    else:
        print(f"Selected segment: {segment}")
        # For all other segment selections
        options = sub_segment_options.get(segment, [])
        return {'opacity': '1', 'pointerEvents': 'auto'}, \
               [{'label': opt, 'value': opt} for opt in options], \
               options[0] if options else None
# Adjust the callback function
@callback(
     Output('table-container', 'children'),
    [Input('segment-dropdown', 'value'),
     Input('sub-segment-dropdown', 'value'),
     Input('start-year-dropdown', 'value'),
     Input('end-year-dropdown', 'value'),
     Input('label-index-store', 'data')],
     [State('memory', 'data'),
      State('tooltip-listener', 'n_events')]
)
def update_output(segment, sub_segment, start_year, 
                  end_year, store_data, memory,
                  n_events):
    print("store_data ", store_data)
    print("memory ", memory)
    print("n_events ", n_events)
    if n_events is not None and n_events != 0:
        if memory.get('index', False) == False:
            raise PreventUpdate
    # Determine row count and label based on button click
    trigger = dash.callback_context.triggered[0]
    trigger_id = trigger['prop_id'].split('.')[0]
    # print("trigger_id ", trigger_id)
    # print("store_data ", store_data)
    if trigger_id == 'row-button':
        current_index = (store_data.get('index', 0) + 1) % 3
        _, num_rows = button_labels[current_index]
    else:
        num_rows = button_labels[store_data.get('index', 0)][1]
    # Select the appropriate file based on segment and sub-segment
    filenames = segment_files[segment]
    filename = filenames[sub_segment_options[segment].index(sub_segment)] if isinstance(filenames, list) else filenames

    # print(f"Loading data from file: {filename}")
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
                'whiteSpace': 'normal',
                'height': 'auto',
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
                # vivid_blue_colors = ['#89A3C1', '#4B9CD3', '#1E84C6', '#0086CF', '#007BFF']
                {'if': {'column_id': 'Question'}, 'color': '#0086CF'}
            ],
            tooltip_delay=0,
            tooltip_duration=None
        )
    )


if __name__ == '__main__':
    print("Running the server...")
    app.run_server(debug=True)
