#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 00:07:16 2019

@author: lukas
"""

from xml.etree import ElementTree
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
            locations.append(elem.attrib['lemma'])
            
