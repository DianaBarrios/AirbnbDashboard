# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import numpy as np

import plotly.offline as py     #(version 4.4.1)
import plotly.graph_objs as go

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'pink': '#FF5A5F',
    'darkGray': '#484848',
    'lightGray': '#767676',
    'green': '#00A699',
    'orange': '#FC642D',
    'yellow': '#fdfd96',
    'blue': '#81dafc'
}

df = pd.read_csv('./AB_NYC_2019.csv')

conditions = [
    (df['neighbourhood_group'] == 'Manhattan'),
    (df['neighbourhood_group'] == 'Brooklyn'),
    (df['neighbourhood_group'] == 'Bronx'),
    (df['neighbourhood_group'] == 'Queens'),
    (df['neighbourhood_group'] == 'Staten Island')
    ]

# create a list of the values we want to assign for each condition
values = [colors['pink'], colors['green'], colors['blue'], colors['yellow'], colors['orange']]

# create a new column and use np.select to assign values to it using our lists as arguments
df['color'] = np.select(conditions, values)

figPrice = px.box(df, 
    x="neighbourhood_group", 
    y="price", 
    color="room_type",
    title = "Prices distribution by room type and neighbourhood group",
    range_y =[0,3000]
)

figPercent = px.histogram(df, 
    x="neighbourhood_group", 
    color="room_type",
    title = 'Room type and neighbourhood group'
) 

figPriceMinNights = px.scatter(df, 
    x="minimum_nights", 
    y="price", 
    color="number_of_reviews",
    title = 'Price by minimum nights',
    range_x =[0,350]
)

fig1 = px.histogram(df, x="price")

fig3 = px.histogram(df, x="neighbourhood_group")

fig4 = px.histogram(df, x="neighbourhood", color="neighbourhood_group")

#figMapNeighbourhood = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="neighbourhood_group", size="price",
         #         color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
          #        mapbox_style="carto-positron")

app.layout = html.Div(children=[
    html.H1(children='Airbnb NYC',
        style={
            'textAlign': 'center',
            'color': colors['pink']
        }
    ),

    html.Div(children='''
        Data visualization of Airbnb NYC data.
    ''',
    style={
            'textAlign': 'center',
            'color': colors['darkGray']
        }
    ),

    html.Div(children = [
        html.Div(children=[
            dcc.Graph(
                    id='map-neighbourhood',
                    config={'displayModeBar': False,
                            'scrollZoom': True
                    }
            )
        ],
        className='col-lg-8'
        ),
        html.Div(children=[
            html.Div(children=[
                html.H6(children='Neighbourhood group',
                    style={
                        'textAlign': 'left',
                        'color': colors['green']
                    }
                ),
                dcc.Checklist(
                    id='neighbourhood_group',
                    options=[
                        {'label': 'Brooklyn', 'value': 'Brooklyn'},
                        {'label': 'Manhattan', 'value': 'Manhattan'},
                        {'label': 'Queens', 'value': 'Queens'},
                        {'label': 'Staten Island', 'value': 'Staten Island'},
                        {'label': 'Bronx', 'value': 'Bronx'}
                    ],
                    value=[n for n in sorted(df['neighbourhood_group'].unique())],
                    className='mx-5',
                    style={
                        'display': 'flex',
                        'flex-direction': 'column'
                    }
                ),
            ]
            ),
            html.Div(children=[
                html.H6(children='Room type',
                    style={
                        'textAlign': 'left',
                        'color': colors['green']
                    }
                ),
                dcc.Checklist(
                    id='check_type',
                    options=[
                        {'label': 'Entire home/apt', 'value': 'Entire home/apt'},
                        {'label': 'Private room', 'value': 'Private room'},
                        {'label': 'Shared room', 'value': 'Shared room'}
                    ],
                    value=[n for n in sorted(df['room_type'].unique())],
                    className='mx-5',
                    style={
                        'display': 'flex',
                        'flex-direction': 'column'
                    }
                ),
            ]
            ),
            html.Div(children=[
                html.H6(children='Price range',
                    style={
                        'textAlign': 'left',
                        'color': colors['green']
                    }
                ),
                dcc.RangeSlider(
                    id='slider-price',
                    min=0,
                    max=3800,
                    step=10,
                    value=[0,3800],
                    marks={
                        500: '$500',
                        1000: '$1000',
                        2000: '$2000',
                        3000: '$3000'
                    },
                ), 
            ]
            ),
            html.Div(children=[
                html.H6(children='Maximum price',
                    style={
                        'textAlign': 'left',
                        'color': colors['green']
                    }
                ),
                dcc.Input(
                    id='input-price',
                    placeholder='Enter a price...',
                    type='number',
                    value=3800,
                    style={
                        'width': '50%'
                    }
                )  
            ]
            )
        ],
        className='col-lg-4',
        style={
            'display': 'flex',
            'flex-direction': 'column',
            'justify-content': 'space-evenly'
        }
        )
    ],
        className = 'row my-5'
    ),

    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
                    id='price _min_nights',
                    figure=figPriceMinNights,
            )
        ],
        className='col-lg-6'
        ),
        html.Div(children=[
            dcc.Graph(
                    id='room_type_neighbourhood',
                    figure=figPercent
            )
        ],
        className='col-lg-6'
        )
    ],
    className = 'row my-5'
    ),

    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
                    id='price_stats',
                    figure=figPrice,
            )
        ],
        className='col-lg-8'
        ),
        html.Div(children=[
            html.H6(children='Neighbourhood group',
                    style={
                        'textAlign': 'left',
                        'color': colors['green']
                    }
            ),
            dcc.RadioItems(
                id='radio-neighbourhood',
                options=[
                        {'label': 'Brooklyn', 'value': 'Brooklyn'},
                        {'label': 'Manhattan', 'value': 'Manhattan'},
                        {'label': 'Queens', 'value': 'Queens'},
                        {'label': 'Staten Island', 'value': 'Staten Island'},
                        {'label': 'Bronx', 'value': 'Bronx'}
                ],
                value='Brooklyn',
                style={
                        'display': 'flex',
                        'flex-direction': 'column'
                }
            ),
        ],
        className='col-lg-4',
        style={
            'display': 'flex',
            'flex-direction': 'column',
            'justify-content': 'center'
        }
        )
    ],
    className = 'row my-5'
    ),
],
    style = {
            'color': colors['darkGray'],
            'fontSize': 14,
            'fontFamily': 'sans-serif'
        }
)

