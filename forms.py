#!/usr/bin/env python
# encoding: utf-8
"""
forms.py

Created by Joris Melchior on 2008-06-13.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""

from model import Bike, BikeRide, BikeType, RideType
from google.appengine.api import users
from wtforms.ext.appengine import ndb, fields

BikeForm = ndb.model_form(Bike, exclude=['bikeRider'])

BikeRideForm = ndb.model_form(BikeRide, exclude=['bikeRider'])
# todo: need to get a query to get bike per bikeRider fields.KeyPropertyField?

BikeTypeForm = ndb.model_form(BikeType)

RideTypeForm = ndb.model_form(RideType)

# That's All Folks!!
