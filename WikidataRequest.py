import json
import requests
from uri.FedregRequest import FedregRequest

class WikidataRequest():
    
    def getQueriesByAgencyNames(self, nameList):
        """
        Returns two dicts of name:query string Wikidata SPARQL queries for the 'label' and 'altlabel' query types on a given list of agency names.
        
        @param nameList: A list of strings, each representing an agency name.
        
        """
        
        queryStart = '''
        SELECT ?wikidataURI 
        WHERE 
        {
          ?wikidataURI rdfs:label "'''
          
        queryStartAlt = '''
        SELECT ?wikidataURI  
        WHERE 
        {
          ?wikidataURI  skos:altLabel "'''
        
        queryEnd = '''"@en .
        }
        '''
            
        namesQueriesDict = {}
        namesAltQueriesDict = {}
        for name in nameList:
            namesQueriesDict[name] = queryStart + name + queryEnd
            namesAltQueriesDict[name] = queryStartAlt + name + queryEnd
        
        return namesQueriesDict, namesAltQueriesDict 

    def getJsonList(self, url, namesQueriesDict):
        """
        Returns a dictionary of agency name:JSON key-value pairs from the Wikidata API. Each JSON value contains agency data returned by Wikidata.
        The value will be None if the search for the agency name failed.
        
        @param url: A string url for the Wikidata SPARQL endpoint. Example: https://query.wikidata.org/sparql
        @param namesQueriesDict: A dictionary of agency name and SPARQL query mappings.
        
        """
        jsonDict = {}
        numFailed = 0
        
        for idx, name in enumerate(namesQueriesDict.keys()):
            try: 
                agencyData = requests.get(url, params = {'format': 'json', 'query': namesQueriesDict[name]}).json()
                jsonDict[name] = self.getUriFromJson(agencyData)
            except ValueError:
                jsonDict[name] = None
            
            print("Progress:", idx, "/", len(namesQueriesDict))
        
        return jsonDict
    
    def getUriFromJson(self, json):
        """
        Returns a URI if available, parsed from the JSON returned for an agency from the Wikidata API.
        If the parsing strategy fails, returns None.
        
        @param json: A JSON object retrieved from Wikidata for a given agency.
        
        """
        try:
            uri = json["results"]["bindings"][0]["wikidataURI"]["value"]
            print(uri)
            return uri
            
        except KeyError:
            return None
        except IndexError:
            return None
