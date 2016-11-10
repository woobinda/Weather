# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.validators import Required, NumberRange


class WeatherRequestForm(FlaskForm):
    """
    Client form for request to API, with following fields:
    
          city        - city name
          period      - period in days
    """
    city = StringField('City',
                       render_kw={'placeholder': 'Enter city name'},
                       validators=[Required()])

    period = IntegerField('Period (days)',
                          default=7,
                          render_kw={'placeholder': 'Enter period in days'},
                          validators=[Required(), NumberRange(
                              min=1, max=14,
                              message='Available period is 1-14 days'
                          )])
    submit = SubmitField('Show weather')
