class Partner:
    def __init__(self, data):
        self.fname = data["firstName"]
        self.lname = data["lastName"]
        self.email = data["email"]
        self.country = data["country"]
        self.dates = data["availableDates"]