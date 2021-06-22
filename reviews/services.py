
import pandas as pd 
import re
import geopandas as gpd
import numpy as np


class DataProvider():

    def __init__(self) -> None:
        
        df = pd.read_csv('~/Downloads/reviews.csv', index_col=0)
        df['entities'] = df.expertai_entities.apply(lambda x: [i for i in re.sub('[\]\"  \[\,]','', x).split("'") if i!=''])
        df['items'] = df['expertai_sentiment.items'].apply(lambda x: [i for i in re.sub('[\]\"  \[\,]','', x).split("'") if i!=''])
        df['phrases'] = df['expertai_mainPhrases'].apply(lambda x: [i for i in re.sub('[\]\"\[\,]','', x).split("'") if i!=''])
        df['lemmas'] = df['expertai_mainLemmas'].apply(lambda x: [i for i in re.sub('[\]\"\[\,]','', x).split("'") if i!=''])
        df['isAgent'] = df.place_name.apply(lambda x: True if 'Agent' in x else False)

        states = sorted(np.append(df.place_state.unique().tolist(),'All'))

        url = ("https://raw.githubusercontent.com/python-visualization/folium/master/examples/data")
        state_geo = f"{url}/us-states.json"

        # We read the file and print it.
        geoJSON_df = gpd.read_file(state_geo)
        geoJSON_df.head()
        df = pd.merge(df, geoJSON_df, left_on='place_state', right_on='name')
        self.df = df 

    
    def get_data(self, search_id):
        # TODO implement selection by search_id here 
        return self.df.copy()
