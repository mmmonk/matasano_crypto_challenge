#!/usr/bin/env python

import c21
import time
import random

#time.sleep(random.randint(40,1000))
ts = int(time.time())

rng = c21.MT19937(ts)
v = rng.extract_number()

v ^=  (v >> 18)
v ^= ((v << 15) & 0xefc60000)
v ^= ((v << 7 ) & 0x9d2c5680)
v ^=  (v >> 11)

print "rng : "+str(v)
print "seed: "+str(ts)
