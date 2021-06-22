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

app = DjangoDash('SentOpinDash')


   

app.layout = html.Div(id='main', children = [
    html.Div(id='url_slug', style = {'visibility': 'hidden'}),
    html.Div(id='output_container', children=[]),
    html.Div([
        html.Div( [
            dcc.Graph(id='my_bee_map', figure={}, style = {'display': '100%'})
        ], ),
        html.Div( [
            html.Div([
                html.Label('Unity type:'),
                dcc.Dropdown(id="agent_type",
                    options=[{'label': group, 'value': group} for group in ['Agent', 'NotAgent', 'All']],
                    multi=False,
                    value='All'),
            ], style = {'width': '25%'}),
            html.Div([
                html.Label('Comment category:'),
                dcc.Dropdown(id="slct_type",
                            options=[{'label':state, 'value':state} for state in ['Overall', 'Service', 'Commercial', 'People']],
                            multi=False,
                            value='Overall',
                            ),
                    ], style = {'width': '25%'}),
            html.Div([
                html.Label('Group by:'),
                dcc.Dropdown(id="slct_group",
                            options=[{'label':group, 'value':group} for group in ['State', 'Unit']],
                            multi=False,
                            value='Unit'),
                    ], style = {'width': '25%'}),
            html.Div([
                html.Label('Show:'),
                dcc.Dropdown(id="value_type",
                                options=[{'label':group, 'value':group} for group in ['Rating', 'Sentiment']],
                                multi=False,
                                value='Sentiment',
                                ),
                    ], style = {'width': '25%'}),
        ], style = { 'display': 'flex'}), 
        
    ], ) 
])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')
    ],
    [
     Input(component_id='url_slug', component_property='children'),
     Input(component_id='agent_type', component_property='value'),
     Input(component_id='slct_type', component_property='value'),
     Input(component_id='slct_group', component_property='value'),
     Input(component_id='value_type', component_property='value'),
    ]
)





 

    

def update_graph(url_slug, agent_type, slct_type,slct_group, value_type, **args):
    slct_type = slct_type.lower()
    value_type = value_type.lower()
    if agent_type == 'Agent':
        agent_type = True 
    elif agent_type == 'NotAgent':
        agent_type = False
    else:
        agent_type = 'All'

    def get_num_items(x, value_to_find:str):
            idx = [index+1 for index, value in enumerate(x) if value == value_to_find]
            return str(dict(Counter(np.array(x)[idx])))
        
    def get_sentiment(x):
        if x < 0:
            return 0
        if x >= 0 and x < 5:
            return 1
        if x>= 5 and x<10:
            return 2
        if x > 10 and x<20:
            return 3
        if x>20 and x < 50:
            return 4
        return 5

    def by_state(df, slct_type, agent_type, value_type):

        if slct_type != 'overall':
            df[slct_type] = df['text'].apply(lambda x: True if slct_type in x else False)
            df = df[df[slct_type] == True]

        
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


        mean_sentiment = round(np.array([get_sentiment(v) for v in df_grouped['sentiment.overall']]).mean(), 2)

        container = (mean_rating, mean_sentiment)
        
        if value_type == 'rating':
            color = 'rating'
        else:
            df_grouped['sentiment'] = df_grouped['sentiment.overall'].apply(get_sentiment)
            color = "sentiment"
            
        fig = px.scatter_mapbox(df_grouped, lat="latitude", lon="longitude", color=color, size= [11] * len(df_grouped),
                color_continuous_scale=px.colors.sequential.haline,
                size_max=40, zoom=2,
    #             text='names',
                mapbox_style = 'carto-positron',
                hover_name = 'place_state',
                hover_data=["rating"],
        )
        return container, fig

    def by_unit(df, slct_type, agent_type, value_type):
        
            
        
        if slct_type != 'overall':
            df[slct_type] = df['text'].apply(lambda x: True if slct_type in x else False)
            df = df[df[slct_type] == True]

    

        
        df_grouped = df\
        .groupby(['place_id', 'place_state', 'place_formatted_address', 'latitude', 'longitude', 'isAgent'], as_index = False)\
        .agg({
            'items': 'sum', 
            'entities': 'sum', 
            'phrases': 'sum',
            'rating':'mean', 
            'sentiment.overall':'mean',
            'expertai_classification':'count'
        })

    

        df_grouped['names'] = df_grouped.entities.apply(get_num_items, args={'NPH'})

    
        if agent_type != 'All':
            df_grouped = df_grouped[df_grouped["isAgent"] == agent_type]
            
        mean_rating = round(df_grouped.rating.mean(), 2)
        mean_sentiment = round(np.array([get_sentiment(v) for v in df_grouped['sentiment.overall']]).mean(), 2)

        
        container = (mean_rating, mean_sentiment)
        df_grouped['sentiment'] = df_grouped['sentiment.overall'].apply(get_sentiment)
        
        fig = px.scatter_mapbox(df_grouped, lat="latitude", lon="longitude", color="sentiment", size='rating',
                color_continuous_scale=px.colors.sequential.haline,
                size_max=10, zoom=2,
                text='names',
                mapbox_style = 'carto-positron',
                hover_name = 'place_formatted_address',
                hover_data=["names", "rating"],
        )
        return container, fig
    





        
    df = data_provider.get_data(url_slug)
    
    if slct_group == 'State':
        container, fig = by_state(df=df, slct_type=slct_type, agent_type=agent_type, value_type=value_type)
    else:
        container, fig = by_unit(df=df, slct_type=slct_type, agent_type=agent_type, value_type=value_type)
    fig.update_layout(
        title_text = f'{slct_type.capitalize()} by {slct_group}: The mean rating: {container[0]}, mean sentiment: {container[1]}',
        geo_scope='usa', # limite map scope to USA
    )
    return '', fig
    
 




