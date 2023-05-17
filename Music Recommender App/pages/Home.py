import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='HOME')

button = html.Div(
    [
        dbc.Button(
            "Psychology meets beats",
            href="/ANALYTICS",
            external_link=False,
            color="warning",
        ),
    ]
)

SQUARE = "assets/este_va.png"

layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Markdown('''
                        #### MUSIC RECOMMENDER
                        \n
                        # __MOODBEATS__
                        \n
                        \n
                        ###### Music suggestions that map your mood swings :)
                                '''),
                align='center',
                width=4,
                style={'fontSize': '60px',
                       'margin': '120px',
                       'marginRight': '100px',
                       'marginLeft': '180px',
                       'marginTop': '2px',
                       'color': 'white',
                       }),

        dbc.Col(html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=SQUARE, height="600px"))
                ],
                align="right",
                className="g-0",
            ),
            href="https://www.tixdatascience.com/",
            style={"textDecoration": "none",
                   'margin-left': '0px',
                   'margin-top': '0px'},
        ), width=2)]),
    dbc.Row(
        dbc.Col(html.Div(button), width=4, align='center',
                style={'margin': '180px',
                       'marginTop': '-420px',
                       'marginBottom': '10px'})
    )]

)
