#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 12:27:58 2018

@author: dorondusheiko
"""

import requests
import json
import settings

# Cape Town cityID is 64 - obtained from manual API query using City API
# Search API returns maximum 20 results per request. 1000 reuqests per day allowed
# Manual request suggested there are 3838 restarants in Cape Town  
# This means 3838/20 = 192 requests will be required to obtain all restaurants
# Scrape results will be written to a set of csv files from which they can be further processed
# The following files will be written:
#   1 - RESTAURANT_FILE contains the restaurants in Cape Town
#   2 - CUISINE_FILE contains the list of cuisines available in Cape Town
#   3 - ESTABLISHMENT_FILE contains the types of establishments in Cape Town



def download_cuisines():
# Finding all cuisine types in Cape Town and writing to file
    headers = {"user-key": settings.API_KEY}
    params = {"city_id": settings.city_id}
    response=requests.get("https://developers.zomato.com/api/v2.1/cuisines", 
                          headers=headers, params=params)
    json_data = response.json()
    
    file_path = settings.RAW_FOLDER + settings.CUISINE_JSON__FILE
    with open(file_path, 'w') as outfile:
        json.dump(json_data, outfile)
    
def download_establishment_types():
# Finding all establishment types in Cape Town and writing to file
    headers = {"user-key": settings.API_KEY}
    params = {"city_id": settings.city_id}
    response=requests.get("https://developers.zomato.com/api/v2.1/establishments", 
                          headers=headers, params=params)
    json_data = response.json()
    establishment_ids = []
    establishment_list = json_data["establishments"]

    for est in establishment_list:
        establishment_ids.append(est["establishment"]["id"])
    
    file_path = settings.RAW_FOLDER + settings.ESTABLISHMENT_JSON__FILE
    with open(file_path, 'w') as outfile:
        json.dump(json_data, outfile)
        
    return establishment_ids
    
    
def download_restaurants(establishment_ids):
# Find 100 top rated restaurants of each establishment type in Cape Town and write to file
    
    headers = {"user-key": settings.API_KEY}
    file_path = settings.RAW_FOLDER + settings.RESTAURANT_JSON_FILE
    json_dump = []
    
    for establishment in establishment_ids:
        start = 0
        results_shown = settings.COUNT
        while results_shown != 0:    
            params = {"entity_id": settings.city_id, "entity_type": "city", "start": start, 
                      "count": settings.COUNT, "establishment_type": establishment,"sort":"rating", 
                      "order": settings.ORDERBY}
            response=requests.get("https://developers.zomato.com/api/v2.1/search", 
                              headers=headers, params=params)
            
            json_data = response.json()
            results_shown = int(json_data["results_shown"])
            print(results_shown)
            
            if results_shown == 0:
                break

            # appending each dictionary to a list so that json.load() can process 
            # multiple dictionaries
            json_dump.append(json.dumps(json_data))     
            
            start += settings.COUNT
    
    # each dictionary must exist as a list object for json.load to read it correctly    
    with open(file_path, 'w') as outfile:
        outfile.write("[")
        count = 0
        for item in json_dump:
            outfile.write(item)
            if count < len(json_dump)-1:
                outfile.write(",")
            count += 1
        outfile.write("]")
        
download_cuisines()
establishment_ids = download_establishment_types()
download_restaurants(establishment_ids)

        






