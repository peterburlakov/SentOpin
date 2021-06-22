from pandas.io.formats import style
import dash
import dash_core_components as dcc
import dash_html_components as html
 
import plotly.express as px  # (version 4.7.0)
import numpy as np

from django_plotly_dash import DjangoDash
from django.shortcuts import render
from dash.dependencies import Input, Output
from collections import Counter 
from .services import DataProvider

data_provider = DataProvider()

app = DjangoDash('SimpleExample')

app.layout = html.Div(id='main', children = [
    html.Div([
        # dcc.Location(id='url', refresh=False),
        html.Div(id='url_slug', style = {'visibility': 'hidden'}),
        dcc.RadioItems(
                    id='agent_type',
                    options=[{'label':'Agent','value': True}, {'label':'notAgent', 'value': False},
                             {'label':'All', 'value':'All'}],
                    value='All',
                    style={'text-align': 'left', 'label': "jvkfjv"},
                    labelClassName='isAgent',
                    labelStyle={'display': 'inline-block'}
                ),    
        html.Div([
            dcc.Dropdown(id="slct_type",
                         options=[{'label':state, 'value':state} for state in ['service', 'commercial', 'overall', 'people']],
                         multi=False,
                         value='overall',
                         style={'width': "40%"}
                         ),
        ]),
        dcc.RadioItems(
                    id='value_type',
                    options=[{'label': str(i), 'value': i} for i in ['rating', 'sentiment']],
                    value='sentiment',
                ),   
        html.Div(id='output_container', children=[]),
        html.Br(),

        dcc.Graph(id='my_bee_map', figure={})
    ])
])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')
    ],
    [
     Input(component_id='url_slug', component_property='children'),
     Input(component_id='agent_type', component_property='value'),
     Input(component_id='slct_type', component_property='value'),
     Input(component_id='value_type', component_property='value')
    ]
)


def update_graph(url_slug, agent_type, slct_type, value_type):
    def get_num_items(x, value_to_find:str):
        idx = [index+1 for index, value in enumerate(x) if value == value_to_find]
        return str(dict(Counter(np.array(x)[idx])))

    df = data_provider.get_data(url_slug)
    if slct_type != 'overall':
        
        #df[slct_type] = df['expertai_classification'].apply(lambda x: True if slct_type in x else False)
        
        #df = df[df[slct_type] == True]
        df[slct_type] = df['items'].apply(lambda x: True if slct_type in x else False)
        df = df[df[slct_type] == True]
        #df[slct_type] = df['text'].apply(lambda x: True if slct_type in x else False)
        #df = df[df[slct_type] == True]
    
    if agent_type == 'All':
        columns_to_group = ['place_state']
    else:
        columns_to_group = ['place_state', 'isAgent']
    
    df_grouped = df\
    .groupby(columns_to_group, as_index = False)\
    .agg({
        'items': 'sum', 
        'entities': 'sum', 
        'phrases': 'sum',
        'rating':'mean', 
        'sentiment.overall':'mean',
        'expertai_classification':'count',
        'latitude': 'mean',
        'longitude': 'mean'
    }).reset_index()

    df_grouped['names'] = df_grouped.entities.apply(get_num_items, args={'NPH'})
    
    
    if agent_type != 'All':
        df_grouped = df_grouped[df_grouped["isAgent"] == agent_type]
    
    mean_rating = round(df_grouped.rating.mean(), 2)
    mean_sentiment = round(df_grouped['sentiment.overall'].mean(), 2)
    
    container = f"The state mean rating: {mean_rating}, mean sentiment: {mean_sentiment}"
    
    if value_type == 'rating':
        color = 'rating'
    else:
        color = "sentiment.overall"
        
    fig = px.scatter_mapbox(df_grouped, lat="latitude", lon="longitude", color=color, size= [12] * len(df_grouped),
            color_continuous_scale=px.colors.sequential.Viridis,
            size_max=40, zoom=2,
            mapbox_style = 'carto-positron',
            hover_name = 'place_state',
            hover_data=["rating"],
            
    )

    fig.update_layout(
        title_text = f'{slct_type} by State',
        geo_scope='usa', # limite map scope to USA,
        
    )
    return container, fig