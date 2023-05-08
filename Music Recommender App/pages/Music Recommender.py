import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import io
from dash import dcc, html, dash_table

dash.register_page(__name__, path='/RECOMMENDER', name='MUSIC RECOMMENDER')

image = 'assets/Estamos_trabajando.png'
layout = html.Div([

        # Use row and col to control vertical alignment of logo / brand
        dbc.Row(
            [
                dbc.Col(html.Img(src=image, height="500px"))
            ],
            align="center",
            className="g-0",
            style= {'marginLeft': '300px' }
        ),
    ])
