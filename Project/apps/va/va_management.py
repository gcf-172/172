import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
from app import app

# Define the layout for the Virtual Assistant Database
layout = dbc.Container([
    # Title Row for Virtual Assistant Database
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(
                        'Virtual Assistant Database', 
                        style={"marginBottom": "0px"}  # Reduce space below heading
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Add New Virtual Assistant",
                    href='/va/va_management_profile?mode=add',
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

    # Row for search bar and Add New VA button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search VA Name", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_virtual_assistant_name",  # ID for search bar
                        type="text",
                        placeholder="Enter VA name...",
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
                {"name": "VA ID", "id": "va_id"},
                {"name": "VA Name", "id": "va_name"},
                {"name": "VA Email Address", "id": "va_email_address"},
                {"name": "Date Hired", "id": "date_hired"},
                {"name": "Action", "id": "action", "presentation": "markdown"}  # Change to markdown
            ],
            data=[
                {
                    "va_id": "1", 
                    "va_name": "Fumi Cabrales", 
                    "va_email_address": "fumi@hohgymnj.com", 
                    "date_hired": "", 
                    "action": f"[Edit](/va_profile/va_management_profile?mode=edit&id=1)"
                },
                {
                    "va_id": "2", 
                    "va_name": "Cheska Miranda", 
                    "va_email_address": "cheska@hohgymnj.com", 
                    "date_hired": "", 
                    "action": f"[Edit](/va_profile/va_management_profile?mode=edit&id=2)"
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
