
import pandas as pd 
import re
import geopandas as gpd
import numpy as np
import json
from .models import Search, Review

class DataProvider():

    def get_data(self, search_id):

        # TODO change search_id
        reviews = Review.objects.filter(place__search__id=1).exclude(text__exact='').select_related('place').select_related()

        data = [{
                'reviewer': obj.reviewer,
                'text': obj.text,
                'entities': obj.expertai_entities,
                'items': obj.expertai_sentiment_items,
                'phrases': [v[0] for v in obj.expertai_mainPhrases],
                'lemmas': obj.expertai_mainLemmas,
                'isAgent': True if 'Agent' in obj.place.name else False,
                'place_state': obj.place.state,
                'expertai_classification': json.dumps(obj.expertai_classification).lower(),
                'latitude': float(obj.place.lat),
                'longitude': float(obj.place.lng),
                'rating': float(obj.place.rating),
                'sentiment.overall': float(obj.sentiment_overall)
        } 

        for obj in reviews]

         

        df = pd.DataFrame.from_records(data)
         
        
        # df = pd.read_csv('~/Downloads/reviews.csv', index_col=0)
        #df['entities'] = df.expertai_entities.apply(lambda x: [i for i in re.sub('[\]\"  \[\,]','', x).split("'") if i!=''])
        #df['items'] = df['expertai_sentiment.items'].apply(lambda x: [i for i in re.sub('[\]\"  \[\,]','', x).split("'") if i!=''])
        #df['phrases'] = df['expertai_mainPhrases'].apply(lambda x: [i for i in re.sub('[\]\"\[\,]','', x).split("'") if i!=''])
        #df['lemmas'] = df['expertai_mainLemmas'].apply(lambda x: [i for i in re.sub('[\]\"\[\,]','', x).split("'") if i!=''])
        #df['isAgent'] = df.place_name.apply(lambda x: True if 'Agent' in x else False)

        states = sorted(np.append(df.place_state.unique().tolist(),'All'))

        url = ("https://raw.githubusercontent.com/python-visualization/folium/master/examples/data")
        state_geo = f"{url}/us-states.json"

        # We read the file and print it.
        geoJSON_df = gpd.read_file(state_geo)
        geoJSON_df.head()
        df = pd.merge(df, geoJSON_df, left_on='place_state', right_on='name')
        

        return df #self.df.copy()
