import requests
import json
from typing import Tuple

OPENWEATHERMAP_API_KEY = 'e762d6c90e1f1670093b64960d9c7463'
WEATHER_API_KEY = '97e5c007431143b496101324220110'
LONGEST_NAME_LEN = 58
def main():
    city_name = get_city()
    #city_name = 'London'

    print("---> openweathermap:")
    call_openweather_API(city_name)
    print("---> weatherapi:")
    call_weather_API(city_name)

def get_city():
    city_name = input("Enter city name: ")
    length = len(city_name)
    if (length > LONGEST_NAME_LEN) or (length < 1):
        print("Invalid name, try again.")
        return get_city()
    return city_name.capitalize()


def call_openweather_API(city_name):
    lat, lon = get_geocoordinates_of(city_name)
    if lat == 0 and lon == 0:
        return

    weather_url = 'https://api.openweathermap.org/data/3.0/onecall?lat=%f&lon=%f&exclude=hourly,daily,minutely&appid=%s'
    weather_url = weather_url%(lat, lon, OPENWEATHERMAP_API_KEY)
    response = requests.get(weather_url)

    status = response.status_code
    if status != 200:
        if status == 401:
            print("Invalid API key (status 401)")
            return
        print("Status code:", status)
        return

    print(response.text)
# -> float, float
def get_geocoordinates_of(city_name) -> Tuple[int,int]:
    LIMIT = 3
    geo_url = 'https://api.openweathermap.org/geo/1.0/direct?q=%s&limit=%d&appid=%s'
    geo_url = geo_url%(city_name, LIMIT, OPENWEATHERMAP_API_KEY)
    print(geo_url)
    response = requests.get(geo_url)
    status = response.status_code
    if status != 200:
        print("Status code:", status)
        return 0,0

    json_dictionary = json.loads(response.text)
    cities = len(json_dictionary)
    print('Candidate cities:', cities)
    if cities < 1:
        return 0,0
    first_city = json_dictionary[0];
    return 53.5, 9.99

def call_weather_API(city_name):
    url = 'https://api.weatherapi.com/v1/current.json?key=%s&q=%s&aqi=no'
    url = url%(WEATHER_API_KEY, city_name)
    print(url)
    response = requests.get(url)
    status = response.status_code
    if status != 200:
        if status == 400:
            print("Not found but says bad request")
        print("Status code:", status)
        return

    json_dictionary = json.loads(response.text)
    location_dict = json_dictionary['location']
    print(location_dict['name'], location_dict['country'], location_dict['localtime'])
    current = json_dictionary['current']
    temp   = 'Temperature: %.1f C feels like %.1f;  %.1f F feels like %.1f'
    temp   = temp%(current['temp_c'],current['feelslike_c'],current['temp_f'],current['feelslike_f'])
    print(temp)
    winds  = 'Winds:       %.1f kph;    %.1f mph'
    winds  = winds%(current['wind_kph'], current['wind_mph'])
    print(winds)
    precip = 'Rain:        %.1f mm;    %.1f inches'
    precip = precip%(current['precip_mm'], current['precip_in'])
    print(precip)

if __name__=="__main__":
    main()
