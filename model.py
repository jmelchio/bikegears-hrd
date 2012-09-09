#!/usr/bin/env python
# encoding: utf-8
"""
model.py

Created by Joris Melchior on 2008-06-07.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""
from datetime import time
from google.appengine.ext import db

class BikeType(db.Model):
    """docstring for BikeType"""
    name = db.StringProperty(required=True)
    description = db.StringProperty(required=True, multiline=True)
    
    def __str__(self):
        return self.name


class Bike(db.Model):
    """docstring for Bike"""
    brand = db.StringProperty(required=True)
    model = db.StringProperty(required=True)
    color = db.StringProperty()
    year = db.IntegerProperty()
    description = db.StringProperty(multiline=True)
    bikeType = db.ReferenceProperty(BikeType, required=True)
    bikeRider = db.UserProperty()
    
    def __str__(self):
        return '%s %s' % (self.brand, self.model)

class RideType(db.Model):
    """docstring for RideType"""
    name = db.StringProperty(required=True)
    description = db.StringProperty(required=True, multiline=True)
    
    def __str__(self):
        return self.name


class BikeRide(db.Model):
    """docstring for BikeRide"""
    date = db.DateProperty(required=True)
    startLocation = db.StringProperty()
    finishLocation = db.StringProperty()
    distanceKm = db.FloatProperty(required=True)
    rideTimeSeconds = db.IntegerProperty()
    averageHr = db.IntegerProperty()
    maximumHr = db.IntegerProperty()
    caloriesBurnt = db.IntegerProperty()
    journal = db.StringProperty(multiline=True)
    bikeRider = db.UserProperty()
    rideType = db.ReferenceProperty(RideType, required=True)
    bike = db.ReferenceProperty(Bike, required=True)
    
    def __str__(self):
        return '%s %s' % (self.date, self.distanceKm)
    
    def getRideTime(self):
        if(self.rideTimeSeconds == None):
            return time(hour=0, minute=0, second=0).isoformat()
        
        hour = 0
        minute = 0
        second = 0
        if(self.rideTimeSeconds >= 3600):
            hour = self.rideTimeSeconds / 3600
            remainder = self.rideTimeSeconds % 3600
            if(remainder == 0):
                minute = remainder
                second = remainder
            else:
                minute = remainder / 60
                second = remainder % 60
        else:
            minute = self.rideTimeSeconds / 60
            second = self.rideTimeSeconds % 60
        
        return time(hour, minute, second)
    
    def getRideTimeAsString(self):
        return self.getRideTime().isoformat()
    
    def getAverageSpeed(self):
        if(self.rideTimeSeconds and self.distanceKm):
            return '%.2f' % ((self.distanceKm / self.rideTimeSeconds) * 3600)
        else:
            return 'NA'


# That's All Folks !!