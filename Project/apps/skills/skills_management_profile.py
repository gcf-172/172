from urllib.parse import parse_qs, urlparse
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from dash import Input, Output, State
from app import app
from dbconnect import getDataFromDB, modifyDB
from dash.exceptions import PreventUpdate

layout = html.Div(
    [
        dcc.Store(id='skillprofile_id', storage_type='memory', data=0),
        dbc.Row(
            [
                dbc.Col(html.H2(id="skill_profile_header", style={'font-size': '25px'}), width="auto"),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/skills",
                        style={
                            "borderRadius": "20px",
                            "fontWeight": "bold",
                            "fontSize": "16px",
                            "marginRight": "10px",
                            "backgroundColor": "#194D62"
                        }
                    ),
                    width="auto"
                ),
            ],
            align="center",
            className="mb-4"
        ),
        
        html.Hr(),
        
        # Form Layout
        dbc.Form(
            [

                # Skill Name
                dbc.Row(
                    [
                        dbc.Label("Skill Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='skill_name',
                                placeholder='Enter Skill Name',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Skill Description
                dbc.Row(
                    [
                        dbc.Label("Skill Description", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='skill_description',
                                placeholder='Enter Description',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
             
                html.Div(
                    [
                        dbc.Checklist(
                            id='skill_profile_delete',
                            options=[dict(value=1, label="Mark as Deleted")],
                            value=[]
                        )
                    ],
                    id='skillprofile_deletediv'
                ),

                dbc.Button(
                    "Submit", 
                    color="primary", 
                    className="mt-3 mb-3",
                    id='skillsubmit_button',
                    style={
                        "borderRadius": "20px",
                        "fontWeight": "bold",
                        "fontSize": "18px",
                        "backgroundColor": "#194D62",
                        "color": "white"
                    },
                )
            ]
        ),
        dbc.Alert(id='skillsubmit_alert', is_open=False)
    ],
    className="container mt-4"
)
#Hides Mark as Deleted During Add Mode
@app.callback(
    [
        Output('skillprofile_id', 'data'),
        Output('skillprofile_deletediv', 'className')
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def skill_profile_load(pathname, urlsearch):
    if pathname == '/skills/skills_management_profile':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            skillprofile_id = 0
            deletediv = 'd-none'
            
        else:
            skillprofile_id = int(parse_qs(parsed.query).get('id', [0])[0])
            deletediv =''
        
        return [skillprofile_id, deletediv]
    else:
        raise PreventUpdate
#Dynamic Header
@app.callback(
    Output('skill_profile_header', 'children'),
    Input('url', 'search')
)
def update_header(urlsearch):
    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]
    
    if create_mode == 'add':
        return "Add New Skill"
    else:
        return "Edit Skill Details"
#This inserts into database
@app.callback(
    [Output('skillsubmit_alert', 'color'),
     Output('skillsubmit_alert', 'children'),
     Output('skillsubmit_alert', 'is_open')],
    [Input('skillsubmit_button', 'n_clicks')],
    [State('skill_name', 'value'),
     State('skill_description', 'value'),
     State('skill_profile_delete', 'value'),
     State('url', 'search'),
     State('skillprofile_id', 'data')]
)
def submit_form(n_clicks, skill_name, skill_description, skill_delete, urlsearch, skillprofile_id):
    
    ctx = dash.callback_context
    if not ctx.triggered or not n_clicks:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    # Check for missing values in the required fields
    if not all([skill_name, skill_description]):
        return 'danger', 'Please fill in all required fields.', True

    # Determine if the client is marked for deletion
    delete_flag = True if skill_delete else False

    # SQL to insert or update the database
    if create_mode == 'add':
        sql = """INSERT INTO skills (skill_m, skill_description, skill_delete_ind)
                VALUES (%s, %s, %s);"""        
        values = [skill_name, skill_description, delete_flag]
        success_message = "New Skill Added Successfully!"
    
    elif create_mode == 'edit':
        sql = """UPDATE skills
                SET skill_m = %s,
                    skill_description = %s,
                    skill_delete_ind = %s
                WHERE skill_id = %s;"""        
        values = [skill_name, skill_description, delete_flag, skillprofile_id]
        success_message = "Skill Details Updated Successfully!"
    else:
        raise PreventUpdate

    try:
        modifyDB(sql, values)
        return 'success', success_message, True
    except Exception as e:
        return 'danger', f'Error Occurred: {e}', True

#This prepopulates during edit mode
@app.callback(
    [Output('skill_name', 'value'),
    Output('skill_description', 'value'),
    ],
    [Input('skillprofile_id', 'modified_timestamp'),],

    [State('skillprofile_id', 'data'),]
)
def skill_profile_populate(timestamp, skillprofile_id):
    if skillprofile_id > 0:
        sql = """SELECT skill_m, skill_description
                FROM skills
                WHERE skill_id = %s"""
        values = [skillprofile_id]
        col = ['skill_name', 'skill_description']

        df = getDataFromDB(sql, values, col)

        skillname = df['skill_name'][0]
        skilldescription = df['skill_description'][0]

        return [skillname, skilldescription]
    else:
        raise PreventUpdate
