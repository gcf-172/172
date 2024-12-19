from datetime import datetime, timedelta
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import dbconnect as db
from dbconnect import getDataFromDB

from app import app

current_date = datetime.now().strftime("%B %d, %Y")

layout = html.Div(
    [
        html.H1(["REPORTS"],
                style={'background-color': '#c3d1e4', 'text-align': 'center'}),
        html.Hr(),

        # Row 1
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3('Client Growth Report')),
                                                dbc.CardBody(
                                                    [
                                                        html.P(f"As of {current_date}", className="fs-5 text-black"),
                                                        html.Hr(),
                                                        html.Div(id='client_growth'),
                                                        html.Div(id='client_growth_rate')
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    title='Client Growth Rate',
                                ),
                            ],
                            active_item=None  # Ensure all accordion items are collapsed by default
                        ),
                        html.Br(),  # Add space below the accordion
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3('Job Status Report')),
                                                dbc.CardBody(
                                                    [
                                                        html.P(f"As of {current_date}", className="fs-5 text-black"),
                                                        html.Hr(),
                                                        html.Div(id='job_assignment')
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    title='Job Assignment Report',
                                ),
                            ],
                            active_item=None  # Ensure all accordion items are collapsed by default
                        ),
                        html.Br(),  # Add space below the accordion
                    ]
                ),
                dbc.Col(
                dbc.Col(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3('VA Utilization Report')),
                                                dbc.CardBody(
                                                    [
                                                        html.P(f"As of {current_date}", className="fs-5 text-black"),
                                                        html.Hr(),
                                                        html.Div(id='va_utilization'),
                                                        html.Div(id='va_utilization_rate')
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    title='VA Utilization Report',
                                ),
                            ],
                            active_item=None  # Ensure all accordion items are collapsed by default
                        ),
                        html.Br(),  # Add space below the accordion
                    ]
                )
                ),
            ]
        ),

        # Row 2
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3('Synergy Commission Report')),
                                                dbc.CardBody(
                                                    [
                                                        html.P(f"As of {current_date}", className="fs-5 text-black"),
                                                        html.Hr(),
                                                        html.Div(id='synergy_commission_per_client'),
                                                        html.Div(id='synergy_commission'),
                                                        dcc.Graph(id='synergy_commission_graph')
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    title='Synergy Commission Report',
                                ),
                            ],
                            active_item=None  # Ensure all accordion items are collapsed by default
                        ),
                        html.Br(),  # Add space below the accordion
                    ]
                ),
            ]
        ),

        # Row 3
        dbc.Row(
            [
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H3('Skill Demand Report')),
                                        dbc.CardBody(
                                            [
                                                html.P(f"As of {current_date}", className="fs-5 text-black"),
                                                html.Hr(),
                                                html.Div(id='total_jobs_va'),
                                                html.Div(id='skill_demand'),
                                                html.Br(),
                                                dcc.Graph(id='job_skill_demand_graph'),  # Graph 1
                                                dcc.Graph(id='va_skill_availability_graph')  # Graph 2
                                            ]
                                        )
                                    ]
                                ),
                            ],
                            title='Skill Demand Report',
                        ),
                        html.Br(),  # Add space below the accordion
                    ], active_item=None 
                ),
            ]
        ),

        #Individual Reports
        dbc.Row(
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                            [
                                dbc.CardHeader(html.H2("Client/VA Performance Reports"),
                                               style={'background-color': '#c3d1e4', 'text-align': 'center'}
                                ),
                                
                                dbc.CardBody(
                                [
                                    # Dropdown to select Client or VA
                                    html.Div(
                                        dcc.Dropdown(
                                            id='user-type-dropdown',
                                            options=[
                                                {'label': 'Client', 'value': 'client'},
                                                {'label': 'Virtual Assistant (VA)', 'value': 'va'}
                                            ],
                                            value='client',  # default value
                                            style={'width': '50%'}
                                        ),
                                        style={'padding-bottom': '20px'}
                                    ),
                                    
                                    # Dropdown to select either client or VA
                                    html.Div(
                                        dcc.Dropdown(
                                            id='selection-dropdown',
                                            style={'width': '50%'}
                                        ),
                                        style={'padding-bottom': '20px'}
                                    ),
                                    
                                    # Output area for performance reports
                                    html.Div(id='performance-report', style={'margin-top': '20px'})
                                 ]
                             )
                        ]
                    )
                ]
            )
        )
    ]
)


