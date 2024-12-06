import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import psycopg2

# Database connection details
DB_CONFIG = {
    'dbname': 'your_database_name',
    'user': 'your_user_name',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

# Connect to the database
def fetch_data(query, params=None):
    with psycopg2.connect(**DB_CONFIG) as conn:
        return pd.read_sql_query(query, conn, params=params)

def execute_query(query, params=None):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()

# Fetch jobs and their required skills
def get_jobs():
    query = """
    SELECT j.job_id, j.start_date, j.hourly_rate, js.skill_id, s.skill_name, js.proficiency_required
    FROM job j
    JOIN job_skill js ON j.job_id = js.job_id
    JOIN skill s ON js.skill_id = s.skill_id;
    """
    return fetch_data(query)

# Fetch VAs and their skills
def get_vas():
    query = """
    SELECT v.va_id, v.va_name, vs.skill_id, s.skill_name, vs.proficiency_level
    FROM va v
    JOIN va_skill vs ON v.va_id = vs.va_id
    JOIN skill s ON vs.skill_id = s.skill_id;
    """
    return fetch_data(query)

# Save pairing in the database
def save_pairing(job_id, va_id):
    query = """
    UPDATE job
    SET va_ID = %s
    WHERE job_id = %s;
    """
    execute_query(query, (va_id, job_id))

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    html.H1("Job and VA Pairing"),
    dbc.Row([
        dbc.Col([
            html.H3("Available Jobs"),
            dcc.Dropdown(id='job-dropdown', placeholder="Select a Job"),
            html.Div(id='job-details', className="mt-3")
        ], width=6),
        dbc.Col([
            html.H3("Available VAs"),
            dcc.Dropdown(id='va-dropdown', placeholder="Select a VA"),
            html.Div(id='va-details', className="mt-3")
        ], width=6),
    ]),
    dbc.Button("Pair Job with VA", id='pair-button', color='primary', className='mt-3'),
    html.Div(id='pairing-status', className='mt-3 text-success')
])

# Callbacks
@app.callback(
    Output('job-dropdown', 'options'),
    Input('job-dropdown', 'value')
)
def load_jobs(_):
    jobs = get_jobs()
    options = [{'label': f"Job {row['job_id']} - {row['skill_name']} (Proficiency: {row['proficiency_required']})", 'value': row['job_id']} for _, row in jobs.iterrows()]
    return options

@app.callback(
    Output('job-details', 'children'),
    Input('job-dropdown', 'value')
)
def display_job_details(job_id):
    if job_id:
        jobs = get_jobs()
        job = jobs[jobs['job_id'] == job_id]
        return html.Ul([html.Li(f"{row['skill_name']} (Required: {row['proficiency_required']})") for _, row in job.iterrows()])
    return "Select a job to view details."

@app.callback(
    Output('va-dropdown', 'options'),
    Input('job-dropdown', 'value')
)
def load_vas(job_id):
    if job_id:
        jobs = get_jobs()
        required_skills = jobs[jobs['job_id'] == job_id]['skill_id'].tolist()

        vas = get_vas()
        filtered_vas = vas[vas['skill_id'].isin(required_skills)]
        options = [{'label': f"VA {row['va_name']} - {row['skill_name']} (Proficiency: {row['proficiency_level']})", 'value': row['va_id']} for _, row in filtered_vas.iterrows()]
        return options
    return []

@app.callback(
    Output('va-details', 'children'),
    Input('va-dropdown', 'value')
)
def display_va_details(va_id):
    if va_id:
        vas = get_vas()
        va = vas[vas['va_id'] == va_id]
        return html.Ul([html.Li(f"{row['skill_name']} (Proficiency: {row['proficiency_level']})") for _, row in va.iterrows()])
    return "Select a VA to view details."

@app.callback(
    Output('pairing-status', 'children'),
    Input('pair-button', 'n_clicks'),
    State('job-dropdown', 'value'),
    State('va-dropdown', 'value')
)
def pair_job_va(n_clicks, job_id, va_id):
    if n_clicks and job_id and va_id:
        save_pairing(job_id, va_id)
        return f"Job {job_id} has been successfully paired with VA {va_id}!"
    return ""

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
