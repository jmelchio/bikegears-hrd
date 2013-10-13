#!/usr/bin/env python
# encoding: utf-8
"""
bikegears.py

Created by Joris Melchior on 2008-06-06.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""
import os
import webapp2
import logging
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from model import Bike, BikeRide, BikeType
from forms import BikeForm, BikeRideForm
from helpers import makeMenu, makeUserLinks
from datetime import date

class BikeOverview(webapp.RequestHandler):
    """overview page for bikes of the rider"""
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template/bikeoverview.html')
        template_values = makeUserLinks(self.request.uri)
        template_values['menu'] = makeMenu(page='user/bikeoverview')
        template_values['bikes'] = Bike.all().filter('bikeRider = ', users.get_current_user())
        template_values['biketypes'] = BikeType.all()
        self.response.out.write(template.render(path, template_values))


class RiderOverview(webapp.RequestHandler):
    """Overview page for recent rides and totals of the rider
       
       This page currently shows the 10 most recent rides of the rider with options to edit or
       delete a ride. It also shows the user name of the current user.
       This page should really show some interesting totals but because there are not aggregate
       queries supported by the data source for AppEngine I have to come up with a suitable
       way of providing the totals without making it too much of a hack.
    """
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template/rideroverview.html')
        template_values = makeUserLinks(self.request.uri)
        template_values['menu'] = makeMenu(page='user/rideroverview')
        template_values['rides'] = BikeRide.gql('where bikeRider = :1 order by date desc', users.get_current_user()).fetch(limit=10)
        self.response.out.write(template.render(path, template_values))


class BikeEntry(webapp.RequestHandler):
    """Handler for entry of the bike both get and post actions
       
       This handler will fetch, insert and update entries for the Bike class.
       Fetching is done in the get method, if no Bike is found creation of a new Bike is assumed.
       Updating and inserting is done in the post method. If a key is provided the record belonging 
       to the key is updated, otherwise a new record is inserted in the table.
    """
    def get(self):
        template_values = makeUserLinks(self.request.uri)
        try:
            id = int(self.request.get('id'))
            bike = Bike.get(db.Key.from_path('Bike', id))
            template_values['submitValue'] = 'Update'
        except ValueError:
            id = None
            bike = None
            template_values['submitValue'] = 'Create'
        
        path = os.path.join(os.path.dirname(__file__), 'template/bikeentry.html')
        template_values['menu'] = makeMenu(page='user/bikeentry')
        template_values['form'] = BikeForm(instance=bike)
        template_values['id'] = id
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        try:
            id = int(self.request.get('_id'))
            bike = Bike.get(db.Key.from_path('Bike', id))
        except ValueError:
            bike = None
            id = None
        data = BikeForm(data=self.request.POST, instance=bike)
        
        if data.is_valid():
            # Save and redirect to admin home page
            entity = data.save(commit=False)
            entity.bikeRider = users.get_current_user()
            entity.put()
            self.redirect('/user/bikeoverview')
        else:
            # back to form for editing
            path = os.path.join(os.path.dirname(__file__), 'template/bikeentry.html')
            template_values = makeUserLinks(self.request.uri)
            template_values['menu'] = makeMenu(page='user/bikeentry')
            template_values['submitValue'] = 'Fix'
            template_values['form'] = data
            template_values['id'] = id
            self.response.out.write(template.render(path, template_values))
    


class RideEntry(webapp.RequestHandler):
    """handler for entry of the bike rides both get and post actions"""
    def get(self):
        template_values = makeUserLinks(self.request.uri)
        try:
            id = int(self.request.get('id'))
            bikeRide = BikeRide.get(db.Key.from_path('BikeRide', id))
            template_values['submitValue'] = 'Update'
            template_values['form'] = BikeRideForm(instance=bikeRide)
        except ValueError:
            id = None
            bikeRide = None
            template_values['submitValue'] = 'Create'
            template_values['form'] = BikeRideForm(initial={'date':date.today().isoformat()})
        
        path = os.path.join(os.path.dirname(__file__), 'template/rideentry.html')
        template_values['menu'] = makeMenu(page='user/rideentry')
        template_values['id'] = id
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        try:
            id = int(self.request.get('_id'))
            bikeRide = BikeRide.get(db.Key.from_path('BikeRide', id))
        except ValueError:
            bikeRide = None
            id = None
        data = BikeRideForm(data=self.request.POST, instance=bikeRide)
        logging.info("data from bikeride form is: %s", data)
        logging.info("data from the bikeride request is: %s", self.request)
        
        if data.is_valid():
            entity = data.save(commit=False)
            entity.bikeRider = users.get_current_user()
            entity.put()
            self.redirect('/user/rideroverview')
        else:
            path = os.path.join(os.path.dirname(__file__), 'template/rideentry.html')
            template_values = makeUserLinks(self.request.uri)
            template_values['menu'] = makeMenu(page='user/rideentry')
            template_values['submitValue'] = 'Fix'
            template_values['form'] = data
            template_values['id'] = id
            self.response.out.write(template.render(path, template_values))
    

class FourOhFour(webapp.RequestHandler):
    """Handler for all pages that don't have an explicit handler (404)"""
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template/under_construction.html')
        template_values = makeUserLinks(self.request.uri)
        template_values['menu'] = makeMenu()
        template_values['message'] = 'Requested page not found'
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([('/user/bikeoverview', BikeOverview)
                              , ('/user/rideroverview', RiderOverview)
                              , ('/user/rideentry', RideEntry)
                              , ('/user/bikeentry', BikeEntry)
                              , ('/user.*', FourOhFour)]
                              , debug=True)

# That's All Folks!