#Table for Client Growth
@app.callback(
    [
        Output('client_growth','children')
     ],
    [
        Input('url','pathname')
    ]
)
def generate_client_summary(pathname):
    if pathname=='/reports':

    # Define SQL queries for each column
        sql_total_clients = """
            SELECT COUNT(*) AS total_clients
            FROM clients;
        """

        sql_active_clients = """
            SELECT COUNT(*) AS active_clients
            FROM clients
            WHERE client_status = 'ACTIVE';
        """

        sql_inactive_clients = """
            SELECT COUNT(*) AS inactive_clients
            FROM clients
            WHERE client_status = 'INACTIVE';
        """

        sql_new_clients = """
            SELECT COUNT(*) AS new_clients
            FROM clients
            WHERE date_acquired >= %s;
        """

    # Calculate the date 3 months ago
    three_months_ago = datetime.now() - timedelta(days=90)
    
    try:
        # Fetch data from the database
        total_clients = getDataFromDB(sql_total_clients, [], ["total_clients"]).get("total_clients", [0])[0]
        active_clients = getDataFromDB(sql_active_clients, [], ["active_clients"]).get("active_clients", [0])[0]
        inactive_clients = getDataFromDB(sql_inactive_clients, [], ["inactive_clients"]).get("inactive_clients", [0])[0]
        new_clients = getDataFromDB(sql_new_clients, [three_months_ago], ["new_clients"]).get("new_clients", [0])[0]
    except Exception as e:
        return [html.Div(f"Error fetching data: {e}", style={"color": "red"})]

    # Create a single-row DataFrame
    data = {
        "Total Clients": [total_clients],
        "Active Clients": [active_clients],
        "Inactive Clients": [inactive_clients],
        "New Clients (Past 3 Months)": [new_clients],
    }

    df = pd.DataFrame(data)

    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(
        df,
        striped=True,
        bordered=True,
        hover=True,
        size='sm',
        style={'textAlign': 'center'}
    )

    return [table]

