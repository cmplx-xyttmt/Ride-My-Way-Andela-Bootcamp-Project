from flask import Flask, jsonify, abort, request, make_response
from app.ride import Ride
from app.ride_request import RideRequest


app = Flask(__name__)
rides = []


@app.route('/ridemyway/api/v1/rides', methods=['GET'])
def get_rides():
    rides_as_dicts = [convert_ride_offer(ride) for ride in rides]
    return jsonify({'rides': rides_as_dicts}), 200


@app.route('/ridemyway/api/v1/rides/<int:ride_id>', methods=['GET'])
def get_ride(ride_id):
    if ride_id > len(rides) or ride_id <= 0:
        abort(404, 'The ride id specified does not exist.')
    ride = rides[ride_id - 1]
    return jsonify({'ride': convert_ride_offer(ride)}), 200


def convert_ride_offer(ride_offer):
    """Converts ride offer to json serializable object
    by first converting requests to dict object"""
    ride_requests_list = [ride_req.__dict__
                          for ride_req in ride_offer.requests]
    ride_offer_dict = ride_offer.__dict__
    ride_offer_dict["requests"] = ride_requests_list
    return ride_offer_dict


@app.route('/ridemyway/api/v1/rides', methods=['POST'])
def create_ride():
    if not request.is_json:
        abort(400, 'Make sure your request contains json data')
    json_request = request.get_json()
    if 'name' not in json_request or \
            'origin' not in json_request or \
            'destination' not in json_request:
        abort(400,
              'Make sure you have specified name, '
              'origin and destination attributes in your json request.')

    ride = Ride(json_request['name'],
                json_request['origin'],
                json_request['destination'],
                json_request.get('price', 0))
    rides.append(ride)
    return jsonify({'ride': convert_ride_offer(ride)}), 201


@app.route('/ridemyway/api/v1/rides/<int:ride_id>/requests', methods=['POST'])
def ride_request(ride_id):
    if not request.is_json:
        abort(400, 'Make sure your request contains json data')
    json_request = request.get_json()
    if 'name' not in json_request:
        abort(400, 'Make sure you have a name attribute in your json request.')
    if ride_id > len(rides) or ride_id <= 0:
        abort(404, 'The ride id specified does not exist.')
    ride_req = RideRequest(json_request['name'])
    rides[ride_id - 1].add_request(ride_req)
    return jsonify({'request': ride_req.__dict__})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": 'Ride Not Found',
                                  "message": error.description}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": 'Bad request.',
                                  'message': error.description}), 400)


if __name__ == '__main__':
    app.run(debug=True)
