import sys

sys.path.append("../..")


class Ride:
    def __init__(self, name, origin, destination, price):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.price = price
        self.requests = []

    def add_request(self, request):
        self.requests.append(request)
