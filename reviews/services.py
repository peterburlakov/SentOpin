
import pandas as pd 
import re
import geopandas as gpd
import numpy as np
import json
from .models import Search, Review

class DataProvider():

    def get_data(self, search_id):

        reviews = Review.objects.filter(place__search__id=search_id).exclude(text__exact='').select_related('place').select_related()

        def flat_lists(x):
            if x:
                items = []
                for v in x:
                    items.extend(v)
                return items
            return []

        data = [{
                'reviewer': obj.reviewer,
                'text': obj.text,
                'entities': flat_lists(obj.expertai_entities),
                'items': json.dumps(obj.expertai_sentiment_items).lower(),
                'phrases': [v[0] for v in obj.expertai_mainPhrases],
                'lemmas': obj.expertai_mainLemmas,
                'isAgent': obj.place.is_agent,
                'place_state': obj.place.state,
                'expertai_classification': json.dumps(obj.expertai_classification).lower(),
                'latitude': float(obj.place.lat),
                'longitude': float(obj.place.lng),
                'rating': float(obj.place.rating),
                'sentiment.overall': float(obj.sentiment_overall),
                'place_id': obj.place.id,
                'place_formatted_address': obj.place.formatted_address
        } 
        for obj in reviews 
        if obj.sentiment_overall and obj.language == 'en']

         

        df = pd.DataFrame.from_records(data)
        #df.to_csv('~/Downloads/test.csv')
        



        #print(df.entities)
        states = sorted(np.append(df.place_state.unique().tolist(),'All'))

        url = ("https://raw.githubusercontent.com/python-visualization/folium/master/examples/data")
        state_geo = f"{url}/us-states.json"

        # We read the file and print it.
        geoJSON_df = gpd.read_file(state_geo)
        geoJSON_df.head()
        df = pd.merge(df, geoJSON_df, left_on='place_state', right_on='name')
        

        return df 
