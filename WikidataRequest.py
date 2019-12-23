"""
The WikidataRequest class contains all methods necessary to extract federal agency URI information from Wikidata.
"""

import json
import requests
import time
from collections import defaultdict

from FedregRequest import FedregRequest

class WikidataRequest():
    
    def getQueriesByAgencyNames(self, nameList):
        """
        Returns two dicts of name:query string Wikidata SPARQL queries for the 'label' and 'altlabel' query types on a given list of agency names.
        
        @param nameList: A list of strings, each representing an agency name.
        """
        
        queryStart = '''
        SELECT ?wikidataURI 
        WHERE {
        {
          ?wikidataURI rdfs:label "'''
        queryMid = '''" @en .
        }
        UNION
        {
          ?wikidataURI  skos:altLabel "'''
        queryEnd = '''"@en .}
        }
        '''
            
        namesQueriesDict = {}
        for name in nameList:
            namesQueriesDict[name] = queryStart + name + queryMid + name + queryEnd
        
        return namesQueriesDict


    def getJsonList(self, url, namesQueriesDict, fedRegAbstracts):
        """
        Returns a dictionary of agency name:JSON key-value pairs from the Wikidata API. Each JSON value contains agency data returned by Wikidata.
        Returns also a dictionary of agency name:string-value pairs for valid matches, where the string is the Federal Register description.
        
        The value will be None if the search for the agency name failed.
        
        @param url: A string url for the Wikidata SPARQL endpoint. Example: https://query.wikidata.org/sparql
        @param namesQueriesDict: A dictionary of agency name and SPARQL query mappings.
        
        """
        nameToUriMap = {}
        uriToAbstractsMap = {}
        numFailed = 0
        
        for idx, name in enumerate(namesQueriesDict.keys()):
            try: 
                agencyData = requests.get(url, params = {'format': 'json', 'query': namesQueriesDict[name]}).json()
                uriList = self.getUriFromJson(agencyData)
                nameToUriMap[name] = uriList
                for uri in uriList:
                    uriToAbstractsMap[uri] = fedRegAbstracts[name]
            except ValueError:
                nameToUriMap[name] = None
                print("Wikidata query attempt raised an exception.")
            delay = 1.0
            print("Querying Wikidata:", idx+1, "/", len(namesQueriesDict))
            time.sleep(delay)
            # if idx > 20:
            #     break
        
        return nameToUriMap, uriToAbstractsMap
    
    def getUriFromJson(self, json):
        """
        Returns a list of URIs if available, parsed from the JSON returned for an agency from the Wikidata API.
        If the parsing strategy fails, returns None.
        
        @param json: A JSON object retrieved from Wikidata for a given agency.
        
        """
        try:
            uriList = []
            for i in json["results"]["bindings"]:
                uriList.append(i["wikidataURI"]["value"])
            return uriList
            
        except KeyError:
            return None
        except IndexError:
            return None


# w = WikidataRequest()
# nameList = ['Federal Railroad Administration', 'Environmental Protection Agency', 'ACTION']
# queries = w.getQueriesByAgencyNames(nameList)
# print(queries)
# print(requests.get('https://query.wikidata.org/sparql', params = {'format': 'json', 'query': queries[nameList[0]]}).json())
# print("JSON LIST")
# print(w.getJsonList('https://query.wikidata.org/sparql', queries, {'Federal Railroad Administration': 'fra', 'Environmental Protection Agency': 'epa', 'ACTION': 'act'}))