#Table for Client Retention Rate and Client Acquisition Rate
@app.callback(
    [
        Output('client_growth_rate', 'children')
    ],
    [
        Input('url', 'pathname')
    ]
)
def generate_client_growth(pathname):
    if pathname == '/reports':
        try:
            # Calculate the date for 3 months ago
            three_months_ago = datetime.now() - timedelta(days=90)
            three_months_ago_str = three_months_ago.strftime('%Y-%m-%d')

            # Define SQL query
            sql = """
            SELECT 
                COUNT(*) AS total_clients,
                SUM(CASE WHEN client_status = 'ACTIVE' THEN 1 ELSE 0 END) AS active_clients,
                SUM(CASE WHEN date_acquired >= %s THEN 1 ELSE 0 END) AS new_clients,
                (SUM(CASE WHEN client_status = 'ACTIVE' THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) AS total_client_retention_rate,
                (SUM(CASE WHEN date_acquired >= %s THEN 1 ELSE 0 END) * 1.0 / 
                (COUNT(*) - SUM(CASE WHEN date_acquired >= %s THEN 1 ELSE 0 END))) AS client_acquisition_rate_past_3_months
            FROM clients;
            """

            # Fetch data from the database
            values = [three_months_ago_str, three_months_ago_str, three_months_ago_str]
            result = getDataFromDB(sql, values, [
                "total_clients", 
                "active_clients", 
                "new_clients", 
                "total_client_retention_rate", 
                "client_acquisition_rate_past_3_months"
            ])

            # Extract and validate results
            retention_rate = result.get("total_client_retention_rate", [0])[0]
            acquisition_rate = result.get("client_acquisition_rate_past_3_months", [0])[0]

            if retention_rate is None or acquisition_rate is None:
                return [html.Div("No data available for client growth rates.", style={"color": "grey"})]

            # Convert rates to percentages
            retention_rate_percentage = round(retention_rate * 100, 2)
            acquisition_rate_percentage = round(acquisition_rate * 100, 2)

            # Prepare data for the table
            data = {
                "Total Client Retention Rate (%)": [f"{retention_rate_percentage:.2f}%"],
                "Client Acquisition Rate (Past 3 Months) (%)": [f"{acquisition_rate_percentage:.2f}%"]
            }
            df = pd.DataFrame(data)

            # Create table
            table = dbc.Table.from_dataframe(
                df,
                striped=True,
                bordered=True,
                hover=True,
                size='sm',
                style={'textAlign': 'center'}
            )

            return [table]

        except Exception as e:
            # Handle errors gracefully
            return [html.Div(f"Error fetching data: {e}", style={"color": "red"})]

    # Return fallback for non-matching paths
    return [html.Div("No data to display for this path.", style={"color": "grey"})]


#Table and query for Job Assignment Report  
@app.callback(
    Output("job_assignment", "children"),
    Input("url", "pathname"),
)
def generate_job_summary(pathname):
    if pathname=='/reports':

    # Define SQL queries for each column
        sql_active_jobs = """
            SELECT COUNT(*) AS active_jobs
            FROM jobs
            WHERE job_status = 'ACTIVE';
        """

        sql_inactive_jobs = """
            SELECT COUNT(*) AS inactive_jobs
            FROM jobs
            WHERE job_status = 'INACTIVE';
        """

        sql_onhold_jobs = """
            SELECT COUNT(*) AS onhold_jobs
            FROM jobs
            WHERE job_status = 'ON HOLD';
        """
    
    try:
        # Fetch data from the database
        active_jobs = getDataFromDB(sql_active_jobs, [], ["active_jobs"]).get("active_jobs", [0])[0]
        inactive_jobs = getDataFromDB(sql_inactive_jobs, [], ["inactive_jobs"]).get("inactive_jobs", [0])[0]
        onhold_jobs = getDataFromDB(sql_onhold_jobs, [], ["onhold_jobs"]).get("onhold_jobs", [0])[0]

    except Exception as e:
        return [html.Div(f"Error fetching data: {e}", style={"color": "red"})]

    # Create a single-row DataFrame
    data = {
        "Active Jobs": [active_jobs],
        "Inactive Jobs": [inactive_jobs],
        "On Hold": [onhold_jobs],
    }

    df = pd.DataFrame(data)

    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(
        df,
        striped=True,
        bordered=True,
        hover=True,
        size='sm',
        style={'textAlign': 'center'}
    )

    return [table]

