import json, schedule, datetime, time, sys
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

    def start(self, job, api_parser):
        schedule.every(self.time_delta).minutes.do(job, api_parser)
        start_time = datetime.datetime.now()
        end_time = start_time + timedelta(minutes=self.duration)
        while datetime.datetime.now() < end_time:
            schedule.run_pending()
            time.sleep(1)

class StationMap:
    def __init__(self, crdnt_str):
        self.stations = {}
        self.cumulative_pm25 = 0
        self.average_pm25 = 0
        self.crdnts = crdnt_str
        self.samples_taken = 0

    def update_stations(self, parser):
        data = parser.get_stations(self.crdnts)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item in data:
            self.stations[item['uid']] = item['aqi']
            if item['aqi'].isnumeric():
                self.cumulative_pm25 += int(item['aqi'])
                self.samples_taken += 1
            print(f"{current_time} Station: {item['station']['name']} pm25: {item['aqi']}")
 
        self.average_pm25 = self.cumulative_pm25/self.samples_taken
        print("\n")

""" Converts list of coordinates into string for use with AQICN api """
def get_coordinate_str(crdnt_list):
    crdnt_str = ''
    num_crdtns = 4
    for i in range(1, num_crdtns+1):
        crdnt_str += sys.argv[i]
        if i < num_crdtns:
            crdnt_str += ","
    return crdnt_str
            
def main():
    if (len(sys.argv) != 7):
        raise ValueError("Require exactly 7 arguments: file_name, lat1, lng1, lat2, lng2, rate, duration")
    elif (int(sys.argv[5]) <= 0 or int(sys.argv[6]) <= 0):
        raise ValueError("Sampling Rate and Duration must both be > 0")
    elif(sys.argv[1] == sys.argv[3] or sys.argv[2] == sys.argv[4]):
        raise ValueError("lat1 must not equal lat2, lng1 must not equal lng2")
    
    latlng = get_coordinate_str(sys.argv[1:5])
    stns = StationMap(latlng)
    sched = Scheduler(6, 1)
    parser = AQICN_Parser(TOKEN)
    sched.start(stns.update_stations, parser)
    print(f"Average Measured pm25: {round(stns.average_pm25, 2)}")
    parser.close_session()

if __name__ == '__main__':
    main()