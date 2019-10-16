from uri.FedregRequest import FedregRequest
from uri.WikidataRequest import WikidataRequest

class uriMatching():
    
    def __init__(self):
        return
    
    def matchWdFrByName(self):
        """
        Returns two dict objects. 
        The first consists of name:url pairs of agency names mapped against their respective urls retrieved by the Federal Register API.
        The second consists of name:uri pairs of agency names retrieved by the Federal Register API mapped against URIs retrieved by the Wikidata API. 
        
        """
        
        wdReq = WikidataRequest()
        frReq = FedregRequest()
         
        frJsonList = frReq.getJsonList("http://www.federalregister.gov/api/v1/agencies")
        frNameUrlMap = frReq.getNamesUrls(frJsonList)
        frNames = frNameUrlMap.keys()
         
        queries, altqueries = wdReq.getQueriesByAgencyNames(frNames)
        wdFrMatchingUriDict = wdReq.getJsonList("https://query.wikidata.org/sparql", queries)
        
        return frNameUrlMap, wdFrMatchingUriDict