#Table and Query for VA Utilization Report
@app.callback(
    Output("va_utilization", "children"),
    Input("url", "pathname"),
)
def generate_va_summary(pathname):
    if pathname=='/reports':

        # Define SQL queries for each column
        sql_total_va = """
            SELECT COUNT(*) AS total_va
            FROM va;
        """

        sql_active_va = """
            SELECT COUNT(*) AS active_va
            FROM va
            WHERE va_status = 'ACTIVE';
        """

        sql_inactive_va = """
            SELECT COUNT(*) AS inactive_va
            FROM va
            WHERE va_status = 'INACTIVE';
        """

        sql_onhold_va = """
            SELECT COUNT(*) AS onhold_va
            FROM va
            WHERE va_status = 'ON HOLD';
        """
    
    try:
        # Fetch data from the database
        total_va = getDataFromDB(sql_total_va, [], ["total_va"]).get("total_va", [0])[0]
        active_va = getDataFromDB(sql_active_va, [], ["active_va"]).get("active_va", [0])[0]
        inactive_va = getDataFromDB(sql_inactive_va, [], ["inactive_va"]).get("inactive_va", [0])[0]
        onhold_va = getDataFromDB(sql_onhold_va, [], ["onhold_va"]).get("onhold_va", [0])[0]

    except Exception as e:
        return [html.Div(f"Error fetching data: {e}", style={"color": "red"})]

    # Create a single-row DataFrame
    data = {
        "Total Clients": [total_va],
        "Active VA": [active_va],
        "Inactive VA": [inactive_va],
        "On Hold": [onhold_va],
    }

    df = pd.DataFrame(data)

    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(
        df,
        striped=True,
        bordered=True,
        hover=True,
        size='sm',
        style={'textAlign': 'center'}
    )

    return [table]

#TABLE and QUERY for VA Utilization Rate
@app.callback(
    [
        Output('va_utilization_rate', 'children')
    ],
    [
        Input('url', 'pathname')
    ]
)
def generate_vautilization_rate(pathname):
    if pathname == '/reports':
        # SQL query to calculate VA utilization rate
        sql = """
            SELECT 
                COUNT(*) AS total_va,
                SUM(CASE WHEN va_status = 'ACTIVE' THEN 1 ELSE 0 END) AS active_va,
                (SUM(CASE WHEN va_status = 'ACTIVE' THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) AS va_utilization_rate
            FROM va;
        """

        try:
            # Fetch data from the database
            result = getDataFromDB(sql, [], ["total_va", "active_va", "va_utilization_rate"])

            # Extract and validate utilization rate
            utilization_rate = result.get("va_utilization_rate", [0])[0]
            if utilization_rate is not None:
                # Convert rate to percentage
                utilization_rate_percentage = round(utilization_rate * 100, 2)

                # Create a DataFrame for display
                data = {
                    "VA Utilization Rate (%)": [f"{utilization_rate_percentage:.2f}%"]
                }
                df = pd.DataFrame(data)

                # Render the table
                table = dbc.Table.from_dataframe(
                    df,
                    striped=True,
                    bordered=True,
                    hover=True,
                    size='sm',
                    style={'textAlign': 'center'}
                )
                return [table]
            else:
                # Handle case where utilization_rate is None
                return [html.Div("No data available for VA utilization rate.", style={"color": "grey"})]
        except Exception as e:
            # Handle exceptions gracefully
            return [html.Div(f"Error fetching data: {e}", style={"color": "red"})]
    
    # Return for non-reports paths
    return [html.Div("No data to display for this path.", style={"color": "grey"})]

#Table of Synergy Commission Per Client
@app.callback(
    [
        Output('synergy_commission_per_client', 'children')
    ],
    [
        Input('url', 'pathname')
    ]
)
def synergy_commission(pathname):
    if pathname == '/reports':
        # SQL query to calculate weekly commission per client with concatenated client_name
        sql = """
        SELECT
            j.client_id,
            CONCAT(c.client_first_m, ' ', c.client_last_m) AS client_name,
            SUM(j.hourly_commission * j.hours) AS weekly_commission
        FROM jobs j
        INNER JOIN clients c ON j.client_id = c.client_id
        WHERE j.job_status = 'ACTIVE'
        GROUP BY j.client_id, c.client_first_m, c.client_last_m;
        """

        try:
            # Fetch data from the database
            result = getDataFromDB(sql, [], ["client_id", "client_name", "weekly_commission"])

            # Convert the result to a DataFrame
            df = pd.DataFrame(result)

            # Explicitly check if the DataFrame is empty
            if df.empty:
                return [html.Div("No data available for synergy commission.", style={"color": "grey"})]

            # Handle None values in 'weekly_commission' column
            df['weekly_commission'] = df['weekly_commission'].fillna(0).astype(float)

            # Format 'Weekly Commission' column to 2 decimal places with $
            df['Weekly Commission ($)'] = df['weekly_commission'].apply(lambda x: f"${x:.2f}")

            # Sort the DataFrame by client_id
            df = df.sort_values(by='client_id', ascending=True)

            # Select relevant columns for display
            display_df = df[['client_id', 'client_name', 'Weekly Commission ($)']]
            display_df.columns = ['Client ID', 'Client Name', 'Weekly Commission ($)']

            # Create a Dash Bootstrap Table
            table = dbc.Table.from_dataframe(
                display_df,
                striped=True,
                bordered=True,
                hover=True,
                size='sm',
                style={'textAlign': 'center'}
            )
            return [table]

        except Exception as e:
            # Handle any database or calculation errors
            return [html.Div(f"Error fetching data: {e}", style={"color": "red"})]
    
    # Return for non-reports paths
    return [html.Div("No data to display for this path.", style={"color": "grey"})]


