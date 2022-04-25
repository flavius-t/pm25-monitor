import unittest

from main import TOKEN, AQICN_Parser, StationMap

class TestAQICN_Parser(unittest.TestCase):
    def setUp(self):
        self.parser = AQICN_Parser(TOKEN)

    def tearDown(self):
        self.parser.close_session()
    
    def test_query_api_returns_ok(self):
        crdnts = '39.379436,116.091230,40.235643,116.784382'
        parameters = {'latlng': crdnts, 'token': self.parser.token}
        url = 'https://api.waqi.info/v2/map/bounds'
        r = self.parser.query_api(url, parameters)
        self.assertEqual(r.status_code, 200)

    def test_get_stations_return_not_null(self):
        crdnts = '39.379436,116.091230,40.235643,116.784382'
        data = self.parser.get_stations(crdnts)
        self.assertIsNotNone(data)

class TestStationMap(unittest.TestCase):
    def setUp(self):
        self.parser = AQICN_Parser(TOKEN)
        self.crdnts = '39.379436,116.091230,40.235643,116.784382'

    def tearDown(self):
        self.parser.close_session()
    
    def test_update_stations_returns_dict(self):
        stns = StationMap(self.crdnts)
        stns.update_stations(self.parser)
        self.assertGreater(len(stns.stations), 0)
    
    def test_update_stations_updates_stats(self):
        stns = StationMap(self.crdnts)
        stns.update_stations(self.parser)
        self.assertGreater(stns.cumulative_pm25, 0)
        self.assertGreater(stns.average_pm25, 0)

if __name__ == '__main__':
    unittest.main()