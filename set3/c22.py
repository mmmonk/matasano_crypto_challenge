#!/usr/bin/env python

import c21
import time
import random

print "sleeping random time twice, this may take a while"
time.sleep(random.randint(40,1000))
ts = int(time.time())
time.sleep(random.randint(40,3600))

rng = c21.MT19937(ts)
v = rng.extract_number()

# get the current timestamp

ts1 = int(time.time())
print "current timestamp: "+str(ts1)

'''
The actual search could be optimized a bit we can assume that if somebody used
the current time then either the localtime or UTC was used and also that
probably that the server is using NTP.  This should narrow the amount of
searching that needs to be done.
'''

# this scans from the last 24hrs backwards to find the correct seed
for i in range(86400):
  rng1 = c21.MT19937(ts1-i) # substracting from current timestamp
  if rng1.extract_number() == v:
    ts1 = ts1 - i
    break

print "original seed   : "+str(ts)
print " guessed seed   : "+str(ts1)