#Table and query for Synergy Commission Report
@app.callback(
    [
        Output('synergy_commission', 'children')
    ],
    [
        Input('url', 'pathname')
    ]
)
def synergy_commission(pathname):
    if pathname == '/reports':
        # SQL query to calculate weekly commission
        sql = """
        SELECT
            SUM(hourly_commission * hours) AS weekly_commission
        FROM jobs
        WHERE job_status = 'ACTIVE';
        """

        try:
            # Fetch data from the database
            result = getDataFromDB(sql, [], ["weekly_commission"])
            
            # Extract weekly commission value
            weekly_commission = result.get("weekly_commission", [0])[0]

            # Handle None values gracefully
            if weekly_commission is not None:
                weekly_commission = float(weekly_commission)  # Ensure it's a float
                data = {
                    "Total Weekly Commission ($)": [f"${weekly_commission:.2f}"]
                }

                # Create a DataFrame and table
                df = pd.DataFrame(data)
                table = dbc.Table.from_dataframe(
                    df,
                    striped=True,
                    bordered=True,
                    hover=True,
                    size='sm',
                    style={'textAlign': 'center'}
                )
                return [table]
            else:
                return [html.Div("No data available for synergy commission.", style={"color": "grey"})]
        
        except Exception as e:
            # Handle any database or calculation errors
            return [html.Div(f"Error fetching data: {e}", style={"color": "red"})]
    
    # Return for non-reports paths
    return [html.Div("No data to display for this path.", style={"color": "grey"})]

# Import necessary libraries
import plotly.express as px

