import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from app import app

# Define the layout for the dashboard
layout = html.Div(
    [
        html.H1('Welcome to Synergy Virtual Allies', style={"text-align": "center"}),
        dbc.Row([]),
        html.H2([html.I(className="bi bi-pie-chart me-2"),'DASHBOARD'], style={"font-size": "20px", "font-weight": "bold", "margin-left": "10px"}),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                html.I(className="bi bi-person-fill text-white fs-1"),
                                className="d-flex justify-content-center align-items-center",
                                style={
                                    "background-color": "#3f587b",
                                    "border-radius": "50%",
                                    "width": "60px",
                                    "height": "60px",
                                    "margin": "0 auto",
                                }
                            ),
                            html.H1("X", className="fs-1 text mt-3"),
                            html.H5("Active Clients", className="mt-2"),
                            html.H6("+X% over the last 3 months", className="text-success", style={"color": "#00c71c", "font-size": "0.9em"}),
                        ],
                    ),
                    className="text-center shadow-sm rounded",
                    style={"border": "1px solid #AAB8C2", "padding": "20px", "height": "250px", "width": "100%"}
                ),
            ], md=4, className="mb-4"),  # Makes each column take up a third of the row width, adjust md=4 for different widths
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                html.I(className="bi bi-people-fill text-white fs-1"),
                                className="d-flex justify-content-center align-items-center",
                                style={
                                    "background-color": "#3f587b",
                                    "border-radius": "50%",
                                    "width": "60px",
                                    "height": "60px",
                                    "margin": "0 auto",
                                }
                            ),
                            html.H1("X", className="fs-1 text mt-3"),
                            html.H5("Active VAs", className="mt-2"),
                            html.H6("+X% over the last 3 months", className="text-success", style={"color": "#00c71c", "font-size": "0.9em"}),
                        ],
                    ),
                    className="text-center shadow-sm rounded",
                    style={"border": "1px solid #AAB8C2", "padding": "20px", "height": "250px", "width": "100%"}
                ),
            ], md=4, className="mb-4"),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                html.I(className="bi bi-link text-white fs-1"),
                                className="d-flex justify-content-center align-items-center",
                                style={
                                    "background-color": "#3f587b",
                                    "border-radius": "50%",
                                    "width": "60px",
                                    "height": "60px",
                                    "margin": "0 auto",
                                }
                            ),
                            html.H1("X", className="fs-1 text mt-3"),
                            html.H5("Active Assignments", className="mt-2"),
                            html.H6("+X% over the last 3 months", className="text-success", style={"color": "#00c71c", "font-size": "0.9em"}),
                        ],
                    ),
                    className="text-center shadow-sm rounded",
                    style={"border": "1px solid #AAB8C2", "padding": "20px", "height": "250px", "width": "100%"}
                ),
            ], md=4, className="mb-4"),
        ], className="g-3")  # Adjust the spacing between columns
    ]
)