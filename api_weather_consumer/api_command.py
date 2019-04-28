import argparse
from datetime import datetime
import sys

import requests


API_URL = 'https://www.metaweather.com/api/location'


def get_city_woeid(city):
    req_url = f'{API_URL}/location/search?query={city}'
    response = requests.get(req_url)
    if not response.status_code == 200:
        print(f'The server return an error {response.status_code}')
        sys.exit(2)

    data = response.json()
    if not data:
        print(f'No city {city} could be found.')
        sys.exit(2)

    if len(data) > 1:
        print(f'{len(data)} cities were find, be more specific !')
        sys.exit(2)

    return response.json()[0]['woeid']


def get_city_weather(woeid, city):
    today = datetime.now().strftime('%Y/%m/%d')
    req_url = f'{API_URL}/{woeid}/{today}'
    response = requests.get(req_url)
    if not response.status_code == 200:
        print(f'The server return an error {response.status_code}')
        sys.exit(2)

    rain_state = ('hr', 'lr', 's')
    data = response.json()
    for prediction in data:
        if prediction['weather_state_abbr'] in rain_state:
            return f"It's going to rain today in {city} with a predictability of {prediction['predictability']}%"

    return f'No rain today in {city}. But maybe still a bad weather !!'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-h',
        '--help',
        action='help',
        help='api consumer to display a city weather. Use the command with a city name.'
    )
    parser.add_argument('city', help='Type a city to get the weather')
    args = parser.parse_args()
    woeid = get_city_woeid(args.city)
    weather = get_city_weather(woeid, args.city)
    print(weather)