# Graph for Quarterly Accumulated Commission (Line Graph)
@app.callback(
    [
        Output('synergy_commission_graph', 'figure')
    ],
    [
        Input('url', 'pathname')
    ]
)
def synergy_commission_graph(pathname):
    if pathname == '/reports':
        # SQL query to calculate accumulated commission by quarter
        sql = """
        WITH quarterly_commission AS (
            SELECT
                EXTRACT(YEAR FROM start_date) AS year,
                EXTRACT(QUARTER FROM start_date) AS quarter,
                SUM(hourly_commission * hours) AS quarterly_commission
            FROM jobs
            WHERE job_status = 'ACTIVE'
            GROUP BY EXTRACT(YEAR FROM start_date), EXTRACT(QUARTER FROM start_date)
        )
        SELECT
            year,
            quarter,
            SUM(quarterly_commission) OVER (ORDER BY year, quarter ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS accumulated_commission
        FROM quarterly_commission
        ORDER BY year, quarter;
        """

        try:
            # Fetch data from the database
            result = getDataFromDB(sql, [], ["year", "quarter", "accumulated_commission"])

            # Convert the result to a DataFrame
            df = pd.DataFrame(result)

            # Handle case when there is no data
            if df.empty:
                return [{
                    'data': [],
                    'layout': {
                        'title': 'Quarterly Accumulated Commission',
                        'xaxis': {'title': 'Quarter'},
                        'yaxis': {'title': 'Accumulated Commission ($)'}
                    }
                }]

            # Format the 'accumulated_commission' column to 2 decimal places with $
            df['Accumulated Commission ($)'] = df['accumulated_commission'].apply(lambda x: f"${x:.2f}")

            # Create a line chart to show the accumulated commission over quarters
            fig = {
                'data': [{
                    'x': [f"Q{int(row['quarter'])} {int(row['year'])}" for _, row in df.iterrows()],
                    'y': df['accumulated_commission'],
                    'type': 'line',
                    'name': 'Accumulated Commission',
                    'line': {'shape': 'linear'}
                }],
                'layout': {
                    'title': 'Quarterly Accumulated Commission',
                    'xaxis': {'title': 'Quarter'},
                    'yaxis': {'title': 'Accumulated Commission ($)'},
                    'hovermode': 'closest'
                }
            }
            return [fig]

        except Exception as e:
            # Handle any database or calculation errors
            return [{
                'data': [],
                'layout': {
                    'title': 'Quarterly Accumulated Commission',
                    'xaxis': {'title': 'Quarter'},
                    'yaxis': {'title': 'Accumulated Commission ($)'}
                }
            }]
    
    # Return for non-reports paths
    return [{
        'data': [],
        'layout': {
            'title': 'Quarterly Accumulated Commission',
            'xaxis': {'title': 'Quarter'},
            'yaxis': {'title': 'Accumulated Commission ($)'}
        }
    }]

#Callbacks for Total Jobs and Total VAs Table
@app.callback(
    [Output('total_jobs_va', 'children')],
    [Input('url', 'pathname')]
)
def generate_total_jobs_va(pathname):
    if pathname == '/reports':
        sql_jobs = "SELECT COUNT(*) AS total_jobs FROM jobs;"
        sql_va = "SELECT COUNT(*) AS total_va FROM va;"
        
        try:
            # Fetch data from the database
            total_jobs_data = getDataFromDB(sql_jobs, [], ["total_jobs"])  # Assumes DataFrame
            total_va_data = getDataFromDB(sql_va, [], ["total_va"])        # Assumes DataFrame

            # Safely extract values from DataFrame
            total_jobs = total_jobs_data['total_jobs'].iloc[0] if not total_jobs_data.empty else 0
            total_va = total_va_data['total_va'].iloc[0] if not total_va_data.empty else 0

            # Ensure values are integers
            total_jobs = int(total_jobs) if pd.notnull(total_jobs) else 0
            total_va = int(total_va) if pd.notnull(total_va) else 0

            # Create DataFrame for display
            data = {"Total Jobs": [total_jobs], "Total VAs": [total_va]}
            df = pd.DataFrame(data)

            # Render the table
            table = dbc.Table.from_dataframe(
                df, striped=True, bordered=True, hover=True, size='sm',
                style={'textAlign': 'center'}
            )
            return [table]
        
        except Exception as e:
            # Handle errors gracefully
            print(f"Error: {e}")
            return [html.Div(f"Error fetching data: {e}", style={"color": "red"})]

    # Fallback for invalid pathnames
    return [html.Div("No data to display for this path.", style={"color": "grey"})]

