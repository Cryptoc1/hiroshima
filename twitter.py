#!/usr/bin/env python

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
    pincode = raw_input('Pincode? ')

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


def main():
    consumer_key = 'p0k5TwqEaNspElJkQCsD33Khn'
    consumer_secret = 'SNC9pak8wUZaafy95B7wFzjbKM8HeZF90GhBz8qeAWxXFtYOKw'
    tokens = get_access_token(consumer_key, consumer_secret)

    api = twitter.Api(consumer_key=consumer_key, 
            consumer_secret=consumer_secret,
            access_token_key=tokens['access_token'],
            access_token_secret=tokens['access_secret'])

    print api.VerifyCredentials()


if __name__ == "__main__":
    main()
