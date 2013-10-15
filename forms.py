#!/usr/bin/env python
# encoding: utf-8
"""
forms.py

Created by Joris Melchior on 2008-06-13.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""

from model import Bike, BikeRide, BikeType, RideType
from google.appengine.api import users
from google.appengine.ext.ndb import djangoforms

class BikeForm(djangoforms.ModelForm):
    class Meta:
        model = Bike
        exclude = ['bikeRider']
    


class BikeRideForm(djangoforms.ModelForm):
    bike = djangoforms.ModelChoiceField(Bike, None)
    
    def __init__(self, *args, **kwargs):
        self.base_fields['bike'].query = Bike.all().filter('bikeRider = ', users.get_current_user())
        self.base_fields['bike'].widget.choices = self.base_fields['bike'].choices
        super(BikeRideForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = BikeRide
        exclude = ['bikeRider']
    


class BikeTypeForm(djangoforms.ModelForm):
    class Meta:
        model = BikeType
    


class RideTypeForm(djangoforms.ModelForm):
    class Meta:
        model = RideType
    
