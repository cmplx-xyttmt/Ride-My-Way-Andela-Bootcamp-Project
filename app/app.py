from flask import Flask, jsonify, abort, make_response, request
from ride import Ride

app = Flask(__name__)
rides = [Ride("Isaac", "Kampala", "Wakiso", 10000), Ride("Rose", "Masaka", "Mpigi", 10000)]


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
    pass


@app.route('/ridemyway/api/v1/rides/<int:ride_id>/requests', methods=['POST'])
def request(ride_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
