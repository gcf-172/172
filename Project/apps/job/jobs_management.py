import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
from app import app

# Define the sidebar layout
layout = dbc.Container([
    # Title Row for Jobs Database
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
                    href='/jobs/jobs_management_profile?mode=add',
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

    # Row for search bar and Add New Job button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search Assignment ID or Name", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_job_name",  # ID for search bar
                        type="text",
                        placeholder="Enter Assignment ID or name...",
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
                {"name": "Job ID", "id": "job_id"},
                {"name": "Job Title", "id": "job_title"},
                {"name": "Client Name", "id": "client_name"},
                {"name": "Required Skills", "id": "skill_name"},
                {"name": "Assigned VA", "id": "va_name"},
                {"name": "Action", "id": "action", "presentation": "markdown"}  # Change to markdown
            ],
            data=[
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
