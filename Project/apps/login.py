import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db


layout = dbc.Container([
    dbc.Row(html.Br()),
    dbc.Row(html.Br()),
    dbc.Row(html.Br()),
    dbc.Row(html.Br()),
    dbc.Row(html.Br()),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.CardImg(src="https://d1hbpr09pwz0sk.cloudfront.net/logo_url/synergy-virtual-allies-80968c75",
                                    top=True, style={"height": "128px", "width": "128px", "display": "block", "margin-left": "auto", "margin-right": "auto"})),
            ]),
            dbc.Row([
                dbc.Col(dbc.Card(
                    dbc.CardBody([
                        dbc.Row(dbc.Col(html.H2("HELLO, "))),
                        dbc.Row(dbc.Col(html.H2("WELCOME BACK!"))),
                        html.Br(),
                        dbc.Row(dbc.Col(dbc.Input(id="login_username", type="text", placeholder="Username"))),
                        html.Br(),
                        dbc.Row(dbc.Col(dbc.Input(id="login_password", type="password", placeholder="Password"))),
                        html.Br(),
                        dbc.Alert('Username or password is incorrect.', color="danger", id='login_alert', is_open=False),
                        dbc.Row(dbc.Col(dbc.Button("Log in", id="login_loginbtn",
                                                    style={'backgroundColor': '#3f587b', 'color': 'white', 'align-items': 'center', 'width': '686.4px', 'font-size': '20px', 'border-radius': '5px', 'justify-content': 'center'}, className="d-flex flex-nowrap",
                                                    ))),
                    ])
                ))
            ]),
            html.Br(),
            html.A('Signup Now!', href='/signup'),
        ]),
        dbc.Col(dbc.CardImg(src="https://www.edygrad.in/assets/images/resource/edygrad-ecosytem.png",
                            top=True, style={"height": "460px", "width": "475px", "display": "block", "margin-left": "auto", "margin-right": "auto"}))
    ])
])

@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
    ],
    [
        Input('login_loginbtn', 'n_clicks'), # begin login query via button click
        Input('sessionlogout', 'modified_timestamp'), # reset session userid to -1 if logged out
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'),   
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'), 
        State('url', 'pathname'), 
    ]
)
def loginprocess(loginbtn, sessionlogout_time,
                 
                 username, password,
                 sessionlogout, currentuserid,
                 pathname):
    
    ctx = callback_context
    
    if ctx.triggered:
        openalert = False
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    
    if eventid == 'login_loginbtn': # trigger for login process
    
        if loginbtn and username and password:
            sql = """SELECT user_id
            FROM users
            WHERE 
                user_name = %s AND
                user_password = %s AND
                NOT user_delete_ind"""
            
            # we match the encrypted input to the encrypted password in the db
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest() 
            
            values = [username, encrypt_string(password)]
            cols = ['userid']
            df = db.querydatafromdatabase(sql, values, cols)
            
            if df.shape[0]: # if query returns rows
                currentuserid = df['userid'][0]
            else:
                currentuserid = -1
                openalert = True
                
    elif eventid == 'sessionlogout' and pathname == '/logout': # reset the userid if logged out
        currentuserid = -1
        
    else:
        raise PreventUpdate
    
    return [openalert, currentuserid]


@app.callback(
    [
        Output('url', 'pathname'),
    ],
    [
        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('currentuserid', 'data'), 
    ]
)
def routelogin(logintime, userid):
    ctx = callback_context
    if ctx.triggered:
        if userid > 0:
            url = '/home'
        else:
            url = '/'
    else:
        raise PreventUpdate
    return [url]