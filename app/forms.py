# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.validators import Required, NumberRange


class RequestForm(FlaskForm):
    """
    Client form for request to API with next fields:

            city 	      - city name
            period	    - period in days
            
    """
    city = StringField('City',
                       render_kw={'placeholder': 'Enter a city'},
                       validators=[Required()])
    period = IntegerField('Period (days)',
                          default=7,
                          render_kw={'placeholder': 'Enter period in days'},
                          validators=[Required(), NumberRange(min=1, max=14,
                                                              message='Available 1-14 days periods'
                                                              )])
    submit = SubmitField('Show weather')
