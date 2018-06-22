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
        self.ride_offers = [
            ride.Ride("Isaac", "Mpererwe", "Kamwokya", 10000),
            ride.Ride("Rose", "Kampala Road", "Mpererwe", 15000),
            ride.Ride("Catherine", "Ibanda", "Kampala", 50000),
            ride.Ride("Anita", "Entebbe", "Kampala", 20000)
        ]
        rides.extend(self.ride_offers)

    def test_get_rides(self):
        """Tests whether the ride offers inserted into rides exist in what the api endpoint returns"""
        response = self.client.get("ridemyway/api/v1/rides")
        self.assertEqual(response.status_code, 200)

        # Expect a list with the values above as dictionaries
        data_from_response = json.loads(str(response.data.decode()))['rides']

        self.assertEqual(len(rides), len(data_from_response))
        for i in range(0, len(data_from_response)):
            self.assertEqual(rides[i].__dict__, data_from_response[i])

    def test_get_ride(self):
        """Tests whether user can retrieve a specific ride with a ride_id"""
        for i in range(len(rides)):
            response = self.client.get("ridemyway/api/v1/rides/{}".format(i + 1))
            self.assertEqual(response.status_code, 200)
            data = json.loads(str(response.data.decode()))['ride']
            self.assertEqual(data, rides[i].__dict__)

    def test_create_ride(self):
        """Tests whether the ride created by client exists in the rides list"""
