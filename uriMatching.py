"""
The uriMatching class contains the method necessary to combine agency information between the Federal Register and Wikidata.
"""

from FedregRequest import FedregRequest
from WikidataRequest import WikidataRequest

class uriMatching():
    
    def __init__(self):
        return
    
    def matchWdFrByName(self):
        """
        Returns two dict objects. 
        The first consists of name:url pairs of agency names mapped against their respective urls retrieved by the Federal Register API.
        The second consists of name:uri pairs of agency names retrieved by the Federal Register API mapped against URIs retrieved by the Wikidata API. 
        
        """
        print("Getting Federal Register data.")
        wdReq = WikidataRequest()
        frReq = FedregRequest()
        
        frJsonList = frReq.getJsonList("http://www.federalregister.gov/api/v1/agencies")
        frNameUrlMap = frReq.getNamesUrls(frJsonList)
        frNames = frNameUrlMap.keys()
        frAbstracts = frReq.getDescriptions(frJsonList)
        print("Federal Register data extracted.")
        
        queries = wdReq.getQueriesByAgencyNames(frNames)
        nameToUriMap, uriToFedRegAbstracts = wdReq.getJsonList("https://query.wikidata.org/sparql", queries, frAbstracts)
        
        return frNameUrlMap, nameToUriMap, uriToFedRegAbstracts

