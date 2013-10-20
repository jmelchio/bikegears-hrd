#!/usr/bin/env python
# encoding: utf-8
"""
welcome.py

Created by Joris Melchior on 2008-06-25.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""

import os
import webapp2
import jinja2
from helpers import makeMenu, makeUserLinks
from bikegears import FourOhFour

jinjaEnvironment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Welcome(webapp2.RequestHandler):
    """Main welcome page handler for the application"""
    def get(self):
        template = jinjaEnvironment.get_template('template/welcome.html')
        template_values = makeUserLinks(self.request.uri)
        template_values['menu'] = makeMenu('')
        self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', Welcome)
                             , ('/.*', FourOhFour)]
                             , debug=True)

# That's All Folks!