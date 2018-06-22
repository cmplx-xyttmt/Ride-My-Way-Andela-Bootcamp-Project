import unittest
import json
from app import app, rides
import ride, request


class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
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
        new_ride_offer = ride.Ride('Isaac', "Kampala", "Arua", 10000)
        response = self.client.post("ridemyway/api/v1/rides",
                                    content_type="application/json",
                                    data=json.dumps(new_ride_offer.__dict__))
        self.assertEqual(response.status_code, 201)  # Ensure status code is the correct one.
        data = json.loads(str(response.data.decode()))
        self.assertEqual(data['ride'], new_ride_offer.__dict__)  # Ensure data returned is equal to data sent.
        self.assertIn(new_ride_offer, rides)  # Ensure ride offer is in list of rides.

    def test_ride_request(self):
        """Tests whether a ride request has been successfully created"""
        new_ride_request = request.RideRequest('Rose')
        response = self.client.post("ridemyway/api/v1/rides/{}/requests".format(1),
                                    content_type="application/json",
                                    data=json.dumps(new_ride_request.__dict__))
        self.assertEqual(response.status_code, 200)  # Ensure status code is correct
        data = json.loads(str(response.data.decode()))
        self.assertEqual(data['request'], new_ride_request.__dict__)  # Ensure data sent is equal to data returned
        # Ensure that the ride request is in list of ride requests
        self.assertEqual(rides[0].request_exists(new_ride_request), True)


if __name__ == '__main__':
    unittest.main()
