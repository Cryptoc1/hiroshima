# Hiroshima
### What is Hiroshima?
Hiroshima is an all-in-one spammer program.

### What's being worked on right now
Hiroshima supports the following (checked means that the feature is active, and properly functing. Un-checked is in development, or being looked into):

- [ ] SMS Bombing
- [x] Instagram Likes
- [ ] ~~Instagram Comments~~<sup>1</sup>
- [ ] ~~Twitter Mentions/Send Tweet~~<sup>2</sup>
- [x] Twitter Favorite
- [x] Twitter Reply <sup>(This feature is **broken** and not included in the user flow, but exists in the code)</sup>
- [x] Twitter Retweet <sup>(beta)</sup>
- [ ] YouTube Likes
- [ ] YouTube Comments
- [ ] Kik messaging
- [ ] Snapchat
- [x] ask.fm queries

Have a suggestion? Open an issue!

<sup>1</sup>As of this commit, Instagram allows for only *approved* clients to comment on media.

<sup>2</sup>Twitter doesn't allow for two like tweets to be tweeted (throws duplication error)

### Screenshots
![screenshot](screens/start-screen.png) 
![screenshot](screens/help.png)
![screenshot](screens/delay.png)
![screenshot](screens/twitter.png)
![screenshot](screens/instagram.png)
![screenshot](screens/askfm.png)

Instagram video demo [here](https://www.youtube.com/watch?v=-xFVXAt4lMY)

Twitter video demo [here](https://youtu.be/oP5qb-41n8c)

### TODO
* Add arguments option?


### Dependencies:
* Mechanize
* tweepy
* python-instagram

Hiroshima has only been tested/designed for Mac OS X
