#!/usr/bin/env python

import c21
import time
import random

time.sleep(random.randint(40,1000))
ts = int(time.time())

rng = c21.MT19937(ts)
v = rng.extract_number()

ts1 = int(time.time())
for i in range(2000):
  rng1 = c21.MT19937(ts1-i)
  if rng1.extract_number() == v:
    ts1 = ts1 - i
    break

print "original seed : "+str(ts)
print " guessed seed : "+str(ts1)
