#!/usr/bin/env python
# encoding: utf-8
"""
bikegears.py

Created by Joris Melchior on 2008-06-06.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""
import os
import webapp2
import jinja2
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
from model import Bike, BikeRide, BikeType, RideType
from forms import BikeForm, BikeRideForm
from helpers import makeMenu, makeUserLinks
from datetime import date

jinjaEnvironment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BikeOverview(webapp2.RequestHandler):
    """overview page for bikes of the rider"""
    def get(self):
        curUser = users.get_current_user()
        template = jinjaEnvironment.get_template('template/bikeoverview.html')
        template_values = makeUserLinks(self.request.uri)
        template_values['menu'] = makeMenu(page='user/bikeoverview')
        template_values['bikes'] = Bike.query(Bike.bikeRider==curUser).fetch()
        template_values['biketypes'] = BikeType.query().fetch()
        self.response.out.write(template.render(template_values))


class RiderOverview(webapp2.RequestHandler):
    """Overview page for recent rides and totals of the rider
       
       This page currently shows the 10 most recent rides of the rider with options to edit or
       delete a ride. It also shows the user name of the current user.
       This page should really show some interesting totals but because there are not aggregate
       queries supported by the data source for AppEngine I have to come up with a suitable
       way of providing the totals without making it too much of a hack.
    """
    def get(self):
        curUser = users.get_current_user()
        template = jinjaEnvironment.get_template('template/rideroverview.html')
        template_values = makeUserLinks(self.request.uri)
        template_values['menu'] = makeMenu(page='user/rideroverview')
        template_values['rides'] = BikeRide.query(BikeRide.bikeRider==curUser).order(-BikeRide.date).fetch(20)
        self.response.out.write(template.render(template_values))


class BikeEntry(webapp2.RequestHandler):
    """Handler for entry of the bike both get and post actions
       
       This handler will fetch, insert and update entries for the Bike class.
       Fetching is done in the get method, if no Bike is found creation of a new Bike is assumed.
       Updating and inserting is done in the post method. If a key is provided the record belonging 
       to the key is updated, otherwise a new record is inserted in the table.
    """
    def get(self):
        template_values = makeUserLinks(self.request.uri)
        id = self.request.get('id')
        try:
            bike = Bike.get_by_id(int(id))
            template_values['submitValue'] = 'Update'
        except ValueError:
            id = None
            bike = Bike()
            template_values['submitValue'] = 'Create'
        
        template = jinjaEnvironment.get_template('template/bikeentry.html')
        template_values['menu'] = makeMenu(page='user/bikeentry')
        bikeForm = BikeForm(obj=bike)
        bikeForm.bikeType.choices = [(bikeType.key.urlsafe(), bikeType.name) for bikeType in BikeType.query().fetch()]
        template_values['form'] = bikeForm
        template_values['id'] = id
        self.response.out.write(template.render(template_values))
    
    def post(self):
        id = self.request.get('_id')
        try:
            bike = Bike.get_by_id(int(id))
        except ValueError:
            bike = Bike()
            id = None
            
        form_data = BikeForm(self.request.POST, bike)
        form_data.bikeType.choices = [(bikeType.key.urlsafe(), bikeType.name) for bikeType in BikeType.query().fetch()]
        logging.info('%s' % form_data.bikeType.data)
        
        if form_data.validate():
            # Save and redirect to admin home page
            form_data.bikeType.data = ndb.Key(urlsafe=form_data.bikeType.data) # translate urlsafe key string to actual key
            form_data.populate_obj(bike)
            bike.bikeRider = users.get_current_user()
            bike.put()
            self.redirect('/user/bikeoverview')
        else:
            # back to form for editing
            template = jinjaEnvironment.get_template('template/bikeentry.html')
            template_values = makeUserLinks(self.request.uri)
            template_values['menu'] = makeMenu(page='user/bikeentry')
            template_values['submitValue'] = 'Fix'
            template_values['form'] = form_data
            template_values['id'] = id
            self.response.out.write(template.render(template_values))
    


class RideEntry(webapp2.RequestHandler):
    """handler for entry of the bike rides both get and post actions"""
    def get(self):
        template_values = makeUserLinks(self.request.uri)
        try:
            id = int(self.request.get('id'))
            bikeRide = BikeRide.get_by_id(id)
            template_values['submitValue'] = 'Update'
        except ValueError:
            id = None
            bikeRide = BikeRide()
            template_values['submitValue'] = 'Create'
        
        bikeRideForm = BikeRideForm(obj=bikeRide)
        bikeRideForm.bike.choices = [(bike.key.urlsafe(), bike.brand) for bike in Bike.query().fetch()]
        bikeRideForm.rideType.choices = [(rideType.key.urlsafe(), rideType.name) for rideType in RideType.query().fetch()]
        template_values['form'] = bikeRideForm
        template = jinjaEnvironment.get_template('template/rideentry.html')
        template_values['menu'] = makeMenu(page='user/rideentry')
        template_values['id'] = id
        self.response.out.write(template.render(template_values))
    
    def post(self):
        try:
            id = int(self.request.get('_id'))
            bikeRide = Key(BikeRide, id).get()
        except ValueError:
            bikeRide = BikeRide()
            id = None
            
        form_data = BikeRideForm(self.request.POST, bikeRide)
        form_data.bike.choices = [(bike.key.urlsafe(), bike.brand) for bike in Bike.query().fetch()]
        form_data.rideType.choices = [(rideType.key.urlsafe(), rideType.name) for rideType in RideType.query().fetch()]
        logging.info("data from bikeride form is: %s", form_data)
        logging.info("data from the bikeride request is: %s", self.request)
        
        if form_data.validate():
            form_data.bike.data = ndb.Key(urlsafe=form_data.bike.data)
            form_data.rideType.data = ndb.Key(urlsafe=form_data.rideType.data)
            form_data.populate_obj(bikeRide)
            bikeRide.bikeRider = users.get_current_user()
            bikeRide.put()
            self.redirect('/user/rideroverview')
        else:
            template = jinjaEnvironment.get_template('template/rideentry.html')
            template_values = makeUserLinks(self.request.uri)
            template_values['menu'] = makeMenu(page='user/rideentry')
            template_values['submitValue'] = 'Fix'
            template_values['form'] = form_data
            template_values['id'] = id
            self.response.out.write(template.render(template_values))
    

class FourOhFour(webapp2.RequestHandler):
    """Handler for all pages that don't have an explicit handler (404)"""
    def get(self):
        template = jinjaEnvironment.get_template('template/under_construction.html')
        template_values = makeUserLinks(self.request.uri)
        template_values['menu'] = makeMenu()
        template_values['message'] = 'Requested page not found'
        self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/user/bikeoverview', BikeOverview)
                              , ('/user/rideroverview', RiderOverview)
                              , ('/user/rideentry', RideEntry)
                              , ('/user/bikeentry', BikeEntry)
                              , ('/user.*', FourOhFour)]
                              , debug=True)

# That's All Folks!