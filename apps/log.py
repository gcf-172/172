from dash import html, dcc

layout = html.Div(
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'height': '100vh',
        'backgroundColor': '#ffffff',
        'flexDirection': 'row',  # Updated from column to row to align items side by side
    },
    children=[
        # Right Section: Log In Section
        html.Div(
            style={
                'backgroundColor': '#fff',
                'borderRadius': '20px',
                'padding': '50px',
                'boxShadow': '0px 6px 6px rgba(0, 0, 0, 0.25)',
                'width': '450px',
                'height': '600px',
                'textAlign': 'center',
                'marginLeft': '100px',
                'marginRight': '100px'
            },
            children=[
                html.Img(src="/assets/synergyvirtual_logo.jpg",  style={'width': '128px', 'marginBottom': '5px', 'display': 'block', 'marginLeft': 'auto', 'marginRight': 'auto', 'borderRadius': '100px'}),
                html.H2("HELLO,", style={'fontSize': '28px', 'textAlign': 'left', 'marginBottom': '5px', 'fontWeight': 'bold', 'color': '#2E2C2C'}),
                html.H2("WELCOME BACK!", style={'fontSize': '28px', 'textAlign': 'left', 'marginBottom': '30px', 'fontWeight': 'bold', 'color': '#2E2C2C'}),
                html.Label("Username", style={'display': 'block', 'textAlign': 'left', 'fontSize': '14px', 'color': '#2E2C2C'}),
                dcc.Input(id='username', type='text', placeholder="Username",
                          style={'width': '100%', 'padding': '12px', 'marginBottom': '20px', 'border': '1px solid #B7B7B7', 'borderRadius': '10px'}),
                html.Label("Password", style={'display': 'block', 'textAlign': 'left', 'fontSize': '14px', 'color': '#2E2C2C'}),
                dcc.Input(id='password', type='password', placeholder="Password",
                          style={'width': '100%', 'padding': '12px', 'marginBottom': '20px', 'border': '1px solid #B7B7B7', 'borderRadius': '10px'}),
                html.Button("LOG IN", id='login-button', n_clicks=0,
                            style={
                                'backgroundColor': '#3f587b', 
                                'color': '#fff', 
                                'width': '100%', 
                                'height': '50px',
                                'borderRadius': '10px',
                                'fontWeight': '600',
                                'border': '0px solid #B7B7B7',
                                'boxShadow': '0px 4px 4px rgba(0, 0, 0, 0.25)',
                                'fontSize': '16px',
                            }),
                html.Div(id='login-error', style={'color': 'red', 'marginTop': '10px'}),

                html.Div(
                    children=[
                        html.P("Don't have an account yet?", style={
                            'fontSize': '14px',
                            'color': '#2E2C2C',
                            'marginTop': '20px',
                            'marginBottom': '5px'
                        }),
                        dcc.Link("Sign up here", href='/signup', refresh=True, style={
                            'color': '#194D62',
                            'fontWeight': '600',
                            'fontSize': '14px',
                            'textDecoration': 'none'
                        })
                    ]
                ),
            ]
        ),
        # Left Section: Dental Studio Database Text
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
                html.P("Welcome to the admin portal. Please log in to continue.",
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
        )    
    ]
)