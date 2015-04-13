# Installation Instructions for Hiroshima 

### Where to Start
The first thing that should be done is to run *install.py*. This script moves and setup some stuff for easier authentication.

### What next?
The next thing you'll need to do is setup clients with respective social networks, instructions are provided below:

Ask.fm: The ask.fm spammer doesn't use an API, it interacts with the web page, so it doesn't need any configurig in the sense of an API. It does, however, take advantage of the *Anonymous* feature, that being said, if the person you are attempting to spam doesn't allow anonymous question, you can't spam them.

Instagram: The Instagram script DOES require APIs to be configured. 
1. Go to [Instagram Client Manager](https://instagram.com/developer/clients/manage/)

2. Create a new client named Hiroshima (Make something up for the webite option) 
3. Under the *Redirect URI* option, enter *http://localhost/hiroshima/auth/insta* or *http://127.0.0.1/hiroshima/auth/insta*. Either of the two function the same. 4. Copy the *Client Id* and *Client Secret* into the *instagram.py* file. (The client tokens could also be passed as arguments, but support is iffy and tedious) 5. You should be set. 

Twitter: Setting up Twitter client is similar to Instgrams process. 1. Go to [Twitter App Manager](https://apps.twitter.com/) 2. Click on *Create New App* 3. Name it Hiroshima 4. Under description, you could enter the following: "Hiroshima is a multi-network spammer written in Python" 5. Under the *Callback URL* enter *http://127.0.0.1/hiroshima/auth/twitter* (using localhost will NOT work here) 6. Once created, go to the settings page and enter the *Keys and Access Tokens* tab 7. Ensure that the *Acces Level* is set to *Read and Write* 8. Copy the *Consumer Key* and *Consumer Secret* into the *twitter.py* file. (Again, the client tokens could be used as arguments, but support is iffy and tedious.) 9. You should be set.
