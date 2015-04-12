#!/usr/bin/env python
from instagram.client import InstagramAPI
import sys, os, pyperclip, time

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

# Fix Python 2.x.
try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass

client_id = 'd00446a61de44643bd0d1a21d78e0f5a'
client_secret = 'c742af13e3a04138bad288c50e005999'
redirect_uri = 'http://localhost/hiroshima/auth/insta'
raw_scope = 'basic likes'
scope = raw_scope.split(' ')
# For basic, API seems to need to be set explicitly
if not scope or scope == [""]:
    scope = ["basic"]

api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
redirect_uri = api.get_authorize_login_url(scope = scope)

def print_user_info(u):
    print "> id: " + u.id
    print "> username: " + u.username
    print "> full_name: " + u.full_name
    print "> profile_picture: " + u.profile_picture
    print "> bio: " + u.bio
    print "> website: " + u.website
    print "> counts: " + str(u.counts)

print "> Redirect URI copied to clipboard, paste it into your browser and copy/paste the ?code=<some number> back into this prompt."
pyperclip.copy(redirect_uri)

code = (str(input("> Paste in code in query string after redirect: ").strip()))

access_token = api.exchange_code_for_access_token(code)

print "> You've been authenticated, now it's just a matter of what to do next... I would say enter a username below"
uname = raw_input("> ")

a_api = InstagramAPI(access_token=access_token[0])
print "> Searching..."
res = a_api.user_search(q=uname, count=1)
print "Found something..."

user = a_api.user(res[0].id)

print_user_info(user)

print "Now what?"
cmd = raw_input("> ").upper()
delay = 5
if cmd == "LIKE ALL":
    print "Liking all photos. Due to rate-limits, this may take a while..."
    print "ETA: " + str(user.counts['media'] * delay) + " S"
    for media in a_api.user_recent_media(user_id=user.id, count=user.counts['media'])[0]:
        a_api.like_media(media.id)
        print "Photo Liked"
        time.sleep(delay)
elif cmd == "UNLIKE ALL":
    delay = int(raw_input("> "))
    print "Unliking all photos. Due to rate-limits, this may take a while..."
    print "ETA: " + str(user.counts['media'] * delay) + " S"
    for media in a_api.user_recent_media(user_id=user.id, count=user.counts['media'])[0]:
        a_api.unlike_media(media.id)
        print "Photo Unliked"
        time.sleep(delay)
else:
    print "Unrecognized command, exiting."
