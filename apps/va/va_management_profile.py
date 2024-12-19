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
        dcc.Store(id='vaprofile_id', storage_type='memory', data=0),
        dbc.Row(
            [
                dbc.Col(html.H2(id="va_profile_header", style={'font-size': '25px'}), width="auto"),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/va_profile",
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

                # First Name
                dbc.Row(
                    [
                        dbc.Label("First Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='vafirst_name',
                                placeholder='Enter First Name',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Last Name
                dbc.Row(
                    [
                        dbc.Label("Last Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='valast_name',
                                placeholder='Enter Last Name',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Email Address
                dbc.Row(
                    [
                        dbc.Label("Email Address", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='email',
                                id='vaemail_address',
                                placeholder='Enter Email Address',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Address
                dbc.Row(
                    [
                        dbc.Label("Address", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='address',
                                placeholder='Enter Address',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                #Skills Checklist
                dbc.Row(
                    [
                        dbc.Label("Skills", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Checklist(
                                    id='va_skills',
                                    style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                                ),
                                className='dash-bootstrap'
                            ),
                            width=8,
                        )
                    ],
                    className='mb-3'
                ), 
                
                # Date hired
                dbc.Row(
                    [
                        dbc.Label("Date hired", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='date',
                                id='date_hired',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Status
                dbc.Row(
                    [
                        dbc.Label("Status", width=2),
                        dbc.Col(
                            dbc.Select(
                                id='va_status',
                                options=[
                                    {'label': 'ACTIVE', 'value': 'ACTIVE'},
                                    {'label': 'INACTIVE', 'value': 'INACTIVE'},
                                    {'label': 'ON HOLD', 'value': 'ON HOLD'}
                                ],
                                placeholder='Select Status',
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
                            id='va_profile_delete',
                            options=[dict(value=1, label="Mark as Deleted")],
                            value=[]
                        )
                    ],
                    id='vaprofile_deletediv'
                ),

                dbc.Button(
                    "Submit", 
                    color="primary", 
                    className="mt-3 mb-3",
                    id='vasubmit_button',
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
        dbc.Alert(id='vasubmit_alert', is_open=False)
    ],
    className="container mt-4"
)
#Hides Mark as Deleted During Add Mode
@app.callback(
    [
        Output('va_skills', 'options'),
        Output('vaprofile_id', 'data'),
        Output('vaprofile_deletediv', 'className')
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def va_profile_load(pathname, urlsearch):
    if pathname == '/va_profile/va_management_profile':
        # Fetch Skills
        sql = """
        SELECT skill_m as label, skill_id as value
        FROM skills
        """
        values = []
        cols = ['label', 'value']
        df = getDataFromDB(sql, values, cols)
        skill_options = df.to_dict('records')

        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            vaprofile_id = 0
            deletediv = 'd-none'
            
        else:
            vaprofile_id = int(parse_qs(parsed.query).get('id', [0])[0])
            deletediv =''
        
        return [skill_options, vaprofile_id, deletediv]
    else:
        raise PreventUpdate
#Dynamic Header
@app.callback(
    Output('va_profile_header', 'children'),
    Input('url', 'search')
)
def update_header(urlsearch):
    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]
    
    if create_mode == 'add':
        return "Add New VA"
    else:
        return "Edit VA Details"
#This inserts into database
@app.callback(
    [Output('vasubmit_alert', 'color'),
     Output('vasubmit_alert', 'children'),
     Output('vasubmit_alert', 'is_open')],
    [Input('vasubmit_button', 'n_clicks')],
    [State('vafirst_name', 'value'),
     State('valast_name', 'value'),
     State('vaemail_address', 'value'),
     State('address', 'value'),
     State('va_skills', 'value'),
     State('date_hired', 'value'),
     State('va_status', 'value'),
     State('va_profile_delete', 'value'),
     State('url', 'search'),
     State('vaprofile_id', 'data')]
)
def submit_form(n_clicks, vafirst_name, valast_name, vaemail_address, address, va_skills, date_hired, va_status, va_profile_delete, urlsearch, vaprofile_id):
    
    ctx = dash.callback_context
    if not ctx.triggered or not n_clicks:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    # Check for missing values in the required fields
    if not all([vafirst_name, valast_name, vaemail_address, address, va_skills, date_hired, va_status]):
        return 'danger', 'Please fill in all required fields.', True
    
    # Determine if the client is marked for deletion
    delete_flag = True if va_profile_delete else False

    # SQL to insert or update the database
    if create_mode == 'add':
        sql_va = """INSERT INTO va (va_first_m, va_last_m, va_email, va_address, date_hired, va_status, va_delete_ind)
                VALUES (%s, %s, %s, %s, %s, %s, %s);"""        
        values_va = [vafirst_name, valast_name, vaemail_address, address, date_hired, va_status, delete_flag]
        va_id = modifyDB(sql_va, values_va)

        sql_skills = "INSERT INTO va_skills (va_id, skill_id) VALUES (%s, %s)"
        for skill in va_skills:
            modifyDB(sql_skills, (va_id, skill))

        return 'success', "New VA Added Successfully!", True
    
    elif create_mode == 'edit':
        sql_va = """
                UPDATE va
                SET va_first_m = %s,
                    va_last_m = %s,
                    va_email = %s,
                    va_address = %s,
                    date_hired = %s,
                    va_status = %s,
                    va_delete_ind = %s
                WHERE va_id=%s
            """
        values_va = [vafirst_name, valast_name, vaemail_address, address, date_hired, va_status, delete_flag, vaprofile_id]
        modifyDB(sql_va, values_va)

        sql_delete_skills = "DELETE FROM va_skills WHERE va_id = %s"
        modifyDB(sql_delete_skills, (vaprofile_id,))

        sql_skills = "INSERT INTO va_skills (va_id, skill_id) VALUES (%s, %s)"
        for skill in va_skills:
            modifyDB(sql_skills, (vaprofile_id, skill))

        return 'success', "VA Details Updated Successfully!", True

#This prepopulates during edit mode
@app.callback(
    [Output('vafirst_name', 'value'),
    Output('valast_name', 'value'),
    Output('vaemail_address', 'value'),
    Output('address', 'value'),
    Output('date_hired', 'value'),
    Output('va_status', 'value'),
    Output('va_skills', 'value')
    ],
    [Input('vaprofile_id', 'modified_timestamp'),],

    [State('vaprofile_id', 'data'),]
)
def va_profile_populate(timestamp, vaprofile_id):
    if not timestamp or vaprofile_id <= 0:
        raise PreventUpdate

    # SQL Query
    sql = """
        SELECT 
            va.va_first_m,
            va.va_last_m,
            va.va_email,
            va.va_address,
            va.date_hired,
            va.va_status,
            ARRAY_AGG(skills.skill_id) AS va_skills
        FROM 
            va
        LEFT JOIN 
            va_skills ON va.va_id = va_skills.va_id
        LEFT JOIN 
            skills ON va_skills.skill_id = skills.skill_id
        WHERE 
            va.va_id = %s
        GROUP BY 
            va.va_id
    """
    values = [vaprofile_id]
    cols = ['va_first_m', 'va_last_m', 'va_email', 'va_address', 'date_hired', 'va_status', 'va_skills']
    
    df = getDataFromDB(sql, values, cols)

    # Validate query results
    if df.empty:
        return [None] * 7  # Return default values if no data is found.

    # Extracting data safely
    record = df.iloc[0]  # Assuming there's always one record per va_id
    va_skills = record['va_skills'] if isinstance(record['va_skills'], list) else []

    return [
        record.get('va_first_m', None),
        record.get('va_last_m', None),
        record.get('va_email', None),
        record.get('va_address', None),
        record.get('date_hired', None),
        record.get('va_status', None),
        va_skills
    ]
