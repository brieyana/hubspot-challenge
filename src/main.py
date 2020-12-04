import json
import requests
from datetime import datetime, timedelta
from Partner import Partner
from Country import Country

# urls
get_url = "https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=06d0965907883646610889cabaf7"
post_url = "https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=06d0965907883646610889cabaf7"


def post_data(payload):
    r = requests.post(post_url, data=json.dumps(payload))
    

def get_payload(data):
    payload = dict()
    payload['countries'] = list(map(lambda result: result.set_payload(), data))

    return payload


def sort_data(info):
    country_list = dict()
    countries = list()

    for x in info["partners"]:
        person = Partner(x)

        if person.country not in country_list:
            country_list[person.country] = dict()

        for date in person.dates:
            if date not in country_list[person.country]:
                country_list[person.country][date] = set()
            country_list[person.country][date].add(person)

    for country_name, dates_attendees in country_list.items():
        sorted_dates = sorted(dates_attendees.keys())
        most_attendees = 0
        best_date = datetime(1, 1, 1)

        for i in range(len(sorted_dates[:-1])):
            # turning data into python object
            raw_first_date = sorted_dates[i]
            raw_next_date = sorted_dates[i + 1]
            curr_date = datetime.strptime(sorted_dates[i], '%Y-%m-%d')
            next_date = datetime.strptime(sorted_dates[i + 1], '%Y-%m-%d')

            # checks if dates are consecutive
            if next_date - curr_date != timedelta(1):
                continue

            attendees = dates_attendees[raw_first_date] & dates_attendees[raw_next_date]
            num_attendees = len(attendees)

            if num_attendees > most_attendees or (num_attendees == most_attendees and curr_date < best_date):
                most_attendees = num_attendees
                best_date = curr_date

        attendees = dates_attendees[best_date.strftime('%Y-%m-%d')]

        # creating country object
        country = Country()
        country.name = country_name
        if most_attendees > 0:
            country.num_attendees = most_attendees
        country.start_date = best_date.strftime('%Y-%m-%d')
        for attendee in attendees:
            country.add_attendee(attendee)
        countries.append(country)

    return countries


def get_data():
    r = requests.get(get_url)
    in_json = r.json()
    return in_json


def main():
    data = get_data()
    country_data = sort_data(data)
    payload = get_payload(country_data)
    post_data(payload)


if __name__ == '__main__':
    main()
