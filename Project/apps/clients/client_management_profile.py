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
        dcc.Store(id='clientprofile_id', storage_type='memory', data=0),
        dbc.Row(
            [
                dbc.Col(html.H2(id="client_profile_header", style={'font-size': '25px'}), width="auto"),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/client_profile",
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
                                id='clientfirst_name',
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
                                id='clientlast_name',
                                placeholder='Enter Last Name',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Company Name
                dbc.Row(
                    [
                        dbc.Label("Company Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='company',
                                placeholder='Enter Company Name',
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
                                id='clientemail_address',
                                placeholder='Enter Email Address',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Date Acquired
                dbc.Row(
                    [
                        dbc.Label("Date Acquired", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='date',
                                id='date_acquired',
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
                                id='client_status',
                                options=[
                                    {'label': 'ACTIVE', 'value': 'ACTIVE'},
                                    {'label': 'INACTIVE', 'value': 'INACTIVE'}
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
                            id='client_profile_delete',
                            options=[dict(value=1, label="Mark as Deleted")],
                            value=[]
                        )
                    ],
                    id='clientprofile_deletediv'
                ),

                dbc.Button(
                    "Submit", 
                    color="primary", 
                    className="mt-3 mb-3",
                    id='clientsubmit_button',
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
        dbc.Alert(id='clientsubmit_alert', is_open=False)
    ],
    className="container mt-4"
)


@app.callback(
    [
        Output('clientprofile_id', 'data'),
        Output('clientprofile_deletediv', 'className')
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def client_profile_load(pathname, urlsearch):
    if pathname == '/client_profile/client_management_profile':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            clientprofile_id = 0
            deletediv = 'd-none'
            
        else:
            clientprofile_id = int(parse_qs(parsed.query).get('id', [0])[0])
            deletediv =''
        
        return [clientprofile_id, deletediv]
    else:
        raise PreventUpdate
#Dynamic Header
@app.callback(
    Output('client_profile_header', 'children'),
    Input('url', 'search')
)
def update_header(urlsearch):
    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]
    
    if create_mode == 'add':
        return "Add New Client Profile"
    else:
        return "Edit Client Profile"
#This inserts into database
@app.callback(
    [Output('clientsubmit_alert', 'color'),
     Output('clientsubmit_alert', 'children'),
     Output('clientsubmit_alert', 'is_open')],
    [Input('clientsubmit_button', 'n_clicks')],
    [State('clientfirst_name', 'value'),
     State('clientlast_name', 'value'),
     State('company', 'value'),
     State('clientemail_address', 'value'),
     State('date_acquired', 'value'),
     State('client_status', 'value'),
     State('client_profile_delete', 'value'),
     State('url', 'search'),
     State('clientprofile_id', 'data')]
)
def submit_form(n_clicks, clientfirst_name, clientlast_name, company, clientemail_address, date_acquired, client_status, client_profile_delete, urlsearch, clientprofile_id):
    ctx = dash.callback_context
    if not ctx.triggered or not n_clicks:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    # Check for missing values in the required fields
    if not all([clientfirst_name, clientlast_name, company, clientemail_address, date_acquired, client_status]):
        return 'danger', 'Please fill in all required fields.', True

    # Determine if the client is marked for deletion
    delete_flag = True if client_profile_delete else False

    # SQL to insert or update the database
    if create_mode == 'add':
        sql = """INSERT INTO clients (client_first_m, client_last_m, client_company, client_email, date_acquired, client_status, client_delete_ind)
                 VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        values = [clientfirst_name, clientlast_name, company, clientemail_address, date_acquired, client_status, delete_flag]
        success_message = "New Client Added Successfully!"

    elif create_mode == 'edit':
        sql = """UPDATE clients
                 SET client_first_m = %s,
                     client_last_m = %s,
                     client_company = %s,
                     client_email = %s,
                     date_acquired = %s,
                     client_status = %s,
                     client_delete_ind = %s
                 WHERE client_id = %s;"""
        values = [clientfirst_name, clientlast_name, company, clientemail_address, date_acquired, client_status, delete_flag, clientprofile_id]
        success_message = "Client Profile Updated Successfully!"
    else:
        raise PreventUpdate

    try:
        modifyDB(sql, values)
        return 'success', success_message, True
    except Exception as e:
        return 'danger', f'Error Occurred: {e}', True


#This prepopulates during edit mode
@app.callback(
    [Output('clientfirst_name', 'value'),
    Output('clientlast_name', 'value'),
    Output('company', 'value'),
    Output('clientemail_address', 'value'),
    Output('date_acquired', 'value'),
    Output('client_status', 'value'),
    ],
    [Input('clientprofile_id', 'modified_timestamp'),],

    [State('clientprofile_id', 'data'),]
)
def client_profile_populate(timestamp, clientprofile_id):
    if clientprofile_id > 0:
        sql = """SELECT client_first_m, client_last_m, client_company, client_email, date_acquired, client_status
                FROM clients
                WHERE client_id = %s"""
        values = [clientprofile_id]
        col = ['clientfirst_name', 'clientlast_name', 'company', 'clientemail_address', 'date_acquired', 'client_status']

        df = getDataFromDB(sql, values, col)

        clientfirstname = df['clientfirst_name'][0]
        clientlastname = df['clientlast_name'][0]
        company = df['company'][0]
        clientemailaddress = df['clientemail_address'][0]
        dateacquired = df['date_acquired'][0]
        clientstatus = df['client_status'][0]

        return [clientfirstname, clientlastname, company, clientemailaddress, dateacquired, clientstatus]
    else:
        raise PreventUpdate
