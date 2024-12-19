import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define Navbar styling and active state
navlink_style = {
    'color': '#fff',
    'font-size': '20px',
    'margin': '0 1.5em',  # Adjusted left and right margin for consistent spacing
    'padding': '10px 0',  # Added padding for vertical alignment
}
navlink_active_style = {
    'color': '#c3d1e4',
    'font-size': '20px',
    'borderBottom': '3px solid skyblue',
    'margin': '0 1.5em',
    'padding': '10px 0',
}

# Navbar component
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavLink(
                            html.Img(
                                src="/assets/synergyvirtual_logo.jpg",
                                height="80px",
                                width="90px",
                                style={'margin-right': '20px', 'borderRadius': "50px"}
                            ),
                            href='/home',
                            style={'padding': '0'}  # Remove padding around the link
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        dbc.NavbarBrand(
                            "Synergy Virtual Allies",
                            className="ms-2",
                            href='/home',
                            style={
                                'color': '#FFFFFF',
                                'font-weight': 'bold',
                                'font-size': '33px',
                                'text-decoration': 'none'  # Ensure no underline on the text
                            }
                        ),
                        width="auto",
                    ),
                ],
                align="center",
                className="g-0 me-auto",            
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Jobs", href="/jobs_profile_info", id="nav-jobs", style=navlink_style),
                    dbc.NavLink("Clients", href="/client_profile", id="nav-client-profile", style=navlink_style),
                    dbc.NavLink("VAs", href="/va_profile_info", id="nav-va-profile", style=navlink_style),
                    dbc.NavLink("Skills", href="/skills", id="nav-skills", style=navlink_style),
                    dbc.NavLink("Reports", href="/reports", id="nav-report", style=navlink_style),
                    dbc.NavLink("Log Out", href="/login", id="nav-logout", style={'backgroundColor': 'white','color': '#194D62','padding': '10px 20px','borderRadius': '5px','textAlign': 'center','fontWeight': 'bold','textDecoration': 'none',}),
                ],
                className="ms-auto",
                navbar=True,
            ),
        ],
        fluid=True,  # Full-width container for better spacing control
    ),
    color="#3f587b",
    dark=False,
    className="mb-4",
    style={'padding': '15px', 'borderBottom': '2px solid #e3e3e3'}
)
