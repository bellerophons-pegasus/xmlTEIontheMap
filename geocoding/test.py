#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 00:07:16 2019

@author: lukas
"""

import geocoder 
from xml.etree import ElementTree



from arcgis.gis import GIS
from arcgis.geocoding import geocode, reverse_geocode
from arcgis.geometry import Point

dev_gis = GIS()


geocode_result = geocode(address="Berlin", as_featureset=True)
print(geocode_result.features[0].geometry.x)
print(geocode_result.features[0].geometry.y)





tree = ElementTree.parse("test.xml")
root = tree.getroot()
#print(root)
#name_tree = ElementTree.parse("names.xml")

name_list = []
locations = []

for elem in tree.iter(tag = '{http://www.tei-c.org/ns/1.0}persName'):
    for child in elem.getchildren():
        if child.tag == '{http://www.tei-c.org/ns/1.0}w':
            name_list.append(child.attrib['lemma'])
    


for elem in tree.iter(tag="{http://www.tei-c.org/ns/1.0}w"):
    
    if elem.attrib['type']=='NE':
        entry = elem.attrib['lemma']
        if entry in name_list:
            continue
        if len(entry) > 2 :
            locations.append([])
            locations[-1].append(elem.attrib['lemma'])
            geocode_result = geocode(address=entry, as_featureset=True)
            locations[-1].append(geocode_result.features[0].geometry.x)
            locations[-1].append(geocode_result.features[0].geometry.y)
            print(locations[-1])
            

