import requests
from datetime import datetime


def request_weather(api_key, location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang={}".format(location, api_key,
                                                                                                      'DE')
    weather_json = requests.get(url).json()

    # check if response failed, exit at failure
    if weather_json['cod'] != 200:
        print('error code:', str(weather_json['cod']), '-', weather_json['message'])
        exit(1)

    weather = Weather(weather_json)
    return weather


def get_wind_direction(degree):
    if degree < 0:
        return 'bullshit'
    elif degree <= 22.5:
        return 'north'
    elif degree <= 67.5:
        return 'north east'
    elif degree <= 112.5:
        return 'east'
    elif degree <= 157.5:
        return 'south east'
    elif degree <= 202.5:
        return 'south'
    elif degree <= 247.5:
        return 'south west'
    elif degree <= 292.5:
        return 'west'
    elif degree <= 337.5:
        return 'north west'
    else:
        return 'north'

def get_timezone(seconds_from_utc):
    hours = int(seconds_from_utc / 60 / 60 - 1)
    sign = '+' if hours > 0 else ''

    return f'{sign}{hours} hours'

class Weather:
    country = None
    city_name = None

    coord_lon = None
    coord_lat = None

    timezone = None
    sunrise = None
    sunset = None

    weather = None
    weather_desc = None

    temp = None
    temp_feels_like = None
    temp_min = None
    temp_max = None
    pressure = None
    humidity = None

    wind_speed = None
    wind_deg = None

    def __init__(self, weather):
        self.country = weather['sys']['country']
        self.city_name = weather['name']

        self.coord_lon = weather['coord']['lon']
        self.coord_lat = weather['coord']['lat']

        self.timezone = weather['timezone']
        self.sunrise = weather['sys']['sunrise']
        self.sunset = weather['sys']['sunset']

        self.weather = weather['weather'][0]['main']  # weather is an array
        self.weather_desc = weather['weather'][0]['description']

        self.temp = weather['main']['temp']
        self.temp_feels_like = weather['main']['feels_like']
        self.temp_min = weather['main']['temp_min']
        self.temp_max = weather['main']['temp_max']
        self.pressure = weather['main']['pressure']
        self.humidity = weather['main']['humidity']

        self.wind_speed = weather['wind']['speed']
        self.wind_deg = weather['wind']['deg']

    def print(self):
        print('country:', self.country)
        print('city_name:', self.city_name)
        print('coord_lon:', self.coord_lon)
        print('coord_lat:', self.coord_lat)
        print('timezone:', self.timezone)
        print('sunrise:', self.sunrise)
        print('sunset:', self.sunset)
        print('weather:', self.weather)
        print('weather_desc:', self.weather_desc)
        print('temp:', self.temp)
        print('temp_feels_like:', self.temp_feels_like)
        print('temp_min:', self.temp_min)
        print('temp_max:', self.temp_max)
        print('pressure:', self.pressure)
        print('humidity:', self.humidity)
        print('wind_speed:', self.wind_speed)
        print('wind_deg:', self.wind_deg)

    def get_description(self):
        return f"""timezone: {get_timezone(self.timezone)}
weather_desc: {self.weather_desc}
minimal_temperatur: {self.temp_min}°C
maximal_temperatur: {self.temp_max}°C
humidity: {self.humidity}%
wind_speed: {self.wind_speed} km/h
wind_dir: {get_wind_direction(self.wind_deg)}

sunrise: {datetime.utcfromtimestamp(int(self.sunrise)).strftime('%H:%M:%S')}
sunset: {datetime.utcfromtimestamp(int(self.sunset)).strftime('%H:%M:%S')}
"""
