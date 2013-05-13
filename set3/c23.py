#!/usr/bin/env python

import c21
import random

def revrnd(x): #{{{
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

  return x #}}}

if __name__ == "__main__":

  rng = c21.MT19937(random.randint(0,2**32))

  # create a list to which we will copy the state
  # and pull the original rng for 624 values
  copy_state = range(624)
  for i in range(624):
    copy_state[i] = revrnd(rng.extract_number())

  # create our own rng
  copy = c21.MT19937()

  # and change its state with the calculated values
  copy.set_state(list(copy_state))

  for i in range(30):
    print "original: "+str(rng.extract_number())
    print " \-copy : "+str(copy.extract_number())


'''
* How would you modify MT19937 to make this attack hard?

Make the output of the last function "extract_number()" none reversible, run it
through a secure hash (message digest function, even the simplest one here is
good enough).


* What would happen if you subjected each tempered output to a cryptographic hash?

It would prevent anybody from reversing the state (except for bruteforcing),
but the disadvantage would be that the process would be slower.
'''
