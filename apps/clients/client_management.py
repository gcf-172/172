import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from dbconnect import getDataFromDB
from app import app

layout = dbc.Container([
    # Title Row for CLIENT DIRECTORY
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(
                        'CLIENT DIRECTORY', 
                        style={"marginBottom": "0px"}  # Reduce space below heading
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Add New Client",
                    href='/client_profile/client_management_profile?mode=add',
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

    # Row for search bar and Add New client button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search Client Name or ID", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_client_name",  # ID for search bar
                        type="text",
                        placeholder="Enter Client Name or ID...",
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

    # Row for the table placeholder
    dbc.Row(
        dbc.Col(
            html.Div(
                id="client-table",  # ID for table placeholder
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "0px", "height": "100%"}  # Adjust height here
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "10px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

@app.callback(
    Output('client-table', 'children'),
    [
        Input('search_client_name', 'value'),
    ]
)
def update_records_table(clientfilter):
    # Base SQL query for the client table
    sql = """
    SELECT 
        c.client_id,
        CONCAT(c.client_first_m, ' ', c.client_last_m) AS "Client Name",
        c.client_company AS "Company",
        c.client_email AS "Client Email Address",
        c.date_acquired AS "Date Acquired",
        c.client_status AS "Status"
    FROM 
        clients c
    WHERE 
        client_delete_ind = false
    """
    val = []

    # Add additional filters
    if clientfilter:
        # Check if the filter is numeric to search by client_id
        if clientfilter.isdigit():
            sql += " AND c.client_id = %s"
            val.append(int(clientfilter))
        else:
            sql += """
                AND (
                    c.client_first_m ILIKE %s OR 
                    c.client_last_m ILIKE %s
                )
            """
            val.extend([f'%{clientfilter}%'] * 2)

    # Add ORDER BY clause
    sql += """
    ORDER BY 
        c.client_id
    """

    # Define the column names
    col = ["Client ID", "Client Name", "Company", "Email Address", "Date Acquired", "Status"]


    # Fetch the filtered data into a DataFrame
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Generating edit buttons for each client
    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                       href=f'/client_profile/client_management_profile?mode=edit&id={row["Client ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]
    display_columns = ["Client ID", "Client Name", "Company", "Email Address", "Date Acquired", "Status", "Action"]
    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(df[display_columns], striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]
