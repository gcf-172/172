from dash import dcc, html
import dash_bootstrap_components as dbc

def layout(mode="view", skill_id=None):
    if mode == "add":
        return dbc.Container([
            html.H2("Add New Skill"),
            dbc.Form([
                dbc.FormGroup([
                    dbc.Label("Skill Name"),
                    dbc.Input(type="text", id="skill-name-input", placeholder="Enter skill name"),
                ]),
                dbc.FormGroup([
                    dbc.Label("Skill Description"),
                    dbc.Textarea(id="skill-description-input", placeholder="Enter skill description"),
                ]),
                dbc.Button("Save Skill", id="save-skill-button", color="primary")
            ])
        ])
    elif mode == "edit":
        # Fetch skill details based on skill_id (e.g., from a database)
        skill = get_skill_details(skill_id)  # Replace with your data-fetching logic
        return dbc.Container([
            html.H2(f"Edit Skill - ID: {skill_id}"),
            dbc.Form([
                dbc.FormGroup([
                    dbc.Label("Skill Name"),
                    dbc.Input(type="text", id="skill-name-input", value=skill["skill_name"], placeholder="Enter skill name"),
                ]),
                dbc.FormGroup([
                    dbc.Label("Skill Description"),
                    dbc.Textarea(id="skill-description-input", value=skill["skill_description"], placeholder="Enter skill description"),
                ]),
                dbc.Button("Save Changes", id="save-skill-button", color="primary")
            ])
        ])
    else:
        return dbc.Container(html.Div("Invalid mode or missing skill ID"))
