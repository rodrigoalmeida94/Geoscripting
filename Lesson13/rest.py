# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 10:12:02 2017

@author: rodrigo & ping
"""

from twython import Twython
import json
import datetime
from geojson import Feature, Point, FeatureCollection
import geojson
import folium
import requests

# codes to access twitter API. 
APP_KEY = 'pNkSd6deMzM0qqsINoF34Fhhi'
APP_SECRET = 	''
OAUTH_TOKEN = '55011261-S1KE8sVU6jY16yw7SWNGhsCxxKVOfd2k2Kl9yJt9q'
OAUTH_TOKEN_SECRET = 	''

# initiating Twython object 
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# search tweets 25 km of the center of Lisbon
search_results = twitter.search(q= '#lisbon',lang='en', geocode = '38.707587,-9.136502,25km', count = 1000)

features = []
# parsing out 
for tweet in search_results["statuses"]:
    data = {}
    if tweet['coordinates'] != None:
        coordinates = tweet['coordinates']
        data['tweettext'] = tweet['text']
        data['created'] = tweet['created_at']
        data['likes'] = tweet['favorite_count']
        if tweet['place'] != None:
            data['full_place_name'] = tweet['place']['full_name']
            data['place_type'] =  tweet['place']['place_type']
        point = Point((coordinates['coordinates'][0], coordinates['coordinates'][1]))
        # uses a post request to analyse the sentiment of the tweet
        res = requests.post('http://text-processing.com/api/sentiment/', data = {'text':data['tweettext']})
        data['emotion'] = res.json()['label']
        feat = Feature(geometry = point, properties = data)
        features += [feat]

collection = FeatureCollection(features)

# Creates a geojson files
fl = open('tweets.geojson', 'w') 
geojson.dump(collection, fl)
fl.close()

# uses folium to plot the points in the map
lis_map = folium.Map(location=[38.707587,-9.136502],
                   tiles='openstreetmap', zoom_start=12)
f = collection['features']
for feat in f:
    if feat['properties']['emotion'] == 'neg':
        c = 'red'
    elif feat['properties']['emotion'] == 'neutral':
        c = 'blue'
    else:
        c = 'green'
    folium.Marker(list(feat['geometry']['coordinates'])[::-1], popup = feat['properties']['tweettext'], icon = folium.Icon(color=c,icon='info-sign') ).add_to(lis_map)
lis_map
lis_map.save('lis_map.html')
