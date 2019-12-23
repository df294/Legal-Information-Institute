"""
The dbpediaRequest class contains all methods to query and process federal agency results from Dbpedia.
"""

import json
import requests
from collections import defaultdict

class DbpediaRequest():

    def getJsonAbstractsFromWikidataURIs(self, endpointUrl, uriList):
        """
        Given a list of URIs, returns a dict of URI::Json results of Dbpedia SPARQL queries for abstracts linked to those URIs.
        As of 12/15/2019, Dbpedia cannot process more than 100 queries per second or queries returning 10000 or more lines.
        This function therefore does not combine all URIs into one UNION query but iteratively sends queries for each URI.

        @param endpointUrl: A string url for the Dbpedia SPARQL endpoint. Example: https://dbpedia.org/sparql
        @param uriList: An array of strings of URI identifiers for Wikidata. 
                        Example: ['http://www.wikidata.org/entity/Q288794', 'http://www.wikidata.org/entity/Q4683456']
        """

        if len(uriList) == 0:
            return None
        
        data = defaultdict(str)
        count = 1
        for uri in uriList:
            query = """
            SELECT ?dbpediaURI ?abstract WHERE {
            ?dbpediaURI <http://www.w3.org/2002/07/owl#sameAs> <""" + uri + """> .
            ?dbpediaURI <http://dbpedia.org/ontology/abstract> ?abstract .
            FILTER (lang(?abstract) = 'en').
            }
            """
            print("Querying Dbpedia: ", count, "/", len(uriList))
            count += 1
            data[uri] = requests.get(endpointUrl, params = {'format': 'json', 'query': query}).json()
        
        # print(requests.get(endpointUrl))
        
        return data

    def getAbstractsFromDict(self, data):
        """
        Given a dict of JSON results of a Dbpedia SPARQL query for abstracts, returns a URI::abstract string dict.
        """

        abstracts = defaultdict(str)
        for key in data:
            try:
                for i in data[key]["results"]["bindings"]:
                    try:
                        abstracts[key] = i["abstract"]["value"]
                    except KeyError:
                        continue
                    except IndexError:
                        continue
            except KeyError:
                return abstracts
            except IndexError:
                return abstracts
        return abstracts