#output of map
@app.callback(
   Output('map-neighbourhood','figure'),
   [Input('neighbourhood_group','value'),
    Input('slider-price','value'),
    Input('input-price','value'),
    Input('check_type','value')
   ] 
)

def update_figure(chosen_neighbourhood,max_price,i_price,room_type):
    df_sub = df[
        (df['neighbourhood_group'].isin(chosen_neighbourhood)) &
        (df['price'] > max_price[0]) & 
        (df['price'] <= max_price[1]) &
        (df['price'] <= i_price) &
        (df['room_type'].isin(room_type)) 
        ]

    # Create figure
    locations = [go.Scattermapbox(
        lon = df_sub['longitude'],
        lat = df_sub['latitude'],
        mode='markers',
        marker={'color' : df_sub['color']},
        hoverinfo='text',
        hovertext=df_sub['price'],
        text = df_sub['name'],
        hovertemplate ="%{text} <br> $%{hovertext} </br> <extra></extra>"
    )]

    return {
        'data': locations,
        'layout': go.Layout(
            uirevision = 'foo',
            clickmode = 'event+select',
            hovermode = 'closest',
            hoverdistance=5,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="sans-serif"
            ),
            title = dict(text="Explore NYC neighbourhoods and prices"),
            height=700,
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiZGlhbmEtYmFycmlvcyIsImEiOiJja2draGh5dTMwMmFlMnRvb3lqa21ycG9oIn0.TlhgOhPy3dPkxEvfeAz2zQ',
                bearing=25,
                style='light',
                center=dict(
                    lat=40.80105,
                    lon=-73.945155
                ),
                pitch=40,
                zoom=11.5
            )
        )
    }


"""
#output of graph
@app.callback(
   Output('price_stats','figure'),
   [
       Input('radio-neighbourhood','value')
   ] 
)

def update_figure(chosen_nb):
    df_b = df[
        (df['neighbourhood_group'].isin(chosen_nb)) 
        ]

    # Create figure
    bxplot = go.Figure()
    bxplot.add_trace(go.Box(
        x=df_b['neighbourhood_group'] 
        y=df_b['price']
    ))

    return {
        'data': bxplot,
        'layout': go.Layout(
            uirevision = 'foo',
            clickmode = 'event+select',
            hovermode = 'closest',
            hoverdistance=5,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="sans-serif"
            ),
            title = dict(text="Prices"),
            height=700
        )
    }


"""

if __name__ == '__main__':
    app.run_server(debug=True)