# -*- coding: utf-8 -*-
import os
from flask import Flask, json, render_template, redirect, url_for
from flask import session
from flask_bootstrap import Bootstrap
from forms import RequestForm
from functions import get_api_data, summarise_forecast


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Display form and redirect client to graph
    """
    form = RequestForm()
    if form.validate_on_submit():
        response = get_api_data(form.city.data, form.period.data)
        data = json.loads(response.text)
        data = summarise_forecast(data)
        session['data'] = data
        session['period'] = form.period.data
        """
        Variable 'data' is a dictionary which contains next keys:

            city              - city name
            dates_list        - array of dates
            morn_temps        - array of morning temperature
            day_temps         - array of day temperature
            night_temps       - array of night temperature
            forecasts         - period dates grouped by weather
        """
        return redirect(url_for('get_chart'))
    return render_template('index.html', title='Weather', form=form)


@app.route('/chart', methods=['GET'])
def get_chart(chartID='chart_ID', chart_type='column',
              chart_height=520, chart_width=1200):
    """
    Build and display a graph with received data

            chart          - display chart option settings
            lable          - template title
            title          - chart title
            period         - amount of days in requested period
            series         - groups of values that are displayed on the X axis
            xAxis          - units of X-axis
            yAxis          - units of Y-axis
    """
    chart = {"renderTo": chartID, "type": chart_type,
             "height": chart_height, "width": chart_width,
             }

    data = session['data']
    period = session['period']
    lable = 'Forecast in %s' % data['city']
    title = {"text": 'Temperature in %s' % str(data['city'])}
    forecasts = data['forecasts']
    series = [
        {"name": 'Morning', "data": data['morn_temps']},
        {"name": 'Day',     "data": data['day_temps']},
        {"name": 'Night',   "data": data['night_temps']}
    ]
    xAxis = {"categories": data['dates_list']}
    yAxis = {"title": {"text": 'Temperature'}}
    return render_template('chart.html', chartID=chartID, series=series,
                           chart=chart, xAxis=xAxis, yAxis=yAxis, lable=lable,
                           forecasts=forecasts, period=period, title=title)


if __name__ == '__main__':
    app.run(host='localhost')
