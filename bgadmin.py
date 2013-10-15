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
from google.appengine.ext.webapp import template
from model import BikeType, RideType
from forms import BikeTypeForm, RideTypeForm
from bikegears import FourOhFour
from helpers import makeUserLinks, makeAdminMenu

class MainAdmin(webapp2.RequestHandler):
    """Main admin screen handler"""
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template/adminwelcome.html')
        template_values = makeUserLinks(self.request.uri)
        template_values['menu'] = makeAdminMenu(page='admin')
        template_values['bikeTypes'] = BikeType.all()
        template_values['rideTypes'] = RideType.all()
        self.response.out.write(template.render(path, template_values))

class RideTypeEntry(webapp2.RequestHandler):
    """Handler for adding and updating RideType objects"""
    def get(self):
        template_values = makeUserLinks(self.request.uri)
        try:
            id = int(self.request.get('id'))
            rideType = RideType.get(db.Key.from_path('RideType', id))
            template_values['submitValue'] = 'Update'
        except ValueError:
            rideType = None
            id = None
            template_values['submitValue'] = 'Create'
        path = os.path.join(os.path.dirname(__file__), 'template/ridetypeentry.html')
        template_values['menu'] = makeAdminMenu(page='admin/ridetypeentry')
        template_values['form'] = RideTypeForm(instance=rideType)
        template_values['id'] = id
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        try:
            id = int(self.request.get('_id'))
            rideType = RideType.get(db.Key.from_path('RideType', id))
        except ValueError:
            rideType = None
            id = None
        data = RideTypeForm(data=self.request.POST, instance=rideType)
        
        if data.is_valid():
            # Save and redirect to admin home page
            entity = data.save(commit=False)
            entity.put()
            self.redirect('/admin')
        else:
            # back to form for editing
            path = os.path.join(os.path.dirname(__file__), 'template/ridetypeentry.html')
            template_values = makeUserLinks(self.request.uri)
            template_values['menu'] = makeAdminMenu(page='admin/ridetypeentry')
            template_values['submitValue'] = 'Fix'
            template_values['form'] = data
            template_values['id'] = id
            self.response.out.write(template.render(path, template_values))
    

class BikeTypeEntry(webapp2.RequestHandler):
    """Handler for adding and updating BikeType objects"""
    def get(self):
        template_values = makeUserLinks(self.request.uri)
        try:
            id = int(self.request.get('id'))
            bikeType = BikeType.get(db.Key.from_path('BikeType', id))
            template_values['submitValue'] = 'Update'
        except ValueError:
            bikeType = None
            id = None
            template_values['submitValue'] = 'Create'
        path = os.path.join(os.path.dirname(__file__), 'template/biketypeentry.html')
        template_values['menu'] = makeAdminMenu(page='admin/biketypeentry')
        template_values['form'] = BikeTypeForm(instance=bikeType)
        template_values['id'] = id
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        try:
            id = int(self.request.get('_id'))
            bikeType = BikeType.get(db.Key.from_path('BikeType', id))
        except ValueError:
            bikeType = None
            id = None
        data = BikeTypeForm(data=self.request.POST, instance=bikeType)
        
        if data.is_valid():
            # Save and redirect to admin home page
            entity = data.save(commit=False)
            entity.put()
            self.redirect('/admin')
        else:
            # back to form for editing
            path = os.path.join(os.path.dirname(__file__), 'template/biketypeentry.html')
            template_values = makeUserLinks(self.request.uri)
            template_values['menu'] = makeAdminMenu(page='admin/biketypeentry')
            template_values['submitValue'] = 'Fix'
            template_values['form'] = data
            template_values['id'] = id
            self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([('/admin', MainAdmin)
                             , ('/admin/ridetypeentry', RideTypeEntry)
                             , ('/admin/biketypeentry', BikeTypeEntry)
                             , ('/admin.*', FourOhFour)]
                             , debug=True)

# That's All Folks!