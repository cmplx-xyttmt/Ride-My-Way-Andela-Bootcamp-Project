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

    def __eq__(self, other):
        return self.name == other.name and \
            self.origin == other.origin and \
            self.destination == other.destination and \
            self.price == other.price and \
            self.requests == other.requests
