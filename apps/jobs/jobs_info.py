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
                        "Search Job Title, Client Name, VA Name or Job ID", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_job_info_title",  # ID for search bar
                        type="text",
                        placeholder="Enter Job Title, Client Name, VA Name or their IDs...",
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
                id="jobs-info-table",  # ID for table placeholder
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "0px", "height": "100%"}  # Adjust height here
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px", "marginTop": "10px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

@app.callback(
    Output('jobs-info-table', 'children'),
    [Input('search_job_info_title', 'value')]
)
def update_records_table(jobinfofilter):
    # Base SQL query for the job table
    sql = """
        SELECT 
            jobs.job_id AS "Job ID",
            jobs.job_title AS "Job Title",
            CONCAT(clients.client_first_m, ' ', clients.client_last_m) AS "Client Name",
            STRING_AGG(skills.skill_m, ', ') AS "Required Skills",
            -- Use a CASE statement to handle the "Assigned VA" column
            CASE 
                WHEN jobs.job_status = 'INACTIVE' THEN 'NOT ASSIGNED'
                WHEN jobs.va_id IS NULL THEN 'NOT ASSIGNED'
                ELSE COALESCE(CONCAT(va.va_first_m, ' ', va.va_last_m), 'NOT ASSIGNED')
            END AS "Assigned VA"
        FROM 
            jobs 
        JOIN 
            clients ON jobs.client_id = clients.client_id
        LEFT JOIN 
            jobs_skills ON jobs.job_id = jobs_skills.job_id
        LEFT JOIN 
            skills ON jobs_skills.skill_id = skills.skill_id
        LEFT JOIN 
            va ON jobs.va_id = va.va_id
        WHERE 
            job_delete_ind = false
    """
    val = []

    # Add the WHERE clause if a filter is provided
    if jobinfofilter:
        # Initialize WHERE clause
        sql += " AND "
        conditions = []

        # If the filter is numeric (for job_id)
        if jobinfofilter.isdigit():
            conditions.append("jobs.job_id = %s")
            val.append(int(jobinfofilter))
        else:
            # Check if filter matches job_title
            conditions.append("jobs.job_title ILIKE %s")
            val.append(f'%{jobinfofilter}%')

            # Check if filter matches client_name (first and last name)
            conditions.append("CONCAT(clients.client_first_m, ' ', clients.client_last_m) ILIKE %s")
            val.append(f'%{jobinfofilter}%')

            # Check if filter matches VA name (first and last name)
            conditions.append("COALESCE(CONCAT(va.va_first_m, ' ', va.va_last_m), '') ILIKE %s")
            val.append(f'%{jobinfofilter}%')

        # Join all conditions with OR
        sql += " (" + " OR ".join(conditions) + ")"

    # Add the GROUP BY and ORDER BY clauses
    sql += """
        GROUP BY 
            jobs.job_id, jobs.job_title, clients.client_first_m, clients.client_last_m, jobs.job_status, va.va_first_m, va.va_last_m
        ORDER BY 
            jobs.job_id"""

    # Fetch the filtered data into a DataFrame
    col = ["Job ID", "Job Title", "Client Name", "Required Skills", "Assigned VA"]
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Handle missing or None values in the Assigned VA column (Python fallback)
    df["Assigned VA"] = df["Assigned VA"].fillna("NOT ASSIGNED")

    # Generating edit buttons for each job
    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                       href=f'/jobs_profile/jobs_management_profile?mode=edit&id={row["Job ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    display_columns = ["Job ID", "Job Title", "Client Name", "Required Skills", "Assigned VA", "Action"]

    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(df[display_columns], striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]