# Callbacks for Skill Demand Summary Table and Graphs
@app.callback(
    [
        Output('skill_demand', 'children'),
        Output('job_skill_demand_graph', 'figure'),
        Output('va_skill_availability_graph', 'figure')
    ],
    [Input('url', 'pathname')]
)
def generate_skill_demand_and_graphs(pathname):
    if pathname == '/reports':
        sql_skill_data = """
            SELECT 
                skills.skill_id AS "Skill ID",
                skills.skill_m AS "Skill Name",
                COALESCE(jobs_skills.job_count, 0) AS "Jobs Requiring Skill",
                COALESCE(va_skills.va_count, 0) AS "VAs with Skill"
            FROM skills
            LEFT JOIN (
                SELECT skill_id, COUNT(DISTINCT job_id) AS job_count
                FROM jobs_skills
                GROUP BY skill_id
            ) jobs_skills ON skills.skill_id = jobs_skills.skill_id
            LEFT JOIN (
                SELECT skill_id, COUNT(DISTINCT va_id) AS va_count
                FROM va_skills
                GROUP BY skill_id
            ) va_skills ON skills.skill_id = va_skills.skill_id;
        """
        try:
            # Fetch skill data
            skill_data = getDataFromDB(
                sql_skill_data,
                [],
                ["Skill ID", "Skill Name", "Jobs Requiring Skill", "VAs with Skill"]
            )
            df = pd.DataFrame(skill_data)
            
            # Fetch total_jobs and total_va
            total_jobs = getDataFromDB("SELECT COUNT(*) AS total_jobs FROM jobs;", [], ["total_jobs"]).get("total_jobs", [1])[0]
            total_va = getDataFromDB("SELECT COUNT(*) AS total_va FROM va;", [], ["total_va"]).get("total_va", [1])[0]

            # Ensure no division by zero
            total_jobs = total_jobs if total_jobs > 0 else 1
            total_va = total_va if total_va > 0 else 1

            # Calculate Job Skill Demand
            df['Job Skill Demand'] = df['Jobs Requiring Skill'] / total_jobs
            # Calculate VA Skill Availability
            df['VA Skill Availability'] = df['VAs with Skill'] / total_va

            # **Remove the unwanted columns for the table**
            table_df = df.drop(columns=['Job Skill Demand', 'VA Skill Availability'])

            # Table without Job Skill Demand and VA Skill Availability
            table = dbc.Table.from_dataframe(
                table_df,
                striped=True,
                bordered=True,
                hover=True,
                size='sm',
                style={'textAlign': 'center'}
            )

            # Graph 1: Job Skill Demand
            fig_job_skill = px.bar(
                df,
                x="Skill ID",
                y="Job Skill Demand",
                title="Job Skill Demand",
                labels={"Job Skill Demand": "Proportion of Jobs Requiring Skill", 'Skill ID': 'Skill ID'},
                text_auto=".2%"
            )
            fig_job_skill.update_traces(marker_color="#3f587b")
            

            # Graph 2: VA Skill Availability
            fig_va_skill = px.bar(
                df,
                x="Skill ID",
                y="VA Skill Availability",
                title="VA Skill Availability",
                labels={"VA Skill Availability": "Proportion of VAs with Skill", 'Skill ID': 'Skill ID'},
                text_auto=".2%"
            )
            fig_va_skill.update_traces(marker_color="#c8d7cd")

            return [table, fig_job_skill, fig_va_skill]

        except Exception as e:
            return [
                html.Div(f"Error fetching data: {e}", style={"color": "red"}),
                {},
                {}
            ]
    else:
        return [html.Div("Invalid pathname"), {}, {}]

# Fetching clients from the database
def get_clients():
    query = "SELECT client_id, client_first_m, client_last_m, client_company FROM clients WHERE client_delete_ind = FALSE"
    df_columns = ['client_id', 'client_first_m', 'client_last_m', 'client_company']
    return getDataFromDB(query, (), df_columns)

# Fetching virtual assistants (VAs) from the database
def get_vas():
    query = "SELECT va_id, va_first_m, va_last_m FROM va WHERE va_delete_ind = FALSE"
    df_columns = ['va_id', 'va_first_m', 'va_last_m']
    return getDataFromDB(query, (), df_columns)

# Fetching jobs based on client_id or va_id with a 3-month filter
def get_jobs(client_id=None, va_id=None):
    three_months_ago = datetime.now() - timedelta(days=90)
    if client_id:
        query = """
            SELECT job_title, days, hours, hourly_rate, hourly_commission, job_status, start_date, assignment_date
            FROM jobs WHERE client_id = %s AND job_delete_ind = FALSE AND start_date >= %s
        """
        values = (client_id, three_months_ago)
    elif va_id:
        query = """
            SELECT job_title, days, hours, hourly_rate, hourly_commission, job_status, start_date, assignment_date
            FROM jobs WHERE va_id = %s AND job_delete_ind = FALSE AND start_date >= %s
        """
        values = (va_id, three_months_ago)
    else:
        query = "SELECT job_title, days, hours, hourly_rate, hourly_commission, job_status, start_date, assignment_date FROM jobs WHERE job_delete_ind = FALSE AND start_date >= %s"
        values = (three_months_ago,)
    
    df_columns = ['job_title', 'days', 'hours', 'hourly_rate', 'hourly_commission', 'job_status', 'start_date', 'assignment_date']
    return getDataFromDB(query, values, df_columns)

# Callback to update the selection dropdown based on user type (client or va)
@app.callback(
    Output('selection-dropdown', 'options'),
    Output('selection-dropdown', 'value'),
    Input('user-type-dropdown', 'value')
)
def update_selection_dropdown(user_type):
    if user_type == 'client':
        clients = get_clients()
        options = [{'label': f"{row['client_first_m']} {row['client_last_m']} - {row['client_company']}", 'value': row['client_id']} for index, row in clients.iterrows()]
        value = clients['client_id'].iloc[0] if len(clients) > 0 else None
    elif user_type == 'va':
        vas = get_vas()
        options = [{'label': f"{row['va_first_m']} {row['va_last_m']}", 'value': row['va_id']} for index, row in vas.iterrows()]
        value = vas['va_id'].iloc[0] if len(vas) > 0 else None
    
    return options, value

# Callback to generate the performance report based on the selected client/VA
@app.callback(
    Output('performance-report', 'children'),
    Input('user-type-dropdown', 'value'),
    Input('selection-dropdown', 'value')
)
def generate_performance_report(user_type, selected_id):
    if user_type == 'client' and selected_id:
        jobs_df = get_jobs(client_id=selected_id)
        if jobs_df.empty:
            return "No jobs found for this client for the past 3 months."
        report = generate_report(jobs_df, "client")
    elif user_type == 'va' and selected_id:
        jobs_df = get_jobs(va_id=selected_id)
        if jobs_df.empty:
            return "No jobs found for this VA for the past 3 months."
        report = generate_report(jobs_df, "va")
    else:
        return "Please select a valid client or VA."
    
    return report

# Function to generate a performance report (table)
def generate_report(df, user_type):
    # Calculate total number of jobs and total commissions
    total_jobs = df.shape[0]
    total_commission = (df['hours'] * df['hourly_commission']).sum()

    # Create a DataFrame for the report table
    report_df = pd.DataFrame({
        'Client/VA': [f"Total for this {user_type}"],
        'Number of Jobs': [total_jobs],
        'Total Commissions ($)': [f"${total_commission:,.2f}"]
    })
    
    # Create a Dash DataTable to display the report
    table = dash_table.DataTable(
        data=report_df.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in report_df.columns],
        style_table={'height': '100%', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center'},
    )

    # Create another DataTable for job details (optional)
    job_details_df = df[['job_title', 'start_date', 'assignment_date', 'hours', 'hourly_commission']].copy()
    job_details_df.loc[:, 'total_commission'] = job_details_df['hours'] * job_details_df['hourly_commission']

    job_details_table = dash_table.DataTable(
        data=job_details_df.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in job_details_df.columns],
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center'},
    )

    return html.Div([
        html.H3(f"Performance Report for the Past 3 Months"),
        table,  # Table for overall summary
        html.H4(f"Job Details"),
        job_details_table  # Table for job-level details
    ])