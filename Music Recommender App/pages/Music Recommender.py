import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, html, dash_table
import pandas as pd
import numpy as np
from numpy.linalg import norm
import plotly.express as px
from dash import dash_table

dash.register_page(__name__, path='/RECOMMENDER', name='MUSIC RECOMMENDER')

df = pd.read_csv('data/scraped_spotify_dataset_ok.csv')
df = df.head(500)

#Dropdowns
feelings = ['😄 Excited', '😊 Happy', '😌 Calm', '😢 Sad', '😨 Distressed', '😴 Sleepy', '😤 Angry', '😬 Nervous']

dropdown_feeling = html.Div([dcc.Dropdown(
    [{'label': x, 'value': x} for x in feelings],
    placeholder="Choose how you are feeling",
    clearable=True,
    multi=False,
    id='filter_feelings',
    className='dropdown-class-feelings'

)],
    style={'margin-left': '85px',
           'color': 'black',
           'margin-top': '30px',
           'width': '290px'})

dropdown_feeling2 = html.Div([dcc.Dropdown(
    [{'label': x, 'value': x} for x in feelings],
    placeholder="Choose how you want to feel",
    clearable=True,
    multi=False,
    id='filter_feelings2',
    className='dropdown-class-feelings2'

)],
    style={'margin-left': '7px',
           'color': 'black',
           'margin-top': '30px',
           'width': '290px'})


table = dash_table.DataTable(id='table_container',
                             data=df.to_dict('records'),
                             columns=[{'id': c, 'name': c} for c in df.columns],
                             page_current=0,
                             page_size=10,
                             page_action="native",
                             row_selectable="multi",
                             export_format='xlsx',
                             selected_columns=[],
                             selected_rows=[],
                             style_table={'width': '1020px', 'height': '550px',
                                          'overflowX': 'auto',
                                          },
                             style_as_list_view=True,
                             style_header={
                                 'backgroundColor': 'rgb(30, 30, 30)',  # '#2a9fd6'
                                 'color': 'white',
                                 'font_family': 'Roboto'}
                             )

layout = html.Div([

    dbc.Row(dcc.Markdown('## **Music Recommender**'),
            align='left',
            style={'fontSize': '18px',
                   'marginRight': '100px',
                   'marginLeft': '95px',
                   'marginTop': '18px',
                   'color': 'white',
                   }
            ),

    dbc.Row(dcc.Markdown('''
                            ###### Select how you are feeling and how you want to feel and let music do the rest

                             '''),
            align='left',
            style={'fontSize': '20px',
                   'marginRight': '120px',
                   'marginLeft': '95px',
                   'marginTop': '8px',
                   'color': 'white',
                   }),

    dbc.Row([dropdown_feeling,
             dropdown_feeling2,
             ],
            align='left',
            style={
                'margin': '10px',
                'color': 'white',
            }
            ),

    dbc.Row([dcc.Graph(id='plot2'),
             table],
            align='center',
            style={
                'margin': '50px',
                'marginLeft': '105px',
                'marginTop': '20px',
            }
            )

])


@callback(
    [Output(component_id='plot2', component_property='figure'),
     Output(component_id='table_container', component_property='data')],
    Input(component_id='filter_feelings', component_property='value'),
    Input(component_id='filter_feelings2', component_property='value'),

)
def update_mood(selected_feeling, selected_feeling2):

    df["mood_vec"] = df[["valence_standard", "energy_standard"]].values.tolist()

    #base emotions location in the graph
    sad = [-1, -1]
    excited = [0.5, 1.5]
    happy = [1, 0.5]
    calm = [1, -1]
    distressed = [-0.5, 1.5]
    sleepy = [0, -1.5]
    angry = [-1, 1]
    nervous = [-1.5, 0]

    if selected_feeling == '😤 Angry':
        p1 = angry
    elif selected_feeling == '😢 Sad':
        p1 = sad
    elif selected_feeling == '😤 Angry':
        p1 = angry
    elif selected_feeling == '😄 Excited':
        p1 = excited
    elif selected_feeling == '😊 Happy':
        p1 = happy
    elif selected_feeling == '😌 Calm':
        p1 = calm
    elif selected_feeling == '😨 Distressed':
        p1 = distressed
    elif selected_feeling == '😴 Sleepy':
        p1 = sleepy
    elif selected_feeling == '😬 Nervous':
        p1 = nervous

    if selected_feeling2 == '😢 Sad':
        p2 = sad
    elif selected_feeling2 == '😄 Excited':
        p2 = excited
    elif selected_feeling2 == '😊 Happy':
        p2 = happy
    elif selected_feeling2 == '😌 Calm':
        p2 = calm
    elif selected_feeling2 == '😨 Distressed':
        p2 = distressed
    elif selected_feeling2 == '😴 Sleepy':
        p2 = sleepy
    elif selected_feeling2 == '😤 Angry':
        p2 = angry
    elif selected_feeling2 == '😬 Nervous':
        p2 = nervous

    x = [p1[0], p2[0]]
    y = [p1[1], p2[1]]

    coefficients = np.polyfit(x, y, 1)
    a = coefficients[0]
    b = coefficients[1]
    n = 10
    p1x = p1[0]
    p2x = p2[0]
    # cuanto vamos a sumar en x por cada n de canciones q se deseen q sean recomendadas
    sumax = (p2x - p1x) / n

    lista_x = []
    for num in range(1, n + 1):
        x1 = p1x + abs(sumax * num)
        lista_x.append(x1)

    # para cada x que esta en el rango de los puntos hallamos el valor de Y => de esta forma hallamos los Valores P
    lista_y = []
    for num in lista_x:
        y = a * num + b
        lista_y.append(y)

    lista_p = []
    for num in range(0, n):
        p = [lista_x[num], lista_y[num]]
        lista_p.append(p)

    #### hasta aca tenemos todos los puntos p => sigue hallar las canciones mas cercanas a cada punto

    df_recommended = pd.DataFrame()

    for n in range(len(lista_p)):
        point_p = lista_p[n]

        df["distances"] = df["mood_vec"].apply(lambda x: norm(point_p - np.array(x)))

        # Sort distances from lowest to highest
        df_sorted = df.sort_values(by="distances", ascending=True)
        df_sorted.reset_index(inplace=True)
        df2 = df_sorted.head(1)

        df_recommended = pd.concat([df_recommended, df2], ignore_index=True)

    dff = df_recommended
    fig = px.scatter(dff, x='valence_standard', y="energy_standard", color='Genre',
                     title="Recommended Songs",
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

    return fig, dff.to_dict('records')
