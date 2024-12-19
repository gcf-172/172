import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate
from app import app

# Layout definition
layout = dbc.Container(
    [
        dbc.Row(
            [
                # Right column with welcome text
                dbc.Col(
                    [
                        html.H1("WELCOME TO THE SYNERGY VIRTUAL NETWORK!", className="display-4 fw-bold text-black text-center"),
                        html.Hr(),
                        html.P(
                            [
                                "The ",
                                html.Strong("Synergy VA Network"),
                                " is a platform designed to assist Synergy VA’s administrative staff in managing agency databases, matching clients with virtual assistants, and generating business reports."
                            ],className="fs-5 text-black",
                        ),
                        html.Br(),
                        html.P(
                            [
                                html.Strong("What are the main features of the network?")
                            ], className="fs-5 text-black",
                        ),
                        html.Br(),
                        html.P(
                            ["Synergy VA offers the following functions across its tabs:"],
                            className='fs-5 text-black'
                        ),
                        html.Br(),
                        html.P(
                            [
                                html.Strong("•Jobs:"),
                                " Oversee active jobs and match VAs to client requirements."                                
                            ], className='fs-5 text-black', style={'margin-left': '30px'}
                        ),
                        html.P(
                            [
                                html.Strong(" •Clients:"),
                                " Add, store, and delete client information in a centralized database."                                
                            ], className='fs-5 text-black', style={'margin-left': '30px'}
                        ),
                        html.P(
                            [
                                html.Strong("•VAs:"),
                                " Manage a database of VAs by adding, storing, and deleting their information."                                
                            ], className='fs-5 text-black', style={'margin-left': '30px'}
                        ),
                        html.P(
                            [
                                html.Strong("•Skills:"),
                                " Track and manage the skill sets of the VA manpower."                                
                            ], className='fs-5 text-black', style={'margin-left': '30px'}
                        ),
                        html.P(
                            [
                                html.Strong("•Reports:"),
                                " Generate business statistics and performance reports for better decision-making."                                
                            ], className='fs-5 text-black', style={'margin-left': '30px'}
                        ),                         
                    ],
                    md=6,
                    className="align-self-center p-4",  # Add padding inside the left column
                ),
                
                # Right column with main image and smaller images
                dbc.Col(
                    [
                        # Main image with border and padding
                        html.Div(
                            html.Img(
                                src="/assets/360_F_771468330_XEo6fKX6bnqNmIh2nzmQ4ivobbPrfOnT.jpg", 
                                style={'width': '100%', 'height': '60vh'}
                            ),  # Replace with main image path
                            style={
                                'padding': '2px',
                                'margin-top': '120px',
                                'horizontal-align': 'middle'
                            }
                        ),
                    ],
                ),
            ],
            className="m-0",
        ),
    ],
    fluid=True,
    style={'padding': '5px', 'backgroundColor': '#FFFFFF', 'height': '80vh'}  # Updated background color
)