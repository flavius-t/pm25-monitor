import json
from requests import Session

f = open('keys.json')
keys = json.load(f)
TOKEN = keys['API_TOKEN']
f.close()

class AQICN_Parser:
    def __init__(self, token):
        self.api_url = 'https://api.waqi.info'
        self.session = Session()
        self.token = token

    """ run query with parameters at API endpoint url, returns ok 200 if API query ok"""
    def query_api(self, url, parameters):
        return self.session.get(url, params=parameters)
    
    """ returns a JSON object containing station information for all
    stations with the coordinate string defined by crdnt_str """
    def get_stations(self, crdnt_str):
        pass
