import webbrowser
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import commonmodule as cm
from apps import home, profile, report
from apps.client import client_management, client_management_profile
from apps.job import jobs_management, jobs_management_profile
from apps.skills import skills_management, skills_management_profile
from apps.va import va_management, va_management_profile
import login  # Import the login module

app.layout = html.Div(
    [
        # Location Variable -- contains details about the url
        dcc.Location(id='url', refresh=True),
        # Conditional Navbar (only for non-login pages)
        html.Div(id="navbar-container"),
        # Page Content -- Div that contains page layout
        html.Div(id='page_content', className='m-2 p-0'),
    ]
)

@app.callback(
    [Output('navbar-container', 'children'), Output('page_content', 'children')],
    [Input('url', 'pathname')]
)
def displaypage(pathname):
    # Check if the current path is the login page
    if pathname == '/' or pathname == '/login':
        return None, login.layout
    elif pathname == '/home':
        return cm.navbar, home.layout
    elif pathname == '/clients':
        return cm.navbar, client_management.layout
    elif pathname == '/client/client_management_profile':
        return cm.navbar, client_management_profile.layout
    elif pathname == '/jobs':
        return cm.navbar, jobs_management.layout
    elif pathname == '/jobs/jobs_management_profile':
        return cm.navbar, jobs_management_profile.layout
    elif pathname == '/va':
        return cm.navbar, va_management.layout
    elif pathname == '/va/va_management_profile':
        return cm.navbar, va_management_profile.layout
    elif pathname == '/skills':
        return cm.navbar, skills_management.layout
    elif pathname == '/skills/skills_management_profile':
        return cm.navbar, skills_management_profile.layout
    elif pathname == '/profile':
        return cm.navbar, profile.layout
    elif pathname == '/reports':
        return cm.navbar, report.layout
    else:
        return cm.navbar, html.Div("404: Page not found")

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)