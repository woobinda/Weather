# -*- coding: utf-8 -*-
import os

from flask import Flask, json, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from functions import get_api_data, summarise_forecast
from forms import RequestForm


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
        data = get_api_data(form.city.data, form.period.data)
        data = json.loads(data.text)
        data = summarise_forecast(data)
        """
        Data is a dictionary which contains next keys:

            city          - city name
            max_temp      - maximum temp on period
            min_temp      - minimum temp on period
            date_list     - array of dates
            temp_list     - array of temperature
            forecasts     - period dates grouped by weather
        """
        return redirect(url_for('get_graph', data=data))
    return render_template('index.html', title='Weather', form=form)


@app.route('/weather-graph', methods=['GET'])
def get_graph(data, chartID='chart_ID', chart_type='column', chart_height=550):
    """
    Build and display a graph with received data
    """
    dates = data['dates_list']
    xAxis = {"categories": dates}
    yAxis = {"title": {"text": 'temperature'}}


if __name__ == '__main__':
    app.run(host='localhost', port=7000)
