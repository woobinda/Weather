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

APPID = '1263e8d0166fbbac6b8c90ec718a2e8d'  # unique account ID
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
                                                              message='Available 1-14 days period')])
    submit = SubmitField('Show weather')


def utc_to_date(utc):
    """
    Translate utc date format to 'yyyy-mm-dd'

    """
    date = datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d')
    return date


def request_to_api(city, period, units='metric'):
    """
    Return API response for requested period with JSON data

            units	- temperature units format('metric'=Kelvins)

    """
    city = 'q=' + city
    period = 'cnt=' + str(period)
    units = 'units=' + units
    _id = 'APPID=' + APPID
    request_data = city, units, period, _id
    request_to_api = requests.request('POST', url + ('&').join(request_data))
    return request_to_api.text


@app.route('/', methods=['GET', 'POST'])
def summarise_forecast():
    """
    Default View with client form

    """
    form = RequestForm()
    if form.validate_on_submit():
        data = request_to_api(form.city.data, form.period.data)
        data = json.loads(data)
        city = data['city']['name']
        max_temp = max(value['temp']['max'] for value in data['list'])
        min_temp = min(value['temp']['min'] for value in data['list'])
        """
		Grouping data dates by weather
		"""
        forecasts = []
        for day in data['list']:
            forecasts.append((day['dt'], day['weather'][0]['main']))
        weather_list = list(set(map(lambda x: x[1], forecasts)))
        date_list = [[utc_to_date(value[0]) for value in forecasts if value[1] == weather]
                     for weather in weather_list]
        forecasts = {}
        for i in range(len(weather_list)):
            forecasts[weather_list[i]] = date_list[i]

        result = {
            'city': city,
            'max': max_temp,
            'min': min_temp,
            'forecasts': forecasts
        }
        print(result)

    return render_template('index.html', title='Weather', form=form)


if __name__ == '__main__':
    app.run(host='localhost', threaded=True)
