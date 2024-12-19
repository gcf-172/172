import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from dbconnect import getDataFromDB
from app import app

layout = dbc.Container([  
    # Title Row for JOBS DIRECTORY
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(
                        'JOBS DIRECTORY', 
                        style={"marginBottom": "0px"}  # Reduce space below heading
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Add New Job",
                    href='/jobs_profile/jobs_management_profile?mode=add',
                    style={"borderRadius": "20px", "fontWeight": "bold", "fontSize": "18px", "backgroundColor": "#194D62", "color": "white", "marginBottom": "0px"},
                    className="float-end"
                ),
                md=4,
                style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"},
            ),
        ],
        className="mb-1", # Adjust margin-bottom of row
        align="center"
    ),
    html.Hr(),  

    # Row for search bar and Add New job button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search Job Title or ID", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_job_title",  # ID for search bar
                        type="text",
                        placeholder="Enter Job Title or ID...",
                        className="form-control",
                        style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                [
                    html.Label(
                        "Filter by Job Status", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Dropdown(
                        id="search_job_status",
                        options=[
                            {"label": "ACTIVE", "value": "ACTIVE"},
                            {"label": "INACTIVE", "value": "INACTIVE"},
                            {"label": "ON HOLD", "value": "ON HOLD"},
                        ],
                        placeholder="Select Job Status",
                        className="form-control",
                        style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                    ),
                ],
                md=8,
            ),
        ],
        className="mb-4",
        align="center"
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    "Job Info",
                    href='/jobs_profile_info',
                    style={"borderRadius": "10px", "fontWeight": "bold", "fontSize": "16px", "backgroundColor": "#194D62", "color": "white", "marginBottom": "0px", "marginLeft": "0px"}
                ), width='auto'
            ),
            dbc.Col(
                dbc.Button(
                    "Details",
                    href='/jobs_profile_details',
                    style={"borderRadius": "10px", "fontWeight": "bold", "fontSize": "16px", "backgroundColor": "#194D62", "color": "white", "marginBottom": "0px", "marginRight": "0px"}
                ), width='auto'
            ),
        ], className="g-1"
    ),
    # Row for the table placeholder
    dbc.Row(
        dbc.Col(
            html.Div(
                id="jobs-table",  # ID for table placeholder
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "0px", "height": "100%"}  # Adjust height here
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px", "marginTop": "10px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

@app.callback(
    Output('jobs-table', 'children'),
    [
        Input('search_job_title', 'value'),
        Input('search_job_status', 'value'),
    ]
)
def update_records_table(jobfilter, jobstatus):
    # Base SQL query for the job table
    sql = """
        SELECT 
        j.job_id AS "Job ID",
        j.job_title AS "Job Title",
        j.days AS "Days",
        j.hours AS "Hours",
        j.hourly_rate AS "VA Hourly Rate ($)",
        j.hourly_commission AS "Synergy Hourly Commission ($)",
        j.start_date AS "Job Start Date",
        j.assignment_date AS "Assignment Start Date",
        j.job_status AS "Status"
        FROM 
        jobs j
        GROUP BY 
        j.job_id, j.job_title, j.days, j.hours, j.hourly_rate, j.hourly_commission, j.start_date, j.assignment_date, j.job_status
        ORDER BY 
        j.job_id
    """
    conditions =[]
    val = []

    # Add the WHERE clause if a filter is provided
    if jobfilter:
        # Check if the filter is numeric to search by job_id
        if jobfilter.isdigit():
            sql += " WHERE j.job_id = %s"
            val.append(int(jobfilter))
        else:
            sql += """
                WHERE 
                j.job_title ILIKE %s
            """
            val.extend([f'%{jobfilter}%'])

    if jobstatus:
        conditions.append("j.job_status = %s")
        val.append(jobstatus)

    if conditions:
        sql += " AND " + " AND ".join(conditions)

    # Fetch the filtered data into a DataFrame
    col = ["Job ID", "Job Title", "Days", "Hours", "VA Hourly Rate ($)", "Synergy Hourly Commission ($)", "Job Start Date", "Assignment Start Date", "Status"]
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Generating edit buttons for each job
    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                       href=f'/jobs_profile/jobs_management_profile?mode=edit&id={row["Job ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]
    display_columns = ["Job ID", "Job Title", "Days", "Hours", "VA Hourly Rate ($)", "Synergy Hourly Commission ($)", "Job Start Date", "Assignment Start Date", "Status", "Action"]
    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(df[display_columns], striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]