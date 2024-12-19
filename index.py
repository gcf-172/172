import webbrowser
import dash
import dash_bootstrap_components as dbc
import hashlib
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Importing your app variable from app.py so we can use it
from app import app
from apps import commonmodules as cm
from apps import reports
from apps.clients import client_management_profile, client_management
from apps.va import va_management, va_management_profile, va_skills
from apps.jobs import jobs_management, jobs_management_profile, jobs_info
from apps.skills import skills_management, skills_management_profile
import dbconnect as db
from apps import log
from apps import signup
from apps import home

# Define styles for active and inactive navbar links
navlink_style = {'color': '#c3d1e4', 'font-size': '20px', 'margin-right': '2.5em'}
navlink_active_style = {'color': '#fff', 'font-size': '20px', 'borderBottom': '3px solid skyblue', 'margin-right': '2.5em'}

# Main layout of the app
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        html.Div(id='navbar-container'),  # Navbar container to toggle visibility
        html.Div(id='page_content', className='m-2 p-2'),
    ]
)

# Callback to update the active link styling based on URL path
@app.callback(
    [Output("nav-jobs", "style"),
     Output("nav-client-profile", "style"),
     Output("nav-va-profile", "style"),
     Output("nav-skills", "style"),
     Output("nav-report", "style")
     ],
    [Input("url", "pathname")]
)
def update_active_link_style(pathname):
    styles = [navlink_style] * 5  # Default styles

    if pathname == "/jobs_profile_info" or pathname== "/jobs_profile_details":
        styles[0] = navlink_active_style
    elif pathname == "/client_profile":
        styles[1] = navlink_active_style
    elif pathname == "/va_profile_info" or pathname=="/va_skills":
        styles[2] = navlink_active_style
    elif pathname == "/skills":
        styles[3] = navlink_active_style
    elif pathname == "/reports":
        styles[4] = navlink_active_style

    return styles

# Callback to toggle the navbar and render correct page content
@app.callback(
    [Output('navbar-container', 'children'),
     Output('page_content', 'children')],
    Input('url', 'pathname'),
    
)
def display_page_content(pathname):
    # Hide navbar for login page
    if pathname == '/login' or pathname == '/':
        return None, log.layout
    elif pathname == '/signup':
        return None, signup.layout
    elif pathname == '/home':
        return cm.navbar, home.layout
    elif pathname == '/jobs_profile_details':
        return cm.navbar, jobs_management.layout
    elif pathname == '/jobs_profile/jobs_management_profile':
        return cm.navbar, jobs_management_profile.layout
    elif pathname == '/jobs_profile_info':
        return cm.navbar, jobs_info.layout
    
    elif pathname == '/client_profile':
        return cm.navbar, client_management.layout
    elif pathname == '/client_profile/client_management_profile':
        return cm.navbar, client_management_profile.layout
    
    elif pathname == '/reports':
        return cm.navbar, reports.layout        
    
    elif pathname == '/va_profile_info':
        return cm.navbar, va_management.layout
    elif pathname == '/va_profile/va_management_profile':
        return cm.navbar, va_management_profile.layout
    elif pathname == '/va_skills':
        return cm.navbar, va_skills.layout
        
    elif pathname == '/skills/skills_management_profile':
        return cm.navbar, skills_management_profile.layout
    elif pathname == '/skills':
        return cm.navbar, skills_management.layout
    else:
        return cm.navbar, html.Div("404 - Page not found", style={'color': 'red', 'font-size': '24px', 'text-align': 'center'})

@app.callback(
    [Output('url', 'pathname'), Output('login-error', 'children')],
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def handle_login(n_clicks, username, password):
    if n_clicks > 0:  # Ensure the button was clicked
        if not username or not password:
            return dash.no_update, "Please enter both username and password."
        
        def encrypt_string(string):
            return hashlib.sha256(string.encode('utf-8')).hexdigest()
        
        sql = """SELECT user_password FROM users WHERE user_name = %s AND user_delete_ind = false"""
        values = [username]
        df_result = db.getDataFromDB(sql, values, ['user_password'])

        if not df_result.empty:  # Check if user was found
            stored_password = df_result.iloc[0]['user_password']  # Get the first row's password
            if encrypt_string(password) == stored_password:  # Compare the hashed passwords
                return "/home", ""  # Redirect to home
            else:
                return dash.no_update, "Invalid username or password. Please try again."
        else:
            return dash.no_update, "Invalid username or password. Please try again."
    
    raise PreventUpdate  # No action if not clicked

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/login', new=0, autoraise=True)
    app.run_server(debug=False)
