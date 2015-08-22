#!/usr/bin/env python
# encoding: utf-8
"""
forms.py

Created by Joris Melchior on 2008-06-13.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""

from wtforms import Form, StringField, TextAreaField, IntegerField, SelectField, DateField, FloatField, validators


class BikeForm(Form):
    """docstring for BikeForm"""
    brand = StringField(u'Brand', validators=[validators.input_required()])
    model = StringField(u'Model', validators=[validators.input_required()])
    color = StringField(u'Color')
    year = IntegerField(u'Year')
    bikeType = SelectField(u'Bike type')
    description = TextAreaField(u'Description')


class BikeRideForm(Form):
    """docstring for BikeRideForm"""
    date = DateField(u'Ride date', validators=[validators.input_required()])
    distanceKm = FloatField(u'Distance', validators=[validators.input_required()])
    rideTimeSeconds = IntegerField(u'Ride Time (secs)')
    averageHr = IntegerField(u'Average HR')
    maximumHr = IntegerField(u'Maximum HR')
    caloriesBurnt = IntegerField(u'Calories burnt')
    journal = TextAreaField(u'Journal')
    rideType = SelectField(u'Ride Type')
    bike = SelectField(u'Bike')


class BikeTypeForm(Form):
    """docstring for BikeTypeForm"""
    name = StringField(u'Name', validators=[validators.input_required()])
    description = TextAreaField(u'Description', validators=[validators.input_required()])


class RideTypeForm(Form):
    """docstring for RideTypeForm"""
    name = StringField(u'Name', validators=[validators.input_required()])
    description = TextAreaField(u'Description', validators=[validators.input_required()])


# That's All Folks!!
