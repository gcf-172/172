import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from app import app
import dbconnect  # Import the dbconnect module

# Fetch client data from the database
client_sql = "SELECT client_id, client_name, client_company, client_email FROM client;"
client_columns = ['client_id', 'client_name', 'client_company', 'client_email']
clients_data = dbconnect.getDataFromDB(client_sql, (), client_columns)  # Fetch the data

# Define the app layout
layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2('Client Database', style={"marginBottom": "0px"})
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Add New Client",
                    href='/client/client_management_profile?mode=add',
                    style={"borderRadius": "20px", "fontWeight": "bold", "fontSize": "18px", "backgroundColor": "#194D62", "color": "white", "marginBottom": "0px"},
                    className="float-end"
                ),
                md=4,
                style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"},
            ),
        ],
        className="mb-1",
        align="center"
    ),
    html.Hr(),

    # Row for search bar and Add New Client button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label("Search Client Name", className="form-label", style={"fontSize": "18px", "fontWeight": "bold"}),
                    dcc.Input(
                        id="search_client_name",  
                        type="text",
                        placeholder="Enter Client name...",
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
        dash_table.DataTable(
            id="client-table",
            columns=[
                {"name": "Client ID", "id": "client_id"},
                {"name": "Client Name", "id": "client_name"},
                {"name": "Client Company", "id": "client_company"},
                {"name": "Client Email Address", "id": "client_email"},
                {"name": "Action", "id": "action", "presentation": "markdown"}
            ],
            data=[{
                "client_id": row["client_id"],
                "client_name": row["client_name"],
                "client_company": row["client_company"],
                "client_email": row["client_email"],
                "action": f"[Edit](/client_profile/client_management_profile?mode=edit&id={row['client_id']})"
            } for _, row in clients_data.iterrows()],
            style_cell={
                "padding": "10px",
                "textAlign": "left"
            },
            style_header={
                "backgroundColor": "#3f587b",
                "fontWeight": "bold",
                "color": "white"
            },
            style_as_list_view=True,
            style_table={
                "width": "100%",
                "padding": "0 20px"
            },
            style_data_conditional=[
                {
                    "if": {"column_id": "action"},
                    "color": "#007bff",
                    "textDecoration": "underline",
                    "cursor": "pointer"
                }
            ]
        )
    )
])
