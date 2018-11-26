from unittest import TestCase
from app import app

class FlaskTests(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_prediction_route(self):
        result = self.client.get("/silas/AAPL")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"date"' and b'"0"' and b'"1"', result.data)
    
    def test_historic_route(self):
        result = self.client.get("/silas/AAPL/historics")
        self.assertEqual(result.status_code, 200)
        print(result.data)
        self.assertIn(b'"open"' and b'"high"' and b'"low"' and b'"close"', result.data)