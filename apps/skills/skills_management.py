import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from dbconnect import getDataFromDB
from app import app

layout = dbc.Container([
    # Title Row for Skill Profile Management
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(
                        'SKILL DIRECTORY', 
                        style={"marginBottom": "0px"}  # Reduce space below heading
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Add New Skill",
                    href='/skills/skills_management_profile?mode=add',
                    style={"borderRadius": "20px", "fontWeight": "bold", "fontSize": "18px", "backgroundColor": "#194D62", "color": "white", "marginBottom": "0px"},
                    className="float-end"
                ),
                md=4,
                style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"},
            ),
        ],
        className="mb-1", # Adjust margin-bottom of row
        align="center"
    ),
    html.Hr(),

    # Row for search bar and Add New Skill button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search Skill Name or ID", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_skill_m",  # ID for search bar
                        type="text",
                        placeholder="Enter Skill Name or ID...",
                        className="form-control",
                        style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                    ),
                ],
                md=8,
            ),
        ],
        className="mb-4",
        align="center"
    ),

    # Row for the table placeholder
    dbc.Row(
        dbc.Col(
            html.Div(
                id="skill-table",  # ID for table placeholder
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "0px", "height": "100%"}  # Adjust height here
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

@app.callback(
    Output('skill-table', 'children'),
    [
    Input('search_skill_m', 'value'),
    ]
)

def update_records_table(skillfilter):
    # Base SQL query for the skill table
    sql = """
        SELECT 
            s.skill_id,
            s.skill_m AS "Skill Name",
            s.skill_description AS "Skill Description"
        FROM
            skills s
        WHERE
            skill_delete_ind = false

    """
    val = []

    # Add the WHERE clause if a filter is provided
    if skillfilter:
        # Check if the filter is numeric to search by skill_id
        if skillfilter.isdigit():
            sql += " AND s.skill_id = %s"
            val.append(int(skillfilter))
        else:
            sql += """
                AND 
                s.skill_m ILIKE %s
            """
            val.extend([f'%{skillfilter}%'])

    # Add the GROUP BY and ORDER BY clauses
    sql += """
        ORDER BY 
        s.skill_id
    """

    # Define the column names
    col = ["Skill ID", "Skill Name", "Skill Description"]

    # Fetch the filtered data into a DataFrame
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Generating edit buttons for each Skill
    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                       href=f'/skills/skills_management_profile?mode=edit&id={row["Skill ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]
    display_columns = ["Skill Name", "Skill Description", "Action"]
    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(df[display_columns], striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]
