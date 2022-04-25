import unittest

from main import TOKEN, AQICN_Parser



class TestAQICN_Parser(unittest.TestCase):
    def setUp(self):
        self.parser = AQICN_Parser(TOKEN)
    
    def test_query_api_returns_ok(self):
        crdnts = '39.379436,116.091230,40.235643,116.784382'
        parameters = {'latlng': crdnts, 'token': self.parser.token}
        url = 'https://api.waqi.info/v2/map/bounds'
        r = self.parser.query_api(url, parameters)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()