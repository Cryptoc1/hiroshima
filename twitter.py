#!/usr/bin/env python

import twitter
import os

api = twitter.Api()

statuses = api.GetUserTimeline('490733871')
print [s.text for s in statuses]
