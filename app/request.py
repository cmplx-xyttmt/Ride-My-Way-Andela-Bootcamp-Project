class RideRequest:
    def __init__(self, name):
        self.name = name
        self.accepted = False
        self.rejected = False

    def accept_request(self):
        if self.rejected:
            return False
        self.accepted = True
        return True

    def reject_request(self):
        if self.accepted:
            return False
        self.rejected = True
        return True

    def __eq__(self, other):
        return self.name == other.name and self.accepted == other.accepted and self.rejected == other.rejected
