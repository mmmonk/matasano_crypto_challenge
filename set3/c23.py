#!/usr/bin/env python

import c21
import random

def revrnd(x):
  '''
  this function reverses the "extract_number" function from:
  https://en.wikipedia.org/wiki/Mersenne_twister#Pseudocode
  '''
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


rng = c21.MT19937(random.randint(0,2**32))

# create a list to which we will copy the state
# and pull the original rng for 624 values
copy_state = range(624)
for i in range(624):
  copy_state[i] = revrnd(rng.extract_number())

# create our own rng
copy = c21.MT19937()
# and change it state with the predicted values
copy.set_state(list(copy_state))

for i in range(30):
  print "original: "+str(rng.extract_number())
  print " \-copy : "+str(copy.extract_number())
