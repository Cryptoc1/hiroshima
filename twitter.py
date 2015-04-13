#!/usr/bin/env python

# Shitty code, deal with it. (atleast it's better than Instagram.py)

import twitter
from requests_oauthlib import OAuth1Session
import webbrowser, os, sys, time

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'


def get_access_token(consumer_key, consumer_secret):
    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret)

    print 'Requesting temp token from Twitter'

    try:
        resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)
    except ValueError, e:
        print 'Invalid respond from Twitter requesting temp token: %s' % e
        return
    url = oauth_client.authorization_url(AUTHORIZATION_URL)

    print ''
    print 'I will try to start a browser to visit the following Twitter page'
    print 'if a browser will not start, copy the URL to your browser'
    print 'and retrieve the pincode to be used'
    print 'in the next step to obtaining an Authentication Token:'
    print ''
    print url
    print ''

    webbrowser.open(url)
    print "Enter code prompted after leaving twitter."
    pincode = raw_input("> ")

    print ''
    print 'Generating and signing request for an access token'
    print ''

    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                 resource_owner_key=resp.get('oauth_token'),
                                 resource_owner_secret=resp.get('oauth_token_secret'),
                                 verifier=pincode
    )
    try:
        resp = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)
    except ValueError, e:
        print 'Invalid respond from Twitter requesting access token: %s' % e
        return

    # print 'Your Twitter Access Token key: %s' % resp.get('oauth_token')
    # print '          Access Token secret: %s' % resp.get('oauth_token_secret')
    print "Authenticated"
    return {'access_token': resp.get('oauth_token'), 'access_secret': resp.get('oauth_token_secret')}

def get_attack_type():
    print "How should we attack? (fav, or mention)"
    return raw_input("> ").upper()

def get_user():
    print "Enter the username of who you'd like to attack."
    return raw_input("> ")

def init_attack(api):
    user = get_user()
    attack_type = get_attack_type()
    if attack_type == "FAV":
        fav_attack(api=api, u=user)
    elif attack_type == "MENTION":
        mention_attack(api=api, u=user)
    else:
        print "Unknown input."
        init_attack(api)

def fav_attack(api, u):
    print "How many tweets should be fetched/favorited? (Must be an integer less than 200)"
    twlt = raw_input("> ")
    tl = api.GetUserTimeline(screen_name=u, count=twlt, include_rts=True)
    for s in tl:
        if not s.favorited:
            api.CreateFavorite(s)
            print "Favorited a tweet by @" + u
        else:
            print "Tweet already favorited, skipping..."
    time.sleep(2.5)

def mention_attack(api, u):
    print "Enter the tweet's text"
    txt = raw_input("> ")
    txt = "@" + u + " " + txt
    char_count = 0
    for char in txt:
        char_count = char_count + 1
    if char_count > 140:
        print "Tweet is too long (140 character limit, remember?) Aborting attack."
        init_attack(api)
    print "How many mentions? (Must be integer)"
    repeat = int(raw_input("> "))
    print "About to tweet \"" + txt + "\" " + str(repeat) + "number of times."
    print "Press Enter to confirm, or CTRL + C to cancel:"
    if raw_input("> ") == "":
        n = 0
        while n < repeat:
            api.PostUpdate(txt)
            print "Tweet posted"
            n = n + 1
            time.sleep(2.5)

def main():
    consumer_key = 'p0k5TwqEaNspElJkQCsD33Khn'
    consumer_secret = sys.argv[1]
    tokens = get_access_token(consumer_key, consumer_secret)

    init_attack(twitter.Api(consumer_key=consumer_key, 
            consumer_secret=consumer_secret,
            access_token_key=tokens['access_token'],
            access_token_secret=tokens['access_secret']))

if __name__ == "__main__":
    main()
