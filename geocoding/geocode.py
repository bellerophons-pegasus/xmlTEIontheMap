#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 00:07:16 2019

@author: lukas
"""

###################### Scope of this script
###################### 
#
# - In this script we try to convert the NEs (Named Entities), which are not Persons, into Places with geographic coordinates
# - These Coordinates are then displayed on a map and so on...
# - This is only a proof of concept! much to be done
#
###################### Methods
######################
#
# - The data was handled with the module ElementTree
# - The geographic data was derived with arcgis
#
###################### Problems
###################### 
#
# 1- The biggest problem were city/country/... names made of several words. 
#    All these words are single NEs and it is rather difficult to combine them in the right way.
# 2- Arcgis gives results for another city elsewhere in the world
# 3- Some citynames have changed since the early 20th century -> only a very limited number of cases...should be fine
# 
###################### Possible Solution
######################
#
# - For 1 and 2 a possible solution could be to create a list with all cities in the mediterranean region.
#   eg. Athen, Greece
#       Rome, Italy
#       Las Palmas de Gran Canaria, Spain
#       ...
#   All found NEs could be checked with this list and so names made of several words and
#   misleading arcgis results can be prevented
# - In this script the corrections are made by hand 
#
######################
###################### 







from xml.etree import ElementTree
from arcgis.gis import GIS
from arcgis.geocoding import geocode


dev_gis = GIS()


######################
###################### Two functions (city and country): - Replacing the element with the <place... element
###################### - Adding the subelement location and geo with the coordinates
######################


def wrap_elem_city(parent,elem,lat,lng):
    parent_index = list(parent).index(elem)
    parent.remove(elem)
    new_elem = ElementTree.Element('place', attrib = {'type': 'city'})
    parent.insert(parent_index,new_elem)
    new_elem.append(elem)

    location = ElementTree.SubElement(new_elem, 'location')
    geo = ElementTree.SubElement(location, 'geo').text = str(lat)+' '+str(lng)
    
def wrap_elem_country(parent,elem,lat,lng):
    parent_index = list(parent).index(elem)
    parent.remove(elem)
    new_elem = ElementTree.Element('place', attrib = {'type': 'country'})
    parent.insert(parent_index,new_elem)
    new_elem.append(elem)

    location = ElementTree.SubElement(new_elem, 'location')
    geo = ElementTree.SubElement(location, 'geo').text = str(lat)+' '+str(lng)


######################
###################### Parsing the xml-file
######################

tree = ElementTree.parse("data_introduction.xml")
root = tree.getroot()

ElementTree.register_namespace('','http://www.tei-c.org/ns/1.0')


######################
###################### Build a map of parent dependencies for each element
######################

parent_map = dict((c,p) for p in tree.getiterator() for c in p)

######################
###################### Checking all NEs that are Persons - not to mix up with places!
######################

name_list = []
for elem in tree.iter(tag = '{http://www.tei-c.org/ns/1.0}persName'):
    for child in elem.getchildren():
        if child.tag == '{http://www.tei-c.org/ns/1.0}w':
            name_list.append(child.attrib['lemma'])
    

######################
###################### Some INTs to track the progress of the script
######################
i = 0.0
j = len(list(tree.iter(tag="{http://www.tei-c.org/ns/1.0}w")))
cities = 0 
countries = 0

for elem in tree.iter(tag="{http://www.tei-c.org/ns/1.0}w"):
    print(100*i/j)
    i = i+1
    
    if elem.attrib['type']=='NE':
        entry = elem.attrib['lemma']
        if entry in name_list:
            continue
        if len(entry) > 2 :

            ######################
            ###################### Simple fixes. Citynames which changed (eg Bôre -> Annaba)
            ###################### Or Names made of several Words which are all NEs (eg Las Palmas)
            ###################### Or Cities that are treated as Countries (eg Tunis vs Tunis City)
            ###################### 
            
            if entry == "Bône":
                entry = "Annaba"
                
            if entry == "Lalla-Marnia":
                entry = "Maghnia"            
            
            if entry == "Tunis":
                entry = "Tunis City"            
            
            if entry == "Saïd":
                entry = "Port Said"             
            
            if entry == "Orotava":
                entry = "Puerto Orotava" 
            
            if entry == "Palmas":
                entry = "Las Palmas"             
            
            if entry == "Kreta":
                entry = "Kreta Island"             
            
            
            
            ######################
            ###################### Getting the geoinformation via arcgis
            ###################### 
            
            while True:
                try:
                    geocode_result = geocode(address=entry, as_featureset=True)
                except:
                    print('Error in geocode')
                    continue
                break
            
            
            ######################
            ###################### Checking if the NE is a country, city or similar
            ######################            
            try:
                if geocode_result.features[0].attributes['Type'] == 'Country':
                                        
                    parent = parent_map[elem]
                    
                    lat = round(geocode_result.features[0].geometry.y,5) #the country's latitude and longitude
                    lng = round(geocode_result.features[0].geometry.x,5)
                    
                    if lng < -35.5 or lat > 47.0 or lat < 26.9 or lng >61.5: #for now only the mediterranean area
                        continue
                    
                    wrap_elem_country(parent,elem,lat,lng)  # replacing the element with <place...
                    
                    # just for monitoring
                    countries += 1 
                    print('Countires: '+str(countries))
                    
                
                if geocode_result.features[0].attributes['Type'] == 'City' or geocode_result.features[0].attributes['Type'] == 'County' or geocode_result.features[0].attributes['Type'] == 'Island':
                    
                    bad_words=['Elbe','Wagner','Schwarzwald','Baden','Karl','Rhein'] #some fixes for confusing results
                    if elem.attrib['lemma'] in bad_words:
                        continue

                    parent = parent_map[elem]
                    
                    lat = round(geocode_result.features[0].geometry.y,5) #the city's latitude and longitude
                    lng = round(geocode_result.features[0].geometry.x,5)
                    
                    if lng < -35.5 or lat > 47.0 or lat < 26.9 or lng >61.5: #for now only the mediterranean area
                        continue
                                    
                    wrap_elem_city(parent,elem,lat,lng) # replacing the element with <place...
                    
                    # just for monitoring
                    cities +=1
                    print('Cities: '+str(cities))
            except:
                continue
                
                
                


######################
###################### Writing the new tree in an output file
######################            

tree.write('MM_places_short2.xml',encoding = 'utf8')

