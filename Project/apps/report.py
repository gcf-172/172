import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate

# Sidebar content
sidebar = html.Div(
    [
        # Sidebar menu items
        html.Ul(
            [
                dcc.Link("Assignments", href="/report/jobs", style={"color": "white", "padding": "10px", "text-decoration": "none", "display": "block"}),
                dcc.Link("Clients", href="/report/clients", style={"color": "white", "padding": "10px", "text-decoration": "none", "display": "block"}),
                dcc.Link("Virtual Assistants", href="/report/va", style={"color": "white", "padding": "10px", "text-decoration": "none", "display": "block"}),
                dcc.Link("Skills", href="/report/skills", style={"color": "white", "padding": "10px", "text-decoration": "none", "display": "block"}),
            ],
            style={"list-style-type": "none", "padding": "0"}
        ),
    ],
    style={
        "background-color": "#333",
        "width": "200px",
        "height": "100vh",
        "position": "fixed",
        "top": "110px",
        "left": "0",
        "padding-top": "20px",
        "color": "white",
    }
)

# Main content with Reports Table
main_content = html.Div(
    [
        # Page header
        html.H2("Reports", style={"margin-top": "20px", "color": "#333", "padding-left": "20px"}),
        html.H4("Assignment Reports", style={"color": "#333", "padding-left": "20px"}),

        # Table for reports
        dash_table.DataTable(
            id="reports-table",
            columns=[
                {"name": "Report ID", "id": "report_id"},
                {"name": "Action", "id": "action"},
                {"name": "Title", "id": "title"},
                {"name": "Description", "id": "description"},
            ],
            data=[
                {"report_id": "ASSIGN-1", "action": "🔍", "title": "Custom Assignment List", "description": "Generate a customized report based on selected filters and columns to be included."},
                {"report_id": "ASSIGN-2", "action": "🔍", "title": "Assignment List Report", "description": "Generate a list of job assignments."},
            ],
            style_cell={
                "padding": "10px",
                "textAlign": "left"
            },
            style_header={
                "backgroundColor": "lightgray",
                "fontWeight": "bold"
            },
            style_as_list_view=True,
            style_table={
                "width": "100%",
                "padding": "0 20px"
            }
        )
    ],
    style={
        "margin-left": "220px",  # To give space for the sidebar
        "padding": "20px"
    }
)

layout = html.Div([sidebar, main_content])
