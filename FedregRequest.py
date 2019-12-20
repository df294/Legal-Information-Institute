import json
import requests
import pprint

class FedregRequest():
    
    def __init__(self):
        return

    def getJsonList(self, url):
        """
        Returns a list of JSON objects from the Federal Register API. Each JSON includes info for a specific agency.
        @param url: A string url for the Federal Register API. Example: http://www.federalregister.gov/api/v1/agencies
        
        """
        
        data = requests.get(url)
        return data.json()
    
    def getNamesUrls(self, jsonList):
        """
        Returns a dict of name:url key value pairs for agencies in the Federal Register.
        @param jsonList: A list of JSON objects produced by a request from the Federal Register API.
        
        """
        nameUrlMap = {}
        for agency in jsonList:
            if 'name' in agency.keys() and 'url' in agency.keys():
                nameUrlMap[agency['name']] = agency['url']
        
        return nameUrlMap

    def getDescriptions(self, jsonList):
        """
        Returns a dict of name:description key value pairs for agencies in the Federal Register.
        @param jsonList: A list of JSON objects produced by a request from the Federal Register API.
        
        """
        descriptionMap = {}
        for agency in jsonList:
            if 'description' in agency.keys() and 'name' in agency.keys():
                descriptionMap[agency['name']] = agency['description']
        
        return descriptionMap

# f = FedregRequest()
# jsonList = f.getJsonList('http://www.federalregister.gov/api/v1/agencies')
# pprint.pprint(f.getDescriptions(jsonList))

