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
from helpers import make_menu, make_user_links, get_profile

jinjaEnvironment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class BikeOverview(webapp2.RequestHandler):
    """overview page for bikes of the rider"""

    def get(self):
        profile = get_profile()
        template = jinjaEnvironment.get_template('template/bikeoverview.html')
        template_values = make_user_links(self.request.uri)
        template_values['menu'] = make_menu(page='user/bikeoverview')
        template_values['bikes'] = Bike.query(ancestor=profile.key).fetch()
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
        profile = get_profile()
        template = jinjaEnvironment.get_template('template/rideroverview.html')
        template_values = make_user_links(self.request.uri)
        template_values['menu'] = make_menu(page='user/rideroverview')
        template_values['rides'] = BikeRide.query(ancestor=profile.key).order(-BikeRide.date).fetch(20)
        self.response.out.write(template.render(template_values))


class BikeEntry(webapp2.RequestHandler):
    """Handler for entry of the bike both get and post actions
       
       This handler will fetch, insert and update entries for the Bike class.
       Fetching is done in the get method, if no Bike is found creation of a new Bike is assumed.
       Updating and inserting is done in the post method. If a key is provided the record belonging 
       to the key is updated, otherwise a new record is inserted in the table.
    """

    def get(self):
        error_list = []
        profile = get_profile()
        template_values = make_user_links(self.request.uri)
        key = self.request.get('key')
        # below test is a bit of a hack because an empty key is returned as the string 'None' sometimes
        if key and (key != 'None'):
            b_key = ndb.Key(urlsafe=key)
            bike = b_key.get()
            template_values['submitValue'] = 'Update'
            if bike:
                if b_key.parent() != profile.key:
                    error_list.append('Attempt to edit bike not owned by user')
            else:
                error_list.append('Bike not found')
        else:
            key = None
            bike = Bike()
            template_values['submitValue'] = 'Create'

        if len(error_list) > 0:
            logging.info('%s' % error_list)
            self.redirect('user/errorPage')
        else:
            template = jinjaEnvironment.get_template('template/bikeentry.html')
            template_values['menu'] = make_menu(page='user/bikeentry')
            bike_form = BikeForm(obj=bike)
            bike_form.bikeType.choices = [(bikeType.key.urlsafe(), bikeType.name) for bikeType in
                                          BikeType.query().fetch()]
            bike_form.bikeType.data = (bike.bikeType.urlsafe() if bike.bikeType else 0)
            template_values['form'] = bike_form
            template_values['key'] = key
            self.response.out.write(template.render(template_values))

    def post(self):
        key = self.request.get('key')
        if key and (key != 'None'):
            b_key = ndb.Key(urlsafe=key)
            bike = b_key.get()
        else:
            profile = get_profile()
            bike = Bike(parent=profile.key)

        form_data = BikeForm(self.request.POST, bike)
        form_data.bikeType.choices = [(bikeType.key.urlsafe(), bikeType.name) for bikeType in BikeType.query().fetch()]
        logging.info('%s' % form_data.bikeType.data)

        if form_data.validate():
            # Save and redirect to bike overview page
            form_data.bikeType.data = ndb.Key(
                urlsafe=form_data.bikeType.data)  # translate urlsafe key string to actual key
            form_data.populate_obj(bike)
            bike.put()
            self.redirect('/user/bikeoverview')
        else:
            # back to form for editing
            template = jinjaEnvironment.get_template('template/bikeentry.html')
            template_values = make_user_links(self.request.uri)
            template_values['menu'] = make_menu(page='user/bikeentry')
            template_values['submitValue'] = 'Fix'
            template_values['form'] = form_data
            template_values['key'] = key
            self.response.out.write(template.render(template_values))


class RideEntry(webapp2.RequestHandler):
    """handler for entry of the bike rides both get and post actions"""

    def get(self):
        cur_user = users.get_current_user();
        template_values = make_user_links(self.request.uri)
        error_list = []
        id = self.request.get('id')
        try:
            bike_ride = BikeRide.get_by_id(int(id))
            template_values['submitValue'] = 'Update'
            try:
                if bike_ride.bikeRider != cur_user:
                    error_list.append('Attempt to edit bikeRide not owned by user')
            except AttributeError:
                error_list.append('bikeRide not found')
        except ValueError:
            id = None
            bike_ride = BikeRide()
            template_values['submitValue'] = 'Create'

        if len(error_list) > 0:
            logging.info('%s' % error_list)
            self.redirect('/user/errorPage')
        else:
            bike_ride_form = BikeRideForm(obj=bike_ride)
            bike_ride_form.bike.choices = [(bike.key.urlsafe(), bike.brand + ' ' + bike.model) for bike in
                                           Bike.query(Bike.bikeRider == cur_user).fetch()]
            bike_ride_form.bike.data = (bike_ride.bike.urlsafe() if bike_ride.bike else 0)
            bike_ride_form.rideType.choices = [(rideType.key.urlsafe(), rideType.name) for rideType in
                                               RideType.query().fetch()]
            bike_ride_form.rideType.data = (bike_ride.rideType.urlsafe() if bike_ride.rideType else 0)
            template_values['form'] = bike_ride_form
            template = jinjaEnvironment.get_template('template/rideentry.html')
            template_values['menu'] = make_menu(page='user/rideentry')
            template_values['id'] = id
            self.response.out.write(template.render(template_values))

    def post(self):
        try:
            id = int(self.request.get('_id'))
            bike_ride = BikeRide.get_by_id(id)
        except ValueError:
            bike_ride = BikeRide()
            id = None

        form_data = BikeRideForm(self.request.POST, bike_ride)
        form_data.bike.choices = [(bike.key.urlsafe(), bike.brand) for bike in Bike.query().fetch()]
        form_data.rideType.choices = [(rideType.key.urlsafe(), rideType.name) for rideType in RideType.query().fetch()]
        logging.info("data from bikeride form is: %s", form_data)
        logging.info("data from the bikeride request is: %s", self.request)

        if form_data.validate():
            form_data.bike.data = ndb.Key(urlsafe=form_data.bike.data)
            form_data.rideType.data = ndb.Key(urlsafe=form_data.rideType.data)
            form_data.populate_obj(bike_ride)
            bike_ride.bikeRider = users.get_current_user()
            bike_ride.put()
            self.redirect('/user/rideroverview')
        else:
            template = jinjaEnvironment.get_template('template/rideentry.html')
            template_values = make_user_links(self.request.uri)
            template_values['menu'] = make_menu(page='user/rideentry')
            template_values['submitValue'] = 'Fix'
            template_values['form'] = form_data
            template_values['id'] = id
            self.response.out.write(template.render(template_values))


class FourOhFour(webapp2.RequestHandler):
    """Handler for all pages that don't have an explicit handler (404)"""

    def get(self):
        template = jinjaEnvironment.get_template('template/under_construction.html')
        template_values = make_user_links(self.request.uri)
        template_values['menu'] = make_menu()
        template_values['message'] = 'Requested page not found'
        self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/user/bikeoverview', BikeOverview)
                                  , ('/user/rideroverview', RiderOverview)
                                  , ('/user/rideentry', RideEntry)
                                  , ('/user/bikeentry', BikeEntry)
                                  , ('/user.*', FourOhFour)]
                              , debug=True)

# That's All Folks!