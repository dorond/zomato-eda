#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 10:52:14 2018

@author: dorondusheiko
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get('https://en.wikipedia.org/wiki/List_of_Cape_Town_suburbs')
content = response.content
parser = BeautifulSoup(content, 'html.parser')

#Finding all regions in th Wiki page - these have the .mw-headline class
regions_list = [region.text for region in parser.select(".mw-headline")]
suburbs_by_region = {}                    

# The .wikitable class is assigned to each table of suburbs per region    
regions = parser.select(".wikitable")  

count = 0
for region in regions:
    # Finding each suburb while skipping columns with postal codes
    # Some fields have additional info in (), so splitting on those and removing
    suburbs = [suburb.text.split('(')[0] for suburb in region.select("td")[::3]]
    
    for suburb in suburbs:
        suburbs_by_region[suburb] = regions_list[count]
    count += 1  
 
# We need to manually add entries which are known suburbs of the greater Cape Town area

              
df = pd.DataFrame(list(suburbs_by_region.items()), columns=['locality', 'region'])
df.to_csv("Processed/cape-town-suburbs.csv", encoding='utf-8-sig', index=False)