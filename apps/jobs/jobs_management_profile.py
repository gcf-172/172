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
        dcc.Store(id='jobmanagement_id', storage_type='memory', data=0),
        dbc.Row(
            [
                dbc.Col(html.H2(id="job_profile_header", style={'font-size': '25px'}), width="auto"),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/jobs_profile_info",
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

                # Job Title
                dbc.Row(
                    [
                        dbc.Label("Job Title", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='job_title',
                                placeholder='Enter Job Title',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                #Client Dropdown
                dbc.Row(
                    [
                        dbc.Label("Client Name", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='job_client',
                                    placeholder='Client Name',
                                    style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                                ),
                                className='dash-bootstrap'
                            ),
                            width=8,
                        )
                    ],
                    className='mb-3'
                ),

                #Skills Checklist
                dbc.Row(
                    [
                        dbc.Label("Required Skills", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Checklist(
                                    id='job_skills',
                                    style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px",'maxHeight': '200px','overflowY': 'scroll', 'display':'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '10px'},
                                    inline=True
                                ),
                                className='dash-bootstrap'
                            ),
                            width=8,
                        )
                    ],
                    className='mb-3'
                ),                

                # Combined Row for Days and Hours
                dbc.Row(
                    [
                        # Days
                        dbc.Label("Days per Week", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='days',
                                placeholder='',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=3
                        ),
                        
                        # Hours
                        dbc.Label("Hours per Week", width=2, className='text-center'),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='hours',
                                placeholder='',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=3
                        ),
                    ],
                    className="mb-3"
                ),

                # Combined Row for VA Hourly Rate and Synergy Hourly Commission
                dbc.Row(
                    [
                        # VA Hourly Rate
                        dbc.Label("VA Hourly Rate ($)", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='hourly_rate',
                                placeholder='',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=3
                        ),
                        
                        # Synergy Hourly Commission
                        dbc.Label("Synergy Hourly Commission ($)", width=2, className='text-center'), 
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='hourly_commission',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=3
                        ),
                    ],
                    className="mb-3"
                ),

                # VA Dropdown
                dbc.Row(
                    [
                        dbc.Label("VA Name", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='job_va',
                                    placeholder='VA Name',
                                    style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                                ),
                                className='dash-bootstrap'
                            ),
                            width=8,
                        )
                    ],
                    className='mb-3'
                ),

                # Job Start Date
                dbc.Row(
                    [
                        dbc.Label("Job Start Date", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='date',
                                id='start_date',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Job Assignment Date
                dbc.Row(
                    [
                        dbc.Label("Job Assignment Date", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='date',
                                id='assignment_date',
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
                                id='job_status',
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
                            id='jobs_profile_delete',
                            options=[dict(value=1, label="Mark as Deleted")],
                            value=[]
                        )
                    ],
                    id='jobmanagement_deletediv'
                ),

                dbc.Button(
                    "Submit", 
                    color="primary", 
                    className="mt-3 mb-3",
                    id='jobsubmit_button',
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
        dbc.Alert(id='jobsubmit_alert', is_open=False)
    ],
    className="container mt-0"
)

@app.callback(
    [
        Output('job_client', 'options'),
        Output('job_skills', 'options'),
        Output('job_va', 'options'),
        Output('jobmanagement_id', 'data'),
        Output('jobmanagement_deletediv', 'className')
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def job_profile_load(pathname, urlsearch):
    if pathname == '/jobs_profile/jobs_management_profile':
        # Fetch clients
        sql = """
        SELECT CONCAT(client_first_m, ' ', client_last_m) as label, client_id as value
        FROM clients
        """
        values = []
        cols = ['label', 'value']
        df = getDataFromDB(sql, values, cols)
        client_options = df.to_dict('records')

        # Fetch Skills
        sql = """
        SELECT skill_m as label, skill_id as value
        FROM skills
        """
        df = getDataFromDB(sql, values, cols)
        skill_options = df.to_dict('records')

        # Fetch ACTIVE VA options
        sql = """
        SELECT CONCAT(va_first_m, ' ', va_last_m) as label, va_id as value
        FROM va
        WHERE va_status = 'ACTIVE'
        """
        df = getDataFromDB(sql, values, cols)
        va_options = df.to_dict('records')

        # Add "NOT ASSIGNED" as a static option to VA dropdown
        va_options.insert(0, {'label': 'NOT ASSIGNED', 'value': 'NOT_ASSIGNED'})

        # Parse URL for mode and ID
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            jobmanagement_id = 0
            deletediv = 'd-none'  # Ensure this is a string
        else:
            jobmanagement_id = int(parse_qs(parsed.query).get('id', [0])[0])
            deletediv = ''  # Ensure this is a string

        return [client_options, skill_options, va_options, jobmanagement_id, deletediv]  # Order of return matches Outputs
    else:
        raise PreventUpdate

#Dynamic Header
@app.callback(
    Output('job_profile_header', 'children'),
    Input('url', 'search')
)
def update_header(urlsearch):
    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]
    
    if create_mode == 'add':
        return "Add New Job"
    else:
        return "Edit Job Details"
#This inserts into database
@app.callback(
    [Output('jobsubmit_alert', 'color'),
     Output('jobsubmit_alert', 'children'),
     Output('jobsubmit_alert', 'is_open')],
    [Input('jobsubmit_button', 'n_clicks')],
    [State('job_title', 'value'),
     State('job_client', 'value'),
     State('job_skills', 'value'),
     State('days', 'value'),
     State('hours', 'value'),
     State('hourly_rate', 'value'),
     State('hourly_commission', 'value'),
     State('job_va', 'value'),
     State('start_date', 'value'),
     State('assignment_date', 'value'),
     State('job_status', 'value'),
     State('jobs_profile_delete', 'value'),
     State('url', 'search'),
     State('jobmanagement_id', 'data')]
)
def submit_form(n_clicks, job_title, job_client, job_skills, days, hours, hourly_rate, hourly_commission, job_va, start_date, assignment_date, job_status, job_delete, urlsearch, jobmanagement_id):
    ctx = dash.callback_context
    if not ctx.triggered or not n_clicks:
        raise PreventUpdate

    # Validate required fields (excluding assignment_date since it's optional)
    if not all([job_title, job_client, job_skills, days, hours, hourly_rate, hourly_commission, start_date, job_status]):
        return 'danger', 'Please fill in all required fields.', True

    # Convert 'NOT_ASSIGNED' to None
    job_va = None if job_va == 'NOT_ASSIGNED' else job_va

    # Parse URL for mode
    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    delete_flag = True if job_delete else False

    # Handle null values for assignment_date
    assignment_date = assignment_date if assignment_date else None

    try:
        if create_mode == 'add':
            sql_job = """
            INSERT INTO jobs (job_title, days, hours, hourly_rate, hourly_commission, start_date, assignment_date, job_status, client_id, va_id, job_delete_ind)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values_job = [job_title, days, hours, hourly_rate, hourly_commission, start_date, assignment_date, job_status, job_client, job_va, delete_flag]
            job_id = modifyDB(sql_job, values_job)

            sql_skills = "INSERT INTO jobs_skills (job_id, skill_id) VALUES (%s, %s)"
            for skill in job_skills:
                modifyDB(sql_skills, (job_id, skill))

            return 'success', "New Job Added Successfully!", True

        elif create_mode == 'edit':
            sql_job = """
                UPDATE jobs 
                SET job_title=%s,
                    days=%s, 
                    hours=%s, 
                    hourly_rate=%s, 
                    hourly_commission=%s, 
                    start_date=%s, 
                    assignment_date=%s, 
                    job_status=%s, 
                    client_id=%s, 
                    va_id=%s,
                    job_delete_ind=%s
                WHERE job_id=%s
            """
            values_job = [job_title, days, hours, hourly_rate, hourly_commission, start_date, assignment_date, job_status, job_client, job_va, delete_flag, jobmanagement_id]
            modifyDB(sql_job, values_job)

            sql_delete_skills = "DELETE FROM jobs_skills WHERE job_id = %s"
            modifyDB(sql_delete_skills, (jobmanagement_id,))

            sql_skills = "INSERT INTO jobs_skills (job_id, skill_id) VALUES (%s, %s)"
            for skill in job_skills:
                modifyDB(sql_skills, (jobmanagement_id, skill))

            return 'success', "Job Details Updated Successfully!", True
    except Exception as e:
        print(f"Error: {e}")
        return 'danger', f'Error Occurred: {e}', True

#This prepopulates during edit mode
@app.callback(
    [Output('job_title', 'value'),
     Output('days', 'value'),
     Output('hours', 'value'),
     Output('hourly_rate', 'value'),
     Output('hourly_commission', 'value'),
     Output('start_date', 'value'),
     Output('assignment_date', 'value'),
     Output('job_status', 'value'),
     Output('job_client', 'value'),
     Output('job_va', 'value'),
     Output('job_skills', 'value')],
    [Input('jobmanagement_id', 'modified_timestamp')],
    [State('jobmanagement_id', 'data')]
)
def job_profile_populate(timestamp, jobmanagement_id):
    if not timestamp or jobmanagement_id <= 0:
        raise PreventUpdate

    # SQL Query
    sql = """
    SELECT 
        jobs.job_title,
        jobs.days,
        jobs.hours,
        jobs.hourly_rate,
        jobs.hourly_commission,
        jobs.start_date,
        jobs.assignment_date,
        jobs.job_status,
        jobs.client_id,
        jobs.va_id,
        ARRAY_AGG(skills.skill_id) AS job_skills
    FROM 
        jobs
    LEFT JOIN 
        jobs_skills ON jobs.job_id = jobs_skills.job_id
    LEFT JOIN 
        skills ON jobs_skills.skill_id = skills.skill_id
    WHERE 
        jobs.job_id = %s
    GROUP BY 
        jobs.job_id
    """
    values = [jobmanagement_id]
    cols = ['job_title', 'days', 'hours', 'hourly_rate', 'hourly_commission',
            'start_date', 'assignment_date', 'job_status', 'client_id', 'va_id', 'job_skills']
    
    df = getDataFromDB(sql, values, cols)

    # Validate query results
    if df.empty:
        return [None] * 11  # Return default values if no data is found.

    # Extracting data safely
    record = df.iloc[0]  # Assuming there's always one record per job_id
    job_skills = record['job_skills'] if isinstance(record['job_skills'], list) else []

    return [
        record.get('job_title', None),
        record.get('days', None),
        record.get('hours', None),
        record.get('hourly_rate', None),
        record.get('hourly_commission', None),
        record.get('start_date', None),
        record.get('assignment_date', None),
        record.get('job_status', None),
        record.get('client_id', None),
        record.get('va_id', None),
        job_skills
    ]
