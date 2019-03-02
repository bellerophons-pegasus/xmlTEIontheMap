# xmlTEIontheMap
This is a hack created for the [ACDH virtual Open Data hackathon series 2019](https://github.com/acdh-oeaw/ACDHhackathonODD). It is a hacky quick and dirty proof of concept.

## The idea
1. Take an annotated TEI encoded XML file where potential places are already marked as named entities in this way:
```xml
<w lemma="Athen" type="NE" xml:id="MM_d1e2915">Athen</w>
```

2. For each named entity try to determine if it is a place, then do some basic disambiguation and find coordinates for it.

3. Add the newly found coordinate information into the TEI encoded XML file according to [TEI specifications](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ND.html#NDGEOG); e.g.:
```xml
<place type="city">
  <w lemma="Athen" type="NE" xml:id="MM_d1e2915">Athen</w>
  <location>
  <geo>37.9838 23.7275</geo>
 </location>
</place>
```

4. Use the new file for display on a webpage. On left side: pretty formatted text (with [CETEIcean](https://github.com/TEIC/CETEIcean)). On right side: a leaflet map with markers of all places encoded in the currently visible snippet.

## Further work
* See initail comments in geocoding/geocode.py
* Clean up pagination display (not properly hidden elements)
* Add clustering of markers on map
* Link markers to their respective mention in the text and highlight it there 

### Ideas for more
* Allow correction of coordinates via map display

## Things used
* Python dependencies:
 * xml.etree
 * arcgis.gis
 * arcgis.geocoding
* [CETEIcean](https://github.com/TEIC/CETEIcean)
* [Pagination for CETEIcean](https://github.com/raffazizzi/ceteicean-pagination)

Other useful resources:
* http://tei.oucs.ox.ac.uk/Talks/2015-02-warsaw/
