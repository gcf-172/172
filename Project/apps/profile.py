import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

# Sidebar content
sidebar = html.Div(
    [
        # Profile section
        html.Div(
            [
                html.Img(src="https://media.licdn.com/dms/image/v2/D560BAQFxpi5VR3cZcA/company-logo_200_200/company-logo_200_200/0/1730965986824/synergyvirtual_logo?e=1738800000&v=beta&t=4h1JsvDVYtnGVuoe4Pd4x5Woznj0k9L-h7BoFU3FpZM", className="rounded-circle", height="40px"),  # Profile icon placeholder
                html.H5("Hello, ", className="text", style={"color": "white", "font-size": "16px"}),
                html.H5("Welcome Back! ", className="text", style={"color": "white", "font-size": "16px"}),
            ],
            style={"text-align": "center", "padding": "20px", "border-bottom": "1px solid #333"}
        ),
        # Menu items as links
        html.Ul(
            [
                dcc.Link(
                    [
                        html.I(className="fa fa-lock", style={"margin-right": "10px"}),  # Lock icon
                        "LOG OUT"
                    ],
                    href="/profile/logout",
                    style={"color": "white", "padding": "10px", "display": "flex", "align-items": "center", "text-decoration": "none"}
                ),
                dcc.Link(
                    [
                        html.I(className="fa fa-cog", style={"margin-right": "10px"}),  # Settings icon
                        "SETTINGS"
                    ],
                    href="/profile/settings",
                    style={"color": "white", "padding": "10px", "display": "flex", "align-items": "center", "text-decoration": "none"}
                ),
                dcc.Link(
                    [
                        html.I(className="fa fa-info-circle", style={"margin-right": "10px"}),  # Support icon
                        "SUPPORT"
                    ],
                    href="/profile/support",
                    style={"color": "white", "padding": "10px", "display": "flex", "align-items": "center", "text-decoration": "none"}
                ),
                dcc.Link(
                    [
                        html.I(className="fa fa-newspaper", style={"margin-right": "10px"}),  # News and announcements icon
                        "NEWS & ANNOUNCEMENTS"
                    ],
                    href="/profile/news-announcements",
                    style={"color": "white", "padding": "10px", "display": "flex", "align-items": "center", "text-decoration": "none"}
                ),
                dcc.Link(
                    [
                        html.I(className="fa fa-bell", style={"margin-right": "10px"}),  # Updates icon
                        "UPDATES ",
                    ],
                    href="/profile/updates",
                    style={"color": "white", "padding": "10px", "display": "flex", "align-items": "center", "text-decoration": "none"}
                ),
            ],
            style={"list-style-type": "none", "padding": "0"}
        )
    ],
    style={
        "background-color": "#333",
        "width": "250px",
        "height": "100vh",
        "position": "fixed",
        "top": "80px",
        "right": "0",
        "z-index": "1000",
        "overflow-y": "auto",
        "padding-top": "10px",
        "font-size": "14px"
    }
)

# Layout to include the sidebar
layout = html.Div([sidebar]) 