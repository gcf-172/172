import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
from app import app

# Define the app layout
layout = dbc.Container([
    # Title Row for Patient Profile Management
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(
                        'Client Database', 
                        style={"marginBottom": "0px"}  # Reduce space below heading
                    ),
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
        className="mb-1",  # Adjust margin-bottom of row
        align="center"
    ),
    html.Hr(),

    # Row for search bar and Add New Patient button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search Client Name", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_client_name",  # ID for search bar
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
            id="reports-table",
            columns=[
                {"name": "Client ID", "id": "client_id"},
                {"name": "Client Name", "id": "client_name"},
                {"name": "Client Company", "id": "client_company"},
                {"name": "Client Email Address", "id": "client_email_address"},
                {"name": "Action", "id": "action", "presentation": "markdown"}  # Change to markdown
            ],
            data=[
                {
                    "client_id": "1", 
                    "client_name": "Jason Bauer", 
                    "client_company": "Head Over Heels", 
                    "client_email_address": "jason@hohgymnj.com", 
                    "action": f"[Edit](/client_profile/client_management_profile?mode=edit&id=1)"
                },
                {
                    "client_id": "2", 
                    "client_name": "Mandi Wilson-Saur", 
                    "client_company": "Northwest Gymnastics Inc.", 
                    "client_email_address": "mandiwilson1225@gmail.com", 
                    "action": f"[Edit](/client_profile/client_management_profile?mode=edit&id=2)"
                },
            ],
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
                    "color": "#007bff",  # Link color
                    "textDecoration": "underline",
                    "cursor": "pointer"
                }
            ]
        )
    )
])
