class Country:
    def __init__(self):
        self.count = 0
        self.num_attendees = None
        self.attendees = list()
        self.name = None
        self.start_date = None

    def add_attendee(self, partner):
        self.attendees.append(partner.email)

    def set_payload(self):
        payload = dict()
        payload["attendeeCount"] = len(self.attendees)
        payload["attendees"] = self.attendees
        payload["name"] = self.name
        payload["startDate"] = self.start_date
        return payload
