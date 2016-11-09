# -*- coding: utf-8 -*-
import requests

from datetime import datetime


# unique account ID
APPID = '1263e8d0166fbbac6b8c90ec718a2e8d'
# weather API provider url
url = 'http://api.openweathermap.org/data/2.5/forecast/daily?'


def utc_to_date(utc):
    """
    Translate utc date format to 'yyyy-mm-dd'
    """
    date = datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d')
    return date


def get_api_data(city, period, units='metric'):
    """
    Create request to weather API and return response with JSON data

            units	- temperature units format('metric' = Kelvins)
    """
    city = 'q=' + city
    period = 'cnt=' + str(period)
    units = 'units=' + units
    appid = 'APPID=' + APPID
    request_data = city, units, period, appid
    response = requests.request('POST', url + ('&').join(request_data))
    return response


def summarise_forecast(data):
    """
    Parsing a received from API data
    """
    city = data['city']['name']
    forecasts = []
    # sorting weather and date for each day
    for day in data['list']:
        forecasts.append((day['dt'], day['weather'][0]['main']))
    weather_list = list(set(map(lambda x: x[1], forecasts)))
    dates_list = [[utc_to_date(x[0]) for x in forecasts if x[1] == weather]
                  for weather in weather_list]

    # grouping dates by weather
    forecasts = []
    for i in range(len(dates_list)):
        forecasts.append([weather_list[i], dates_list[i]])

    # preparation additional data for build chart
    morn_temps = [day['temp']['morn'] for day in data['list']]
    day_temps = [day['temp']['day'] for day in data['list']]
    night_temps = [day['temp']['night'] for day in data['list']]
    dates_list = [utc_to_date(day['dt']) for day in data['list']]

    result = {
        'city': city,                   # city name
        'dates_list': dates_list,       # array of dates
        'morn_temps': morn_temps,       # array of morning temperature
        'day_temps': day_temps,         # array of day temperature
        'night_temps': night_temps,     # array of night temperature
        'forecasts': forecasts          # period dates grouped by weather
    }
    return result
