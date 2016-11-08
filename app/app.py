# -*- coding: utf-8 -*-
import requests
import os

from flask import Flask, json, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.validators import Required, NumberRange
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

bootstrap = Bootstrap(app)

# unique account ID
APPID = '1263e8d0166fbbac6b8c90ec718a2e8d'
# weather API provider url
url = 'http://api.openweathermap.org/data/2.5/forecast/daily?'


class RequestForm(FlaskForm):
    """
    Client form for request to API

            city 	- requested city
            period	- requested period in days
    """
    city = StringField('City',
                       render_kw={'placeholder': 'Enter a city'},
                       validators=[Required()])
    period = IntegerField('Period (days)',
                          default=7,
                          render_kw={'placeholder': 'Enter period in days'},
                          validators=[Required(), NumberRange(min=1, max=14,
                                                              message='Available 1-14 days period'
                                                              )])
    submit = SubmitField('Show weather')


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
    # Parsing a received from API data
    city = data['city']['name']
    max_temp = max(value['temp']['max'] for value in data['list'])
    min_temp = min(value['temp']['min'] for value in data['list'])

    # grouping dates by weather
    forecasts = []
    for day in data['list']:
        forecasts.append((day['dt'], day['weather'][0]['main']))
    weather_list = list(set(map(lambda x: x[1], forecasts)))
    date_list = [[utc_to_date(x[0]) for x in forecasts if x[1] == weather]
                 for weather in weather_list]
    forecasts = {}
    for i in range(len(weather_list)):
        forecasts[weather_list[i]] = date_list[i]

    result = {
        'city': city,			# city name
        'max_temp': max_temp,   # maximum temp on period
        'min_temp': min_temp,   # minimum temp on period
        'forecasts': forecasts  # period dates grouped by weather
    }
    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Display form and redirect client to graph
    """
    form = RequestForm()
    if form.validate_on_submit():
        data = get_api_data(form.city.data, form.period.data)
        data = json.loads(data.text)
        result = summarise_forecast(data)
        print(result)

    return render_template('index.html', title='Weather', form=form)


if __name__ == '__main__':
    app.run(host='localhost')
