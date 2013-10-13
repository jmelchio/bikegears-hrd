#!/usr/bin/env python
# encoding: utf-8
"""
welcome.py

Created by Joris Melchior on 2008-06-25.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""

import os
import webapp2
from google.appengine.ext.webapp import template
from helpers import makeMenu, makeUserLinks
from bikegears import FourOhFour

class Welcome(webapp.RequestHandler):
    """Main welcome page handler for the application"""
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template/welcome.html')
        template_values = makeUserLinks(self.request.uri)
        template_values['menu'] = makeMenu('')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([('/', Welcome)
                             , ('/.*', FourOhFour)]
                             , debug=True)

# That's All Folks!