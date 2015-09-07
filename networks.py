#!/usr/bin/env python

##
#
# networks.py
# This file contains the classes for different social network attacks.
# Samuel Steele (cryptoc1)
#
##

import sys, os, time, webbrowser, ConfigParser
from instagram.client import InstagramAPI
import tweepy
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
    def __init__(self, delay=5):
        # Stuff for the attack
        self.delay = int(delay)
        self.victim = None

        # Stuff for the API
        self.client_id = 'd00446a61de44643bd0d1a21d78e0f5a'
        self.client_secret = 'c742af13e3a04138bad288c50e005999'
        self.redirect_uri = 'http://localhost/hiroshima/auth/insta'
        self.raw_scope = 'basic likes'
        self.scope = self.raw_scope.split(' ')
        # For basic, API seems to need to be set explicitly
        if not self.scope or self.scope == [""]:
            self.scope = ["basic"]
        self.api = InstagramAPI(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri)
        self.redirect_uri = self.api.get_authorize_login_url(scope=self.scope)
        if os.path.exists(os.path.expanduser("~/.config/hiroshima/hiroshima.cfg")):
            self.config = ConfigParser.ConfigParser()
            self.config.read(os.path.expanduser("~/.config/hiroshima/hiroshima.cfg"))
            self.access_token = self.config.get('insta', 'access_token')
            if self.access_token != "None":
                self.AUTH_IN_PREFS = True
            else:
                self.AUTH_IN_PREFS = False
        else:
            print "~/.config/hiroshima/hiroshima.cfg does not exist. Run install.sh or copy defautl.cfg to ~/.config/hiroshima/hiroshima.cfg"

    def login(self):
        if not self.AUTH_IN_PREFS:
            print "You will be redirected to an authorization page in your browser. Copy the code in the prompt and paste it below."
            webbrowser.open(self.redirect_uri)
            code = (str(input("code: ").strip()))
            self.access_token = self.api.exchange_code_for_access_token(code)
            if self.access_token != None:
                self.config.set('insta', 'access_token', str(self.access_token[0]))
                f = open(os.path.expanduser("~/.config/hiroshima/hiroshima.cfg"), 'wb')
                self.config.write(f)
                f.close()
                self.a_api = InstagramAPI(access_token=self.access_token[0])
                print "You're account has been authorized."
                return True
            else:
                return False
        else:
            self.a_api = InstagramAPI(access_token=self.access_token)
            print "You're account has been authorized."
            return True

    def set_victim(self, user):
        self.victim = self.a_api.user(user.id)
        if self.victim.username == "cryptoc1":
            print "Nice fucking try! bruh. ;)"
            return False
        if self.victim != None:
            return  True
        else:
            return False

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
        return "id: " + str(u.id) + "\nusername: " + str(u.username) + "\nfull_name: " + unicode(u.full_name).encode('utf-8', 'ignore') + "\nprofile_picture: " + str(u.profile_picture) + "\nbio: " + unicode(u.bio).encode('utf-8', 'ignore') + "\nwebsite: " + str(u.website) + "\ncounts: " + str(u.counts)

