# xmlTEIontheMap
Idea:
1. Take an annotated TEI encoded XML file where potential places are already marked as named entities as such:
```xml
<w lemma="Athen" type="NE" xml:id="MM_d1e2915">Athen</w>
```

2. For each named entity try to determine if it is a place, then do some basic disambiguation and find coordinates for it.

3. Add coordinate information into the TEX encoded XML file according to [TEI specifications](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ND.html#NDGEOG); e.g.:
```xml
<place type="city">
  <w lemma="Athen" type="NE" xml:id="MM_d1e2915">Athen</w>
  <location>
  <geo>37.9838 23.7275</geo>
 </location>
</place>
```
4. Use the new file for display on a webpage. On left side: pretty formatted text. On right side: map with markers of all places encoded in the currently visible snippet.


Useful resources
* 
* https://github.com/TEIC/CETEIcean
* http://tei.oucs.ox.ac.uk/Talks/2015-02-warsaw/
* Pagination: https://github.com/raffazizzi/ceteicean-pagination and https://gist.github.com/raffazizzi/21ae2bffb387f71feb1efe9feeccba1f
