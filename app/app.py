# -*- coding: utf-8 -*-
import os

from flask import Flask, json, render_template
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
        result = summarise_forecast(data)
        print(result)

    return render_template('index.html', title='Weather', form=form)


@app.route('/weather-graph', methods=['GET'])
def get_graph(chartID='chart_ID', chart_type='column', chart_height=550):
    """
    Build a graph with received data
    """
    pass


if __name__ == '__main__':
    app.run(host='localhost')
