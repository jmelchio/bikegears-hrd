#!/usr/bin/env python
# encoding: utf-8
"""
helpers.py

Created by Joris Melchior on 2008-06-21.
Copyright (c) 2008 Melchior I.T. Inc.. All rights reserved.
"""

from google.appengine.api import users

from google.appengine.ext import ndb

from model import Profile


class MenuEntry(object):
    """The MenuEntry class."""

    def __init__(self, link=None, name=None, active=None):
        self.link = link
        self.name = name
        self.active = active


menuDict = {1: MenuEntry('', 'Home', False),
            2: MenuEntry('user/rideroverview', 'Rider Overview', False),
            3: MenuEntry('user/rideentry', 'Ride Entry', False),
            4: MenuEntry('user/bikeoverview', 'Bike Overview', False),
            5: MenuEntry('user/bikeentry', 'Bike Entry', False)}

adminMenuDict = {2: MenuEntry('', 'Home', False),
                 1: MenuEntry('admin', 'Admin Home', False),
                 3: MenuEntry('admin/ridetypeentry', 'Ride Type Entry', False),
                 4: MenuEntry('admin/biketypeentry', 'Bike Type Entry', False)}


def make_menu(page=None):
    menu = []
    key_list = menuDict.keys()
    key_list.sort()
    for key in key_list:
        if page == menuDict[key].link:
            menuDict[key].active = True
        else:
            menuDict[key].active = False
        menu.append(menuDict[key])
    return menu


def make_admin_menu(page=None):
    menu = []
    key_list = adminMenuDict.keys()
    key_list.sort()
    for key in key_list:
        if page == adminMenuDict[key].link:
            adminMenuDict[key].active = True
        else:
            adminMenuDict[key].active = False
        menu.append(adminMenuDict[key])
    return menu


def make_user_links(request_uri):
    profile = get_profile()

    if profile:
        user_name = profile.nickName
        url = users.create_logout_url(request_uri)
        url_linktext = 'Logout'
    else:
        user_name = 'anonymous'
        url = users.create_login_url(request_uri)
        url_linktext = 'Login'

    return {'url': url, 'url_linktext': url_linktext, 'user_name': user_name}


def get_profile():
    user = users.get_current_user()

    if user:
        user_id = user.user_id()
        p_key = ndb.Key(Profile, user_id)
        profile = p_key.get()
        # create a Profile if not found
        if not profile:
            profile = Profile(key=p_key, nickName=user.nickname(), eMail=user.email(), )
            profile.put()

        return profile
    else:
        return None

# That's All Folks !!
