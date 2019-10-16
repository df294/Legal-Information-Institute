'''
Work in progress for agency information matching.
Currently running this file will print to a .txt file Federal Register agency urls with matching Wikidata URIs.

Created on Sep 25, 2019

@author: David
'''

from uri.uriMatching import uriMatching

uriMatching = uriMatching()
frNameUrlMap, wdFrMatchingUriDict = uriMatching.matchWdFrByName()

f = open("frAndWikiDataMatches.txt","w+")
for key in frNameUrlMap.keys():
    if wdFrMatchingUriDict[key] == None:
        match = frNameUrlMap[key] + " : None"
    else:  
        match = frNameUrlMap[key] + " : " + wdFrMatchingUriDict[key]
    f.write(match + "\n")
    print(match)
f.close()