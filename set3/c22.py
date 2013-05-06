#!/usr/bin/env python

import c21
import time
import random

#time.sleep(random.randint(40,1000))
ts = int(time.time())-random.randint(40,1000)

rng = c21.MT19937(ts)
v = rng.extract_number()

print "rng : "+str(v)
print "seed: "+str(ts)

pseeds = list()
ts1 = int(time.time())
for x in range(ts1-3600,ts1):
  rng2 = c21.MT19937(x)
  if rng2.extract_number() == v:
    pseeds.append(x)

print pseeds

