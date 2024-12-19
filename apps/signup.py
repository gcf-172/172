import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
import dbconnect as db

layout = html.Div(
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'height': '100vh',
        'backgroundColor': '#f8f9fa',  # Light background for better contrast
    },

    children=[
                html.Div(
            children=[
                html.Img(src="/assets/edygrad-ecosytem.png", style={'width': '600px', 'marginBottom': '20px', 'display': 'block', 'marginLeft': 'auto', 'marginRight': 'auto'}),  # Adjusted logo size
                html.H1("Synergy Virtual Allies Network", style={
                    'fontSize': '40px',
                    'fontWeight': 'bold',
                    'color': '#3f587b',
                    'textAlign': 'center',
                    'marginTop': '0',
                    'marginBottom': '20px'
                }),
                html.P("Welcome to Sign Up page. Please create an account to continue.",
                       style={
                           'fontSize': '18px',
                           'color': '#555',
                           'textAlign': 'center'
                       })
            ],
            style={
                'width': '50%',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '20px'
            }
        ),
        html.Div(
            style={
                'backgroundColor': '#ffffff',
                'borderRadius': '10px',
                'padding': '40px',
                'boxShadow': '0px 6px 12px rgba(0, 0, 0, 0.15)',
                'width': '450px',
                'textAlign': 'center',
                'marginRight': '100px',
                'marginLeft': '100px'
            },
            children=[
                # Header
                html.H2("Create an Account", style={
                    'marginBottom': '20px',
                    'fontWeight': 'bold',
                    'color': '#3f587b',
                }),
                html.P(
                    "Please provide your details below to create an account.",
                    style={'marginBottom': '30px', 'color': '#555'}
                ),
                
                # Alert for errors
                dbc.Alert(
                    "Please supply valid details.",
                    color="danger",
                    id='signup_alert',
                    is_open=False,
                    dismissable=True,
                ),
                
                # Username input
                dbc.Row(
                    [
                        dbc.Label("Username", html_for="signup_username", width=12, style={
                            'textAlign': 'left', 'fontWeight': 'bold', 'marginBottom': '5px'
                        }),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="signup_username",
                                placeholder="Enter a username",
                                style={'borderRadius': '5px'}
                            ),
                            width=12,
                        ),
                    ],
                    className="mb-3",
                ),
                
                # Password input
                dbc.Row(
                    [
                        dbc.Label("Password", html_for="signup_password", width=12, style={
                            'textAlign': 'left', 'fontWeight': 'bold', 'marginBottom': '5px'
                        }),
                        dbc.Col(
                            dbc.Input(
                                type="password",
                                id="signup_password",
                                placeholder="Enter a password",
                                style={'borderRadius': '5px'}
                            ),
                            width=12,
                        ),
                    ],
                    className="mb-3",
                ),
                
                # Confirm Password input
                dbc.Row(
                    [
                        dbc.Label("Confirm Password", html_for="signup_passwordconf", width=12, style={
                            'textAlign': 'left', 'fontWeight': 'bold', 'marginBottom': '5px'
                        }),
                        dbc.Col(
                            dbc.Input(
                                type="password",
                                id="signup_passwordconf",
                                placeholder="Re-type the password",
                                style={'borderRadius': '5px'}
                            ),
                            width=12,
                        ),
                    ],
                    className="mb-4",
                ),
                
                # Signup Button
                dbc.Button(
                    "Sign Up",
                    id="signup_signupbtn",
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'borderRadius': '5px',
                        'fontWeight': 'bold',
                        'backgroundColor': '#3f587b',
                        'border': 'none',
                        'color': 'white',
                        'marginBottom': '15px'
                    },
                ),


                html.Div(
                    children=[
                        dcc.Link("Back to log in", href='/login', refresh=True, style={
                            'color': '#194D62',
                            'fontWeight': '600',
                            'fontSize': '14px',
                            'textDecoration': 'none'
                        })
                    ]
                ),
                
                # Confirmation Modal
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            dbc.ModalTitle("Account Created"),
                            style={'color': '#3f587b'}
                        ),
                        dbc.ModalBody(
                            "Your account has been created successfully.",
                            id='signup_confirmation',
                            style={'color': '#555'}
                        ),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Go to Login",
                                href='/login',
                                color="primary",
                                style={'fontWeight': 'bold'}
                            ),
                        ),
                    ],
                    id="signup_modal",
                    is_open=False,
                ),   
            ]
        ),
    ]
)

# disable the signup button if passwords do not match
@app.callback(
    [
        Output('signup_signupbtn', 'disabled'),
    ],
    [
        Input('signup_password', 'value'),
        Input('signup_passwordconf', 'value'),
    ]
)
def deactivatesignup(password, passwordconf):
    
    # enable button if password exists and passwordconf exists 
    #  and password = passwordconf
    enablebtn = password and passwordconf and password == passwordconf

    return [not enablebtn]


# To save the user
@app.callback(
    [
        Output('signup_alert', 'is_open'),
        Output('signup_modal', 'is_open')   
    ],
    [
        Input('signup_signupbtn', 'n_clicks')
    ],
    [
        State('signup_username', 'value'),
        State('signup_password', 'value')
    ]
)
def saveuser(loginbtn, username, password):
    openalert = openmodal = False
    if loginbtn:
        if username and password:
            sql = """INSERT INTO users (user_name, user_password)
            VALUES (%s, %s)"""  
            
            # This lambda fcn encrypts the password before saving it
            # for security purposes, not even database admins should see
            # user passwords 
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
            
            values = [username, encrypt_string(password)]
            db.modifyDB(sql, values)
            
            openmodal = True
        else:
            openalert = True
    else:
        raise PreventUpdate

    return [openalert, openmodal]