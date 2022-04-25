import json, schedule, datetime, time
from requests import Session
from datetime import timedelta

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
        parameters = {'latlng': crdnt_str, 'token': self.token}
        url = self.api_url + '/v2/map/bounds'
        r = self.query_api(url, parameters)
        if r.status_code == 200:
            data = r.json()['data']
            return data

    def close_session(self):
        self.session.close()

class Scheduler:
    def __init__(self, sample_rate, duration):
        self.time_delta = 1/sample_rate
        self.duration = duration

    def start(self, job):
        schedule.every(self.time_delta).minutes.do(job)
        start_time = datetime.datetime.now()
        end_time = start_time + timedelta(minutes=self.duration)
        while datetime.datetime.now() < end_time:
            schedule.run_pending()
            time.sleep(1)