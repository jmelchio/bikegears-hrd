#!/usr/bin/env python
# encoding: utf-8
"""
helpers.py

Created by Joris Melchior on 2008-06-21.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""

from google.appengine.api import users

class MenuEntry(object):
    """The MenuEntry class."""
    def __init__(self, link=None, name=None, active=None):
        self.link = link
        self.name = name
        self.active = active


menuDict = {1:MenuEntry('', 'Home', False)
            , 2:MenuEntry('user/rideroverview', 'Rider Overview', False)
            , 3:MenuEntry('user/rideentry', 'Ride Entry', False)
            , 4:MenuEntry('user/bikeoverview', 'Bike Overview', False)
            , 5:MenuEntry('user/bikeentry', 'Bike Entry', False)}
            
adminMenuDict = {2:MenuEntry('', 'Home', False)
            , 1:MenuEntry('admin', 'Admin Home', False)
            , 3:MenuEntry('admin/ridetypeentry', 'Ride Type Entry', False)
            , 4:MenuEntry('admin/biketypeentry', 'Bike Type Entry', False)}

def makeMenu(page=None, user=None):
    menu=[]
    keyList = menuDict.keys()
    keyList.sort()
    for key in keyList:
        if page == menuDict[key].link:
            menuDict[key].active = True
        else:
            menuDict[key].active = False
        menu.append(menuDict[key])
    return menu

def makeAdminMenu(page=None, user=None):
    menu=[]
    keyList = adminMenuDict.keys()
    keyList.sort()
    for key in keyList:
        if page == adminMenuDict[key].link:
            adminMenuDict[key].active = True
        else:
            adminMenuDict[key].active = False
        menu.append(adminMenuDict[key])
    return menu


def makeUserLinks(request_uri):
    user = users.get_current_user()
    
    if user:
        user_name = user.nickname()
        url = users.create_logout_url(request_uri)
        url_linktext = 'Logout'
    else:
        user_name = 'anonymous'
        url = users.create_login_url(request_uri)
        url_linktext = 'Login'
    
    return {'url': url, 'url_linktext': url_linktext, 'user_name': user_name}
