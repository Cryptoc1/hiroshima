#!/usr/bin/env python

##
# 
# networks.py
# This file contains the classes for different social network attacks.
# Samuel Steele (cryptoc1)
#
##


import sys, os, time, webbrowser
from instagram.client import InstagramAPI
import mechanize

if len(sys.argv) > 1 and sys.argv[1] == 'local':
    try:
        from test_settings import *
    
        InstagramAPI.host = test_host
        InstagramAPI.base_path = test_base_path
        InstagramAPI.access_token_field = "access_token"
        InstagramAPI.authorize_url = test_authorize_url
        InstagramAPI.access_token_url = test_access_token_url
        InstagramAPI.protocol = test_protocol
    except Exception:
        pass
# Python 2.x
try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass
    
class Instagram:
    def __init__(self):
               # Stuff for the attack
        self.delay = 5
        self.victim = None

        # Stuff for the API
        self.client_id = 'd00446a61de44643bd0d1a21d78e0f5a'
        self.client_secret = 'c742af13e3a04138bad288c50e005999'
        self.access_token = None
        self.redirect_uri = 'http://localhost/hiroshima/auth/insta'
        self.raw_scope = 'basic likes'
        self.scope = self.raw_scope.split(' ')
        # For basic, API seems to need to be set explicitly
        if not self.scope or self.scope == [""]:
            self.scope = ["basic"]
        self.api = InstagramAPI(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri)
        self.redirect_uri = self.api.get_authorize_login_url(scope=self.scope)

    def login(self):
        print "You will be redirected to an authorization page in your browser. Copy the code in the prompt and paste it below."
        webbrowser.open(self.redirect_uri)
        code = (str(input("code: ").strip()))
        self.access_token = self.api.exchange_code_for_access_token(code)
        if self.access_token != None:
            self.a_api = InstagramAPI(access_token=self.access_token[0])
            print "You're account has been authorized."
            return True
        else:
            return False

    def set_victim(self, user):
        self.victim = self.a_api.user(user.id)
        if self.victim != None:
            return  True
        else:
            return False
        pass

    def search_users(self, uname):
        return self.a_api.user(self.a_api.user_search(q=uname, count=1)[0].id)

    def like_attack(self, count):
        if str(count).lower() == "all":
            print "Liking " + str(count) + " photos. Due to rate-limits, this may take a while..."
            print "Number of photos expected to be liked: " + str(self.victim.counts['media'])
            eta = self.victim.counts['media'] * self.delay
            print self.format_eta(eta)
            for media in self.a_api.user_recent_media(user_id=self.victim.id, count=self.victim.counts['media'])[0]:
                if media.user_has_liked:
                    print "Photo with id: " + str(media.id) + " already liked, skipping."
                else:
                    self.a_api.like_media(media.id)
                    print "Photo with id: " + str(media.id) + " liked."
                time.sleep(self.delay)
        else:
            count = int(count)
            print "Liking " + str(count) + " photos. Due to rate-limits, this may take a while..."
            print "Number of photos expected to be liked: " + str(count)
            eta = count * self.delay
            print self.format_eta(eta)
            for media in self.a_api.user_recent_media(user_id=self.victim.id, count=count)[0]:
                if media.user_has_liked:
                    print "Photo with id: " + str(media.id) + " already liked, skipping."
                else:
                    self.a_api.like_media(media.id)
                    print "Photo with id: " + str(media.id) + " liked."
                time.sleep(self.delay)

    def unlike_attack(self, count):
        if str(count).lower() == "all":
            print "Unliking " + str(count) + " photos. Due to rate-limits, this may take a while..."
            print "Number of photos expected to be unliked: " + str(self.victim.counts['media'])
            eta = self.victim.counts['media'] * self.delay
            print self.format_eta(eta)
            for media in self.a_api.user_recent_media(user_id=self.victim.id, count=self.victim.counts['media'])[0]:
                if media.user_has_liked:
                    self.a_api.unlike_media(media.id)
                    print "Photo with id: " + str(media.id) + " unliked."
                else:
                    print "Photo with id: " + str(media.id) + " already not liked, skipping."
                time.sleep(self.delay)
        else:
            count = int(count)
            print "Unliking " + str(count) + " photos. Due to rate-limits, this may take a while..."
            print "Number of photos expected to be unliked: " + str(count)
            eta = count * self.delay
            print self.format_eta(eta)
            for media in self.a_api.user_recent_media(user_id=self.victim.id, count=count)[0]:
                if media.user_has_liked:
                    self.a_api.unlike_media(media.id)
                    print "Photo with id: " + str(media.id) + " unliked."
                else:
                    print "Photo with id: " + str(media.id) + " already not liked, skipping."
                time.sleep(self.delay)


    def get_attack_types(self):
        return "like, unlike"

    def format_eta(self, eta):
        if eta > 60:
            return "ETA: " + str(eta / 60) + "M"
        else:
            return "ETA: " + str(eta) + "S"

    def format_user_info(self, u):
        return "id: " + u.id + "\nusername: " + u.username + "\nfull_name: " + u.full_name + "\nprofile_picture: " + u.profile_picture + "\nbio: " + u.bio + "\nwebsite: " + u.website + "\ncounts: " + str(u.counts)

class Twitter:
    def __init__(self, client_secret):
        pass

class AskFM:
    def __init__(self, username):
        self.username = username
        self.delay = 5

    def ask_question(self, q, count):
        n = 0
        eta = self.delay * int(count)
        print self.format_eta(eta)
        while n < int(count):
            br = mechanize.Browser()
            br.open("http://ask.fm/" + self.username)

            for form in br.forms():
                if form.attrs['id'] == "question_form":
                    br.form = form
                    break
            br.form['question[question_text]'] = q
            br.submit()
            n += 1
            print "Question submitted."
            time.sleep(self.delay)

    def format_eta(self, eta):
        if eta > 60:
            return "ETA: " + str(eta / 60) + "M"
        else:
            return "ETA: " + str(eta)
