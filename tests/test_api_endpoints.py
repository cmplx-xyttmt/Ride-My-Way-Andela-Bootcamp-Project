import unittest
import sys
import json
from app import app, ride, request
from app.app import rides

sys.path.append("../..")


class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()

    def test_get_rides(self):
        """Tests whether the ride offers inserted into rides exist in what the api endpoint returns"""
        ride_offers = [
            ride.Ride("Isaac", "Mpererwe", "Kamwokya", 10000),
            ride.Ride("Rose", "Kampala Road", "Mpererwe", 15000),
            ride.Ride("Catherine", "Ibanda", "Kampala", 50000),
            ride.Ride("Anita", "Entebbe", "Kampala", 20000)
        ]

        rides.extend(ride_offers)
        response = self.client.get("ridemyway/api/v1/rides")
        self.assertEqual(response.status_code, 200)

        # Expect a list with the values above as dictionaries
        data_from_response = json.loads(str(response.data.decode()))['rides']

        self.assertEqual(len(rides), len(data_from_response))
        for i in range(0, len(data_from_response)):
            self.assertEqual(rides[i].__dict__, data_from_response[i])
