#!/usr/bin/env python
# encoding: utf-8
"""
model.py

Created by Joris Melchior on 2008-06-07.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""
from datetime import time
from google.appengine.ext import ndb


class BikeType(ndb.Model):
    """docstring for BikeType"""
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    
    def __str__(self):
        return self.name


class Bike(ndb.Model):
    """docstring for Bike"""
    brand = ndb.StringProperty(required=True)
    model = ndb.StringProperty(required=True)
    color = ndb.StringProperty()
    year = ndb.IntegerProperty()
    description = ndb.StringProperty()
    bikeType = ndb.KeyProperty(kind=BikeType, required=True)
    bikeRider = ndb.UserProperty()
    
    def __str__(self):
        return '%s %s' % (self.brand, self.model)


class RideType(ndb.Model):
    """docstring for RideType"""
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    
    def __str__(self):
        return self.name


class BikeRide(ndb.Model):
    """docstring for BikeRide"""
    date = ndb.DateProperty(required=True)
    startLocation = ndb.StringProperty()
    finishLocation = ndb.StringProperty()
    distanceKm = ndb.FloatProperty(required=True)
    rideTimeSeconds = ndb.IntegerProperty()
    averageHr = ndb.IntegerProperty()
    maximumHr = ndb.IntegerProperty()
    caloriesBurnt = ndb.IntegerProperty()
    journal = ndb.StringProperty()
    bikeRider = ndb.UserProperty()
    rideType = ndb.KeyProperty(kind=RideType, required=True)
    bike = ndb.KeyProperty(kind=Bike, required=True)
    
    def __str__(self):
        return '%s %s' % (self.date, self.distanceKm)
    
    def get_ride_time(self):
        if self.rideTimeSeconds == None:
            return time(hour=0, minute=0, second=0).isoformat()
        
        hour = 0
        if self.rideTimeSeconds >= 3600:
            hour = self.rideTimeSeconds / 3600
            remainder = self.rideTimeSeconds % 3600
            if remainder == 0:
                minute = remainder
                second = remainder
            else:
                minute = remainder / 60
                second = remainder % 60
        else:
            minute = self.rideTimeSeconds / 60
            second = self.rideTimeSeconds % 60
        
        return time(hour, minute, second)
    
    def get_ride_time_as_string(self):
        return self.get_ride_time().isoformat()
    
    def get_average_speed(self):
        if self.rideTimeSeconds and self.distanceKm:
            return '%.2f' % ((self.distanceKm / self.rideTimeSeconds) * 3600)
        else:
            return 'NA'


# That's All Folks !!