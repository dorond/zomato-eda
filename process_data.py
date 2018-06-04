#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 14:22:48 2018

@author: dorondusheiko
"""

import pandas as pd
import json
import settings



def create_establishments_csv():

    db = json.load(open(settings.RAW_FOLDER + settings.ESTABLISHMENT_JSON__FILE))
    
    establishment_cols = ['id', 'name']
    establishment_list = db["establishments"]
    
    establishments = [est["establishment"] for est in establishment_list]
    
    df = pd.DataFrame(establishments, columns=establishment_cols)
    output_file = settings.PROCESSED_FOLDER + settings.ESTABLISHMENT_CSV_FILE
    df.to_csv(output_file, encoding='utf-8-sig', index=False)

def create_cuisines_csv():
    
    db = json.load(open(settings.RAW_FOLDER + settings.CUISINE_JSON__FILE))
        
    cuisine_cols = ['cuisine_id', 'cuisine_name']
    cuisine_list = db["cuisines"]
        
    cuisines = [cuisine["cuisine"] for cuisine in cuisine_list]
        
    df = pd.DataFrame(cuisines, columns=cuisine_cols)
    output_file = settings.PROCESSED_FOLDER + settings.CUISINE_CSV_FILE
    df.to_csv(output_file, encoding='utf-8-sig', index=False)




def create_restaurants_csv():
    
    db = json.load(open(settings.RAW_FOLDER + settings.RESTAURANT_JSON_FILE))
    
    restaurant_cols = ["name", 
                       "cuisines",
                       "aggregate_rating", 
                       "rating_text", 
                       "votes",
                       "currency", 
                       "average_cost_for_two", 
                       "price_range",                    
                       "locality", 
                       "city", 
                       "latitude", 
                       "longitude",                                       
                       "has_online_delivery", 
                       "is_delivering_now", 
                       "has_table_booking", 
                       ]
    
    restaurants = [restaurant_group["restaurant"] for count_group in db 
                       for restaurant_group in count_group["restaurants"]] 
    
    for restaurant in restaurants:
        restaurant["locality"] = restaurant["location"]["locality"]
        restaurant["city"] = restaurant["location"]["city"]
        restaurant["latitude"] = restaurant["location"]["latitude"]
        restaurant["longitude"] = restaurant["location"]["longitude"]
        restaurant["zipcode"] = restaurant["location"]["zipcode"]
        restaurant["aggregate_rating"] = restaurant["user_rating"]["aggregate_rating"]
        restaurant["votes"] = restaurant["user_rating"]["votes"]
        restaurant["rating_text"] = restaurant["user_rating"]["rating_text"]
        
    
    df = pd.DataFrame(restaurants, columns=restaurant_cols)
    output_file = settings.PROCESSED_FOLDER + settings.RESTAURANT_CSV_FILE
    df.to_csv(output_file, encoding='utf-8-sig', index=False)

create_establishments_csv()
create_cuisines_csv()
create_restaurants_csv()