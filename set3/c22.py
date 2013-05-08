#!/usr/bin/env python

import c21
import time
import random

def revrnd(x):

  x ^=  (x >> 18)
  x ^= ((x << 15) & 0xefc60000)

  cv = x
  x ^= ((x << 7 ) & 0x9d2c5680)
  for i in range(64): # missing 6 bits
    tv = x ^ (((i & 32)<<26) + ((i & 16)<<24) + ((i & 8) <<23) + ((i & 4)<<19) + ((i & 2)<<18) + ((i & 1)<<14))
    if (tv ^ (tv << 7) & 0x9d2c5680) == cv:
      x = tv
      break

  cv = x
  x ^=  (x >> 11)
  for i in range(1024):
    tv = x ^ i
    if (tv ^ (tv >> 11)) == cv:
      x = tv
      break

  return x

def bins(i):
  return bin(i).replace("0b","").zfill(32)

#time.sleep(random.randint(40,1000))
ts = int(time.time())-random.randint(40,1000)

rng = c21.MT19937(ts)
(x,v) = rng.extract_number()

x1 = revrnd(v)
print str(x)+" "+str(x1)

print "rng : "+str(v)
print "seed: "+str(ts)

x1 = bins(x1)
x = bins(x)
out = ""
for i in range(32):
  if x[i] == x1[i]:
    out += "."
  else:
    out += "x"
print out
