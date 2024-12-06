# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app

navlink_style = {
    'color': '#ffffff', 
    'margin-right': '1.5em', 
    'text-align': 'center'
}

navbar = dbc.Navbar(
    [
        # Brand with logo and title below the image
        dbc.NavbarBrand(
            dbc.Row([
                dbc.Col([
                    html.Img(
                        src="https://media.licdn.com/dms/image/v2/D560BAQFxpi5VR3cZcA/company-logo_200_200/company-logo_200_200/0/1730965986824/synergyvirtual_logo?e=1738800000&v=beta&t=4h1JsvDVYtnGVuoe4Pd4x5Woznj0k9L-h7BoFU3FpZM",
                        height="84px",
                        style={"display": "block", "justify-content": "center", "margin-left": "1.5em"}  # Center image horizontally
                    ),
                ])
            ], align="center", className="g-0"),
            href="/home",
            className="me-auto",
        ),
        # Navigation links
        dbc.Nav(
            [
                dbc.NavItem(
                    dbc.NavLink(
                        html.Div([
                            html.I(className="bi bi-link-45deg", style={"font-size": "1.2em"}),  # Icon
                            html.Span("ASSIGNMENTS", style={"font-size": "0.8em"}),  # Text
                        ], className="d-flex flex-column align-items-center"),  # Stacks icon and text vertically
                        href="/jobs",
                        style=navlink_style
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        html.Div([
                            html.I(className="bi bi-person-fill", style={"font-size": "1.2em"}),
                            html.Span("CLIENTS", style={"font-size": "0.8em"}),
                        ], className="d-flex flex-column align-items-center"),
                        href="/clients",
                        style=navlink_style
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        html.Div([
                            html.I(className="bi bi-people-fill", style={"font-size": "1.2em"}),
                            html.Span("VAs", style={"font-size": "0.8em"}),
                        ], className="d-flex flex-column align-items-center"),
                        href="/va",
                        style=navlink_style
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        html.Div([
                            html.I(className="bi bi-stars", style={"font-size": "1.2em"}),
                            html.Span("SKILLS", style={"font-size": "0.8em"}),
                        ], className="d-flex flex-column align-items-center"),
                        href="/skills",
                        style=navlink_style
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        html.Div([
                            html.I(className="bi bi-clipboard", style={"font-size": "1.2em"}),
                            html.Span("REPORT", style={"font-size": "0.8em"}),
                        ], className="d-flex flex-column align-items-center"),
                        href="/reports",
                        style=navlink_style
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        html.Div([
                            html.I(className="bi bi-person-circle", style={"font-size": "1.2em"}),
                            html.Span("PROFILE", style={"font-size": "0.8em"}),
                        ], className="d-flex flex-column align-items-center"),
                        href="/profile",
                        style=navlink_style
                    )
                ),
            ],
            className="ms-auto"
        ),
    ],
    color='#3f587b',
    dark=True,
)