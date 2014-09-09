#!/usr/bin/env python
# encoding: utf-8
"""
bgadmin.py

Created by Joris Melchior on 2008-06-14.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""

import os
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import logging
from model import BikeType, RideType
from forms import BikeTypeForm, RideTypeForm
from bikegears import FourOhFour
from helpers import make_user_links, make_admin_menu

jinjaEnvironment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainAdmin(webapp2.RequestHandler):
    """Main admin screen handler"""
    def get(self):
        template = jinjaEnvironment.get_template('template/adminwelcome.html')
        template_values = make_user_links(self.request.uri)
        template_values['menu'] = make_admin_menu(page='admin')
        template_values['bikeTypes'] = BikeType.query().fetch()
        template_values['rideTypes'] = RideType.query().fetch()
        self.response.out.write(template.render(template_values))


class RideTypeEntry(webapp2.RequestHandler):
    """Handler for adding and updating RideType objects"""
    def get(self):
        template_values = make_user_links(self.request.uri)
        id = self.request.get('id')
        
        try:
            ride_type = RideType.get_by_id(int(id))
            template_values['submitValue'] = 'Update'
        except ValueError:
            ride_type = RideType()
            id = None
            template_values['submitValue'] = 'Create'
        
        template = jinjaEnvironment.get_template('template/ridetypeentry.html')
        template_values['menu'] = make_admin_menu(page='admin/ridetypeentry')
        template_values['form'] = RideTypeForm(obj=ride_type)
        template_values['id'] = id
        self.response.out.write(template.render(template_values))
    
    def post(self):
        id = self.request.get('_id')
        
        try:
            ride_type = RideType.get_by_id(int(id))
        except ValueError:
            ride_type = RideType()
            id = None
        
        form_data = RideTypeForm(self.request.POST, ride_type)
        
        if form_data.validate():
            # Save and redirect to admin home page
            form_data.populate_obj(ride_type)
            ride_type.put()
            self.redirect('/admin')
        else:
            # back to form for editing
            template = jinjaEnvironment.get_template('template/ridetypeentry.html')
            template_values = make_user_links(self.request.uri)
            template_values['menu'] = make_admin_menu(page='admin/ridetypeentry')
            template_values['submitValue'] = 'Fix'
            template_values['form'] = form_data
            template_values['id'] = id
            self.response.out.write(template.render(template_values))
    

class BikeTypeEntry(webapp2.RequestHandler):
    """Handler for adding and updating BikeType objects"""
    def get(self):
        template_values = make_user_links(self.request.uri)
        id = self.request.get('id')
        
        try:
            bike_type = BikeType.get_by_id(int(id))
            template_values['submitValue'] = 'Update'
        except ValueError:
            bike_type = BikeType()
            id = None
            template_values['submitValue'] = 'Create'
            
        template = jinjaEnvironment.get_template('template/biketypeentry.html')
        template_values['menu'] = make_admin_menu(page='admin/biketypeentry')
        template_values['form'] = BikeTypeForm(obj=bike_type)
        template_values['id'] = id
        self.response.out.write(template.render(template_values))
    
    def post(self):
        id = self.request.get('_id')
        try:
            bike_type = BikeType.get_by_id(int(id))
        except ValueError:
            bike_type = BikeType()
            id = None
        form_data = BikeTypeForm(self.request.POST, bike_type)
        
        if form_data.validate():
            # Save and redirect to admin home page
            form_data.populate_obj(bike_type)
            bike_type.put()
            self.redirect('/admin')
        else:
            # back to form for editing
            template = jinjaEnvironment.get_template('template/biketypeentry.html')
            template_values = make_user_links(self.request.uri)
            template_values['menu'] = make_admin_menu(page='admin/biketypeentry')
            template_values['submitValue'] = 'Fix'
            template_values['form'] = form_data
            template_values['id'] = id
            self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/admin', MainAdmin)
                             , ('/admin/ridetypeentry', RideTypeEntry)
                             , ('/admin/biketypeentry', BikeTypeEntry)
                             , ('/admin.*', FourOhFour)]
                             , debug=True)

# That's All Folks!