class Twitter:
    def __init__(self, delay=5):
        self.consumer_key = "ss9uxPWgFA5VIjZsSx5J0riHE"
        self.consumer_secret = "B2HFkfYtCIAvl2JebZky9G790ggeNUzDbcnVC6FpsRlIufcWUy"
        self.victim = None
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.redirect_uri = self.auth.get_authorization_url()
        self.delay = int(delay)
        if os.path.exists(os.path.expanduser("~/.config/hiroshima/hiroshima.cfg")):
            self.config = ConfigParser.ConfigParser()
            self.config.read(os.path.expanduser("~/.config/hiroshima/hiroshima.cfg"))
            self.tokens = {"key": self.config.get('twit', 'access_token'), "secret": self.config.get('twit', 'access_token_secret')}
            if self.tokens["key"] == "None" or self.tokens["secret"] == "None":
                self.AUTH_IN_PREFS = False
            else:
                self.AUTH_IN_PREFS = True
        else:
            print "~/.config/hiroshima/hiroshima.cfg does not exist. Run install.sh, or copy default.cfg to ~/.config/hiroshima/hiroshima.cfg."

    def login(self):
        if not self.AUTH_IN_PREFS:
            print "You will be redirected to an authorization page in your browser. Copy the code in the prompt and paste it below."
            webbrowser.open(self.redirect_uri)
            code = raw_input("code: ")
            self.auth.get_access_token(code)
            if self.auth.access_token:
                self.config.set('twit', 'access_token', str(self.auth.access_token))
                self.config.set('twit', 'access_token_secret', str(self.auth.access_token_secret))
                f = open(os.path.expanduser("~/.config/hiroshima/hiroshima.cfg"), 'wb')
                self.config.write(f)
                f.close()
                self.api = tweepy.API(self.auth)
                print "Your account has been authorized."
                return True
            else:
                return False
        else:
            self.auth.set_access_token(self.tokens["key"], self.tokens["secret"])
            if self.auth.access_token:
                self.api = tweepy.API(self.auth)
                print "You have been authorized."
                return True
            else:
                return False

    def set_victim(self, user):
        self.victim = self.api.get_user(user.id)
        if self.victim.screen_name == "cryptoc1":
            # Fuck you for trying ;)
            print "Nice fucking try, bruh! ;)"
            return False
        if self.victim != None:
            return True
        else:
            return False

    def search_users(self, username):
        return self.api.get_user(username)

    def fav_attack(self, count, include_rts=False, include_mentions=False):
        count = int(count)
        print "Favoriting " + str(count) + " tweets. Due to rate-limits, this may take a while..."
        print "Tweets expected to be favorited: " + str(count)
        eta = count * self.delay
        print self.format_eta(eta)
        for s in self.api.user_timeline(self.victim.id, count=count):
            if self.is_retweet(s):
                if include_rts:
                    if s.favorited:
                        print "Tweet with id: " + str(s.id) + " already favorited, skipping."
                    else:
                        self.api.create_favorite(s.id)
                        print "Tweet with id: " + str(s.id) + " favorited."
            elif self.is_mention(s):
                if "@" + self.api.me().screen_name in s.text:
                    if s.favorited:
                        print "Tweet with id: " + str(s.id) + " already favorited, skipping."
                    else:
                        self.api.create_favorite(s.id)
                        print "Tweet with id: " + str(s.id) + " that mentions you favorited."
                elif include_mentions:
                    if s.favorited:
                        print "Tweet with id: " + str(s.id) + " already favorited, skipping."
                    else:
                        self.api.create_favorite(s.id)
                        print "Tweet with id: " + str(s.id) + " favorited."
                else:
                    print "Tweet with id: " + str(s.id) + " is a mention, skipping."
            else:
                if s.favorited:
                    print "Tweet with id: " + str(s.id) + " already favorited, skipping."
                else:
                    self.api.create_favorite(s.id)
                    print "Tweet with id: " + str(s.id) + " favorited."
            time.sleep(self.delay)

    def reply_attack(self, text, count):
        count = int(count)
        print "Replying to " + str(count) + " tweets. Due to rate-limits, this may take a while..."
        print "Tweets expected to be replied to: " + str(count)
        eta = count * self.delay
        print self.format_eta(eta)
        for s in self.api.user_timeline(self.victim.id, count=count):
            self.api.update_status(text, in_reply_to_status_id=s.id)
            print "Tweet with id: " + str(s.id) + " replied to."
            time.sleep(self.delay)

    def rewtweet_attack(self, count, include_rts=False, include_mentions=False):
        count = int(count)
        print "Retweeting " + str(count) + " tweets. Due to rate-limits, this may take a while..."
        print "Tweets expected to be retweeted: " + str(count)
        eta = count * self.delay
        print self.format_eta(eta)
        for s in self.api.user_timeline(self.victim.id, count=count):
            if self.is_retweet(s):
                if s.retweeted_status.author.id == self.api.me().id:
                    print "Tweet with id: " + str(s.id) + " is owned by you, skipping."
                elif include_rts:
                    if s.retweeted:
                        print "Tweet with id: " + str(s.id) + " already retweeted, skipping."
                    else:
                        self.api.retweet(s.id)
                        print "Tweet with id: " + str(s.id) + " retweeted."
            elif self.is_mention(s):
                if "@" + self.api.me().screen_name in s.text:
                    if s.retweeted:
                        print "Tweet with id: " + str(s.id) + " already retweeted, skipping."
                    else:
                        self.api.retweet(s.id)
                        print "Tweet with id: " + str(s.id) + " that mentions you retweeted."
                elif include_mentions:
                    if s.retweeted:
                        print "Tweet with id: " + str(s.id) + " already retweeted, skipping."
                    else:
                        self.api.retweet(s.id)
                        print "Tweet with id: " + str(s.id) + " retweeted."
                else:
                    print "Tweet with id: " + str(s.id) + " is a mention, skipping."
            else:
                if s.retweeted:
                    print "Tweet with id: " + str(s.id) + " already retweeted, skipping."
                else:
                    self.api.retweet(s.id)
                    print "Tweet with id: " + str(s.id) + " retweeted."
            time.sleep(self.delay)

    def is_retweet(self, s):
        if "RT" in s.text:
            return True
        else:
            return False

    def is_mention(self, s):
        if "@" in s.text and " @ " not in s.text:
            return True
        else:
            return False

    def get_attack_types(self):
        return "favorite, retweet (beta)"

    def format_eta(self, eta):
        if eta > 60:
            return "ETA: " + str(eta / 60) + "M"
        else:
            return "ETA: " + str(eta) + "S"

    def format_user_info(self, u):
        return "id: " + str(u.id) + "\nscreen_name: " + str(u.screen_name) + "\nname: " + unicode(u.name).encode('utf-8', 'ignore') + "\nprofile_image_url: " + str(u.profile_image_url.replace("_normal", "")) + "\ndescription: " + unicode(u.description).encode('utf-8', 'ignore') + "\nwebsite: " + str(u.url)


class AskFM:
    def __init__(self, username, delay=5):
        self.username = username
        self.delay = delay

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
            return "ETA: " + str(eta) + "S"
