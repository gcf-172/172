import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, State
from dash.exceptions import PreventUpdate

# Sample in-memory database (replace with your database connection logic)
va_database = [
    {"va_id": "1", "va_name": "Fumi Cabrales", "va_email": "fumi@hohgymnj.com", "date_hired": "2023-01-15"},
    {"va_id": "2", "va_name": "Cheska Miranda", "va_email": "cheska@hohgymnj.com", "date_hired": "2023-02-01"}
]

# Define layout for adding/editing Virtual Assistant
layout = html.Div([
    dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H2("Virtual Assistant Management", className="text-center text-primary mb-4"),
                width=12
            )
        ),
        dbc.Row(
            [
                dbc.Col([
                    dbc.Label("VA Name", className="form-label"),
                    dbc.Input(id="va-name", type="text", placeholder="Enter VA name", className="mb-3"),
                ], md=6),
                dbc.Col([
                    dbc.Label("Email Address", className="form-label"),
                    dbc.Input(id="va-email", type="email", placeholder="Enter email address", className="mb-3"),
                ], md=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([
                    dbc.Label("Date Hired", className="form-label"),
                    dcc.DatePickerSingle(
                        id="va-date-hired",
                        placeholder="Select date hired",
                        className="mb-3"
                    ),
                ], md=6),
                dbc.Col([
                    html.Div(id="va-id-container", hidden=True),  # Hidden container for VA ID during edit
                ], md=6)
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Save", id="save-va", color="primary", className="mt-3"),
                width=12,
                className="text-center"
            )
        ),
        html.Div(id="save-feedback", className="mt-3"),
        dbc.Row(
            dbc.Col(
                dcc.Link("Back to Virtual Assistant Database", href="/va", className="btn btn-secondary mt-4")
            )
        )
    ])
])


@callback(
    [Output("va-name", "value"), 
     Output("va-email", "value"), 
     Output("va-date-hired", "date"),
     Output("va-id-container", "children")],
    [Input("url", "search")]
)
def load_va_details(search):
    """Load VA details for editing if in edit mode."""
    import urllib.parse
    if not search:
        raise PreventUpdate

    query = urllib.parse.parse_qs(search.lstrip('?'))
    mode = query.get("mode", [""])[0]
    va_id = query.get("id", [""])[0]

    if mode == "edit" and va_id:
        # Find VA details
        va = next((entry for entry in va_database if entry["va_id"] == va_id), None)
        if va:
            return va["va_name"], va["va_email"], va["date_hired"], va["va_id"]
    return "", "", None, ""  # Default empty values for "add" mode


@callback(
    Output("save-feedback", "children"),
    [Input("save-va", "n_clicks")],
    [State("va-name", "value"), State("va-email", "value"), State("va-date-hired", "date"), State("va-id-container", "children")]
)
def save_va_entry(n_clicks, name, email, date_hired, va_id):
    """Save or update VA entry."""
    if not n_clicks:
        raise PreventUpdate

    if not name or not email or not date_hired:
        return dbc.Alert("All fields are required!", color="danger")

    if va_id:
        # Update existing entry
        for va in va_database:
            if va["va_id"] == va_id:
                va.update({"va_name": name, "va_email": email, "date_hired": date_hired})
                return dbc.Alert("Virtual Assistant updated successfully!", color="success")
    else:
        # Add new entry
        new_id = str(len(va_database) + 1)
        va_database.append({"va_id": new_id, "va_name": name, "va_email": email, "date_hired": date_hired})
        return dbc.Alert("New Virtual Assistant added successfully!", color="success")

    return dbc.Alert("An error occurred. Please try again.", color="danger")
