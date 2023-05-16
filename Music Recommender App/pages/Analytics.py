from dash import Dash, dcc, html, Input, Output, callback, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import plotly.express as px

pd.options.plotting.backend = "plotly"
from dash_bootstrap_templates import load_figure_template

load_figure_template(["darkly"])

dash.register_page(__name__, path='/ANALYTICS', name='ANALYTICS')

##https://fontawesome.bootstrapcheatsheets.com/

##DATA
df = pd.read_csv('data/scraped_spotify_dataset_ok.csv')

##Dropdown
genre = set(df[df.columns[1]])

dropdown_genre = html.Div([dcc.Dropdown(
    [{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in list(genre)],
    value='all-values',
    placeholder="Filter by Genres",
    clearable=True,
    multi=True,
    id='filter_genre',
    className='dropdown-class-genre'

)],
    style={'margin-left': '7px',
           'color': 'black',
           'margin-top': '30px',
           'width': '260px'},
)

artist = set(df[df.columns[3]])
dropdown_artist = html.Div([dcc.Dropdown(
    [{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in list(artist)],
    value='all-values',
    placeholder="Filter by Artist",
    clearable=True,
    multi=True,
    id='filter_artist',
    className='dropdown-class-artist'

)],
    style={'margin-left': '7px',
           'color': 'black',
           'margin-top': '30px',
           'width': '260px'})

song = set(df[df.columns[2]])
dropdown_song = html.Div([dcc.Dropdown(
    [{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in list(song)],
    value='all-values',
    placeholder="Find your favourite track",
    clearable=True,
    multi=True,
    id='filter_song',
    className='dropdown-class-song'

)],
    style={'margin-left': '7px',
           'color': 'black',
           'margin-top': '30px',
           'width': '260px'})

popularity = ['Top 100', 'Top 500', 'Top 1000']

dropdown_popularity = html.Div([dcc.Dropdown(
    [{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in popularity],
    value='all-values',
    placeholder="Filter by Popularity",
    clearable=True,
    multi=True,
    id='filter_popularity',
    className='dropdown-class-popularity'

)],
    style={'margin-left': '85px',
           'color': 'black',
           'margin-top': '30px',
           'width': '260px'})

# https://towardsdatascience.com/create-a-professional-dasbhoard-with-dash-and-css-bootstrap-e1829e238fc5


layout = html.Div([
    dbc.Row(dcc.Markdown('## **Psychology meets beats**'),
            align='left',
            style={'fontSize': '18px',
                   # 'margin': '80px',
                   'marginRight': '100px',
                   'marginLeft': '95px',
                   'marginTop': '18px',
                   'color': 'white',
                   }
            ),
    dbc.Row(dcc.Markdown('''
                            ###### Find your favourites songs and where in the Arousal - Valence plane are found
                             
                             '''),
            align='left',
            style={'fontSize': '20px',
                   # 'margin': '80px',
                   'marginRight': '120px',
                   'marginLeft': '95px',
                   'marginTop': '8px',
                   'color': 'white',
                   }),
    dbc.Row([dropdown_popularity,
             dropdown_genre,
             dropdown_artist,
             dropdown_song],
            align='left',
            style={  # 'fontSize': '20px',
                # 'margin': '80px',
                'margin': '10px',
                # 'marginLeft': '95px',
                # 'marginTop': '8px',
                'color': 'white',
            }
            ),
    dbc.Row([dcc.Graph(id='plot')],
            align='center',
            style={
                'margin': '50px',
                'marginLeft': '105px',
                'marginTop': '20px',
            }
            )
])


@callback(
    Output(component_id='plot', component_property='figure'),
    [Input(component_id='filter_popularity', component_property='value'),
     Input(component_id='filter_genre', component_property='value'),
     Input(component_id='filter_artist', component_property='value'),
     Input(component_id='filter_song', component_property='value')]
)
def update_graph(selected_popularity, selected_genre, selected_artist, selected_song):

    if selected_popularity == ['Top 100']:
        dff = df.head(100)

    elif selected_popularity == ['Top 500']:
        dff = df.head(500)

    elif selected_popularity == ['Top 1000']:
        dff = df.head(1000)

    elif selected_genre != ['all_values']:
        selected_genre = list(selected_genre)
        dff = df[df[df.columns[1]].isin(selected_genre)]

    elif selected_artist != ['all_values']:
        selected_artist = list(selected_artist)
        dff = df[df[df.columns[3]].isin(selected_artist)]

    elif selected_song != ['all_values']:
        selected_song = list(selected_song)
        dff = df[df[df.columns[2]].isin(selected_song)]

    else:
        dff = df

    fig = px.scatter(dff, x='valence_standard', y="energy_standard", color='Genre',
                     title="Music Psychology: Valence Arousal Plane",
                     labels={"valence_standard": "</b>Valence</b>",
                             "energy_standard": '</b>Arousal</b>'},
                     hover_data=["Genre", "Track", "Artist"],
                     width=1000, height=800,
                     template="plotly_dark",
                     )

    fig.add_hline(y=0, line_color="grey")
    fig.add_vline(x=0, line_color="grey")

    fig.add_annotation(x=1, y=1,
                       text="Excitement",
                       font=dict(size=15, ),
                       showarrow=False,
                       opacity=0.8)
    fig.add_annotation(x=-1, y=1,
                       text="Distress",
                       font=dict(size=15, ),
                       showarrow=False, )
    fig.add_annotation(x=-1, y=-1,
                       text="Depression",
                       font=dict(size=15, ),
                       showarrow=False,
                       )
    fig.add_annotation(x=1, y=-1,
                       text="Contentment",
                       font=dict(size=15, ),
                       showarrow=False,
                       )
    fig.add_annotation(x=0, y=-1.8,
                       text="Sleepiness",
                       font=dict(size=15, ),
                       showarrow=False,
                       )
    fig.add_annotation(x=-1.8, y=0,
                       text="Misery",
                       font=dict(size=15, ),
                       showarrow=False, bgcolor="#000000",
                       )
    fig.add_annotation(x=1.8, y=0,
                       text="Pleasure",
                       font=dict(size=15, ),
                       showarrow=False, bgcolor="#000000",
                       )

    fig.update_layout(yaxis_range=[-2, 2], xaxis_range=[-2, 2])
    return fig
