from instagram.client import InstagramAPI
import sys, os, pyperclip

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
redirect_uri = 'http://localhost:8515'
raw_scope = 'likes'
scope = raw_scope.split(' ')
# For basic, API seems to need to be set explicitly
if not scope or scope == [""]:
    scope = ["basic"]

api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
redirect_uri = api.get_authorize_login_url(scope = scope)

print("Redirect URI copied to clipboard, paste it into your browser and copy/paste the ?code=<some number> back into this prompt.")
pyperclip.copy(redirect_uri)

code = (str(input("Paste in code in query string after redirect: ").strip()))

access_token = api.exchange_code_for_access_token(code)

recent_media, next_ = api.user_recent_media(user_id=access_token[1]['id'], count=5)
for media in recent_media:
    print media.caption.text
