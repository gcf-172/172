import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from app import app
from dbconnect import getDataFromDB, modifyDB

layout = html.Div(
    [
        html.H2('jobs Details'), # Page Header
        html.Hr(),
        dbc.Alert(id='jobsprofile_alert', is_open=False), # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Job Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='jobsprofile_name',
                                placeholder="Job Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Hours Daily", width=1),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='jobsprofile_hours',
                                    placeholder='Hours Daily'
                                ),
                                className='dash-bootstrap'
                            ),
                            width=5,
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Days Weekly", width=1),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='jobsprofile_days',
                                    placeholder='Days Weekly'
                                ),
                                className='dash-bootstrap'
                            ),
                            width=5,
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Hourly Rate", width=1),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='jobsprofile_rate',
                                    placeholder='Hourly Rate'
                                ),
                                className='dash-bootstrap'
                            ),
                            width=5,
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Commission Rate", width=1),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='jobsprofile_comission',
                                    placeholder='Commission Rate'
                                ),
                                className='dash-bootstrap'
                            ),
                            width=5,
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Start Date", width=1),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='jobsprofile_startdate',
                                placeholder='Start Date',
                                month_format='MMM Do, YY',
                            ),
                            width=5, 
                            className='dash-bootstrap'
                        )
                    ],
                    className='mb-3'
                ),

            ]
        ),
          dbc.Button(
            'Submit',
            id='jobsprofile_submit',
            n_clicks=0 # Initialize number of clicks
        ),
        dbc.Modal( # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    'Message here! Edit me please!'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/jobs/jobs_management' # Clicking this would lead to a change of pages
                    )
                )
            ],
            centered=True,
            id='jobsprofile_successmodal',
            backdrop='static' # Dialog box does not go away if you click at the background
        )
    ]
)

@app.callback(
    [
        Output('jobsprofile_description', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def jobsprofile_populatedescriptions(pathname):
    if pathname == '/jobs/jobs_management_profile':
        sql = """
        SELECT description_name as label, description_id as value
        FROM descriptions 
        WHERE description_delete_ind = False
        """
        values = []
        cols = ['label', 'value']

        df = getDataFromDB(sql, values, cols)
        # The output must be a dictionary with the following structure
        # options=[
        #     {'label': "Factorial", 'value': 1},
        #     {'label': "Palindrome Checker", 'value': 2},
        #     {'label': "Greeter", 'value': 3},
        # ]

        description_options = df.to_dict('records')
        return [description_options]
    else:
        raise PreventUpdate

        
@app.callback(
    [
        # dbc.Alert Properties
        Output('jobsprofile_alert', 'color'),
        Output('jobsprofile_alert', 'children'),
        Output('jobsprofile_alert', 'is_open'),
        # dbc.Modal Properties
        Output('jobsprofile_successmodal', 'is_open')
    ],
    [
        # For buttons, the property n_clicks 
        Input('jobsprofile_submit', 'n_clicks')
    ],
    [
        # The values of the fields are States 
        # They are required in this process but they 
        # do not trigger this callback
        State('jobsprofile_title', 'value'),
        State('jobsprofile_description', 'value'),
        State('jobsprofile_releasedate', 'date'),
    ]
)
def jobsprofile_saveprofile(submitbtn, title, description, releasedate):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'jobsprofile_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout

            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            # We need to check inputs
            if not title: # If title is blank, not title = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the jobs title.'
            elif not description:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the jobs description.'
            elif not releasedate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the jobs release date.'
            else: # all inputs are valid
                # Add the data into the db

                sql = '''
                    INSERT INTO jobss (jobs_name, description_id,
                        jobs_release_date, jobs_delete_ind)
                    VALUES (%s, %s, %s, %s)
                '''
                values = [title, description, releasedate, False]

                modifyDB(sql, values)

                # If this is successful, we want the successmodal to show
                modal_open = True

            return [alert_color, alert_text, alert_open, modal_open]

        else: 
            raise PreventUpdate

    else:
        raise PreventUpdate
