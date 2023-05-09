import dash
import dash_auth
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

VALID_USERNAME_PASSWORD_PAIRS = {
    'tatinogues': '1234',
    'music': 'mood',
}

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

##Auth de ingreso
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS)

# design
app.title = 'Raico Analytics'
app._favicon = ("disco-de-vinilo.ico")
##themes fot plots
pd.options.plotting.backend = "plotly"
load_figure_template(["darkly"])
LOGO = "assets/disco-de-vinilo.png"

nav = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
        if page["module"] != "pages.404_not_found"
    ], navbar=True, fill=False, navbar_scroll=True, id='nav', style={
        "width": "100%",
        'height': '50px',
        "textAlign": "left",
        # "borderStyle": "solid",
        # "marginTop": '187.5',
        'marginBottom': '5px',
        'fontSize': '15px',
        'margin': '45px',
        'left': '0px',
        'margin-right':'10px',
    }
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=LOGO, height="50px"))
                ],
                align='Right',
                className="g-0",
            ),
            href="https://www.tixdatascience.com/",
            style={"textDecoration": "none",
                   #'marginLeft': '500px',
                   'margin-right': '80px',
                   #'marginTop': '50px',
                   'margin': '20px'},
        ), width=1),
        dbc.Col([nav], align='left', width=6),
    ]),
    dbc.Row([
        dbc.Col([
            dash.page_container
        ])
    ]),
], fluid=True)

# run app
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8012)
