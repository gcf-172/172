import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
from app import app

# Define the sidebar layout
layout = dbc.Container([
    # Title Row for Skills Database
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(
                        'Skills Database', 
                        style={"marginBottom": "0px"}  # Reduce space below heading
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Add New Skill",
                    href='/skills/skill_management_profile?mode=add',
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

    # Row for search bar and Add New Skill button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search Skill Name", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_skill_name",  # ID for search bar
                        type="text",
                        placeholder="Enter Skill name...",
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
                {"name": "Skill ID", "id": "skill_id"},
                {"name": "Skill Name", "id": "skill_name"},
                {"name": "Skill Description", "id": "skill_description"},
                {"name": "Action", "id": "action", "presentation": "markdown"}  # Change to markdown
            ],
            data=[
                {
                    "skill_id": "1", 
                    "skill_name": "Admin Assistance", 
                    "skill_description": "Manages schedules, emails, and documents to support smooth operations.", 
                    "action": f"[Edit](/skill_profile/skill_management_profile?mode=edit&id=1)"
                },
                {
                    "skill_id": "2", 
                    "skill_name": "Social Media Management", 
                    "skill_description": "Curates and posts content to grow and engage online audiences.", 
                    "action": f"[Edit](/skill_profile/skill_management_profile?mode=edit&id=2)"
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
