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

# d = DbpediaRequest()
# uriList = ['http://www.wikidata.org/entity/Q288794',
# 'http://www.wikidata.org/entity/Q4683456',
# 'http://www.wikidata.org/entity/Q4686857',
# 'http://www.wikidata.org/entity/Q4692008',
# 'http://www.wikidata.org/entity/Q69079117',
# 'http://www.wikidata.org/entity/Q4692019',
# 'http://www.wikidata.org/entity/Q4693909',
# 'http://www.wikidata.org/entity/Q2827151',
# 'http://www.wikidata.org/entity/Q4698229',
# 'http://www.wikidata.org/entity/Q2478827',
# 'http://www.wikidata.org/entity/Q635012',
# 'http://www.wikidata.org/entity/Q53043584',
# 'http://www.wikidata.org/entity/Q2910288',
# 'http://www.wikidata.org/entity/Q922454',
# 'http://www.wikidata.org/entity/Q583725',
# 'http://www.wikidata.org/entity/Q5152749',
# 'http://www.wikidata.org/entity/Q5154722',
# 'http://www.wikidata.org/entity/Q1091543',
# 'http://www.wikidata.org/entity/Q612276',
# 'http://www.wikidata.org/entity/Q26732188',
# 'http://www.wikidata.org/entity/Q860051',
# 'http://www.wikidata.org/entity/Q5374270',
# 'http://www.wikidata.org/entity/Q28129963',
# 'http://www.wikidata.org/entity/Q1133499',
# 'http://www.wikidata.org/entity/Q3673184',
# 'http://www.wikidata.org/entity/Q5440177',
# 'http://www.wikidata.org/entity/Q3740862',
# 'http://www.wikidata.org/entity/Q5440253',
# 'http://www.wikidata.org/entity/Q5440273',
# 'http://www.wikidata.org/entity/Q1400052',
# 'http://www.wikidata.org/entity/Q5440472',
# 'http://www.wikidata.org/entity/Q204711',
# 'http://www.wikidata.org/entity/Q5468218',
# 'http://www.wikidata.org/entity/Q55740630',
# 'http://www.wikidata.org/entity/Q60064564',
# 'http://www.wikidata.org/entity/Q1525061',
# 'http://www.wikidata.org/entity/Q61748193',
# 'http://www.wikidata.org/entity/Q5690644',
# 'http://www.wikidata.org/entity/Q6019856',
# 'http://www.wikidata.org/entity/Q6040649',
# 'http://www.wikidata.org/entity/Q6316916',
# 'http://www.wikidata.org/entity/Q30296816',
# 'http://www.wikidata.org/entity/Q1425405',
# 'http://www.wikidata.org/entity/Q861855',
# 'http://www.wikidata.org/entity/Q6971257',
# 'http://www.wikidata.org/entity/Q16932143',
# 'http://www.wikidata.org/entity/Q1967022',
# 'http://www.wikidata.org/entity/Q1967116',
# 'http://www.wikidata.org/entity/Q1967350',
# 'http://www.wikidata.org/entity/Q11683311',
# 'http://www.wikidata.org/entity/Q176691',
# 'http://www.wikidata.org/entity/Q6974287',
# 'http://www.wikidata.org/entity/Q6978856',
# 'http://www.wikidata.org/entity/Q7075792',
# 'http://www.wikidata.org/entity/Q900525',
# 'http://www.wikidata.org/entity/Q458620',
# 'http://www.wikidata.org/entity/Q7164754',
# 'http://www.wikidata.org/entity/Q7197274',
# 'http://www.wikidata.org/entity/Q43895490',
# 'http://www.wikidata.org/entity/Q7315144',
# 'http://www.wikidata.org/entity/Q7380517',
# 'http://www.wikidata.org/entity/Q7444918',
# 'http://www.wikidata.org/entity/Q7569497',
# 'http://www.wikidata.org/entity/Q7692553',
# 'http://www.wikidata.org/entity/Q368804',
# 'http://www.wikidata.org/entity/Q943091',
# 'http://www.wikidata.org/entity/Q1141049',
# 'http://www.wikidata.org/entity/Q2495435',
# ]
# data = d.getJsonAbstractsFromWikidataURIs('https://dbpedia.org/sparql', uriList)
# abstracts = d.getAbstractsFromDict(data)
# print(abstracts)