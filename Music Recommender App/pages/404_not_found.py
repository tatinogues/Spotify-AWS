from dash import html
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/404")


image = 'assets/not_found.png'
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
