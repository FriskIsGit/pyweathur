import requests
import json

OPENWEATHERMAP_API_KEY = 'e762d6c90e1f1670093b64960d9c7463'
WEATHER_API_KEY = '14b0cfe10aea45df883141650223009'
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
    if city_name[0].islower():
        city_name = city_name.capitalize()
    return city_name


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
def get_geocoordinates_of(city_name):
    LIMIT = 3
    geo_url = 'https://api.openweathermap.org/geo/1.0/direct?q=%s&limit=%d&appid=%s'
    geo_url = geo_url%(city_name, LIMIT, OPENWEATHERMAP_API_KEY)
    print(geo_url)
    response = requests.get(geo_url)
    status = response.status_code
    if status != 200:
        print("Status code:", status)
        return 0, 0

    json_dictionary = json.loads(response.text)
    first_city = json_dictionary[0];
    print('Candidate cities:', len(json_dictionary))
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
    temp = 'Temperature: %d C feels like %d;  %d F feels like %d'
    temp = temp%(current['temp_c'],current['feelslike_c'],current['temp_f'],current['feelslike_f'])
    winds = 'Winds:       %d kph;    %d mph'
    winds = winds%(current['wind_kph'], current['wind_mph'])
    print(temp)
    print(winds)
if __name__=="__main__":
    main()
