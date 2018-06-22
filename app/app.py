from flask import Flask, jsonify, abort, request
from app.ride import Ride
from app.request import RideRequest
import sys

sys.path.append("..")
app = Flask(__name__)
rides = []


@app.route('/ridemyway/api/v1/rides', methods=['GET'])
def get_rides():
    rides_as_dicts = [ride.__dict__ for ride in rides]
    return jsonify({'rides': rides_as_dicts})


@app.route('/ridemyway/api/v1/rides/<int:ride_id>', methods=['GET'])
def get_ride(ride_id):
    if ride_id > len(rides):
        abort(404)
    ride = rides[ride_id - 1]
    return jsonify({'ride': ride.__dict__})


@app.route('/ridemyway/api/v1/rides', methods=['POST'])
def create_ride():
    if not request.is_json:
        abort(400)
    json_request = request.get_json()
    if 'name' not in json_request or 'origin' not in json_request or 'destination' not in json_request:
        abort(400)  # Bad request

    ride = Ride(json_request['name'], json_request['origin'], json_request['destination'], json_request.get('price', 0))
    rides.append(ride)
    return jsonify({'ride': ride.__dict__}), 201


@app.route('/ridemyway/api/v1/rides/<int:ride_id>/requests', methods=['POST'])
def ride_request(ride_id):
    if not request.is_json:
        abort(400)
    json_request = request.get_json()
    if 'name' not in json_request:
        abort(400)
    ride_request = RideRequest(json_request['name'])



if __name__ == '__main__':
    app.run(debug=True)
