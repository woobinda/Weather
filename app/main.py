# -*- coding: utf-8 -*-
import os
from flask import Flask, json, render_template, redirect, url_for, abort
from flask import session
from flask_bootstrap import Bootstrap
from forms import WeatherRequestForm
from functions import utc_to_date, summarise_forecast, \
    get_api_data, get_chart_params


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Takes input data from client form and performs redirection to charts
    """
    form = WeatherRequestForm()
    if form.validate_on_submit():
        response = get_api_data(form.city.data, form.period.data)
        if response.status_code != 200:
            abort(404)
        response_data = json.loads(response.text)
        data = summarise_forecast(response_data)
        session['data'] = data
        session['response_data'] = response_data
        """
        Variable 'data' is a dictionary which contains a following keys:

            city              - city name
            dates_list        - array of dates
            morn_temps        - array of morning temperature
            day_temps         - array of day temperature
            night_temps       - array of night temperature
            forecasts         - array of dates grouped by weather
        """
        return redirect(url_for('get_charts'))
    return render_template('index.html', title='Weather', form=form)


@app.route('/charts', methods=['GET'])
def get_charts():
    """
    Build and display a charts with following data:

        chart         - display chart option settings
        period        - amount of days in requested period
        title         - chart title
        lable         - template title
        series        - groups of values that are displayed on the X axis
        xAxis         - units of X-axis
        yAxis         - units of Y-axis
    """
    try:
        data = session['data']
    except KeyError:
        abort(404)

    period = str(len(data['dates_list'])) + ' days'
    forecasts, title, lable, chart, chartID, series, \
        xAxis, yAxis = get_chart_params(data)

    return render_template('chart.html', chartID=chartID, series=series,
                           chart=chart, xAxis=xAxis, yAxis=yAxis, lable=lable,
                           forecasts=forecasts, period=period, title=title)


@app.route('/charts/<day_date>', methods=['GET'])
def charts_by_date(day_date):
    """
    Providing charts for single day on selected date:

        new_list        - array of values for requested day
        period          - day date in 'yyyy-mm-dd'
    """
    try:
        data = session['response_data']
    except KeyError:
        abort(404)
    new_list = [day for day in data['list'] if
                utc_to_date(day['dt']) == day_date]
    if not new_list:
        abort(404)

    data['list'] = new_list
    data = summarise_forecast(data)
    period = day_date
    forecasts, title, lable, chart, chartID, series, \
        xAxis, yAxis = get_chart_params(data)

    return render_template('chart.html', chartID=chartID, series=series,
                           chart=chart, xAxis=xAxis, yAxis=yAxis, lable=lable,
                           forecasts=forecasts, period=period, title=title)


if __name__ == '__main__':
    app.run(host='localhost')
