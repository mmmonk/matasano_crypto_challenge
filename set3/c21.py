#!/usr/bin/env python

import time

class MT19937:
  '''
  based on the pseudocode from:
  https://en.wikipedia.org/wiki/Mersenne_twister#Pseudocode
  '''

  def __init__(self,seed=int(time.time())):
    '''
    if not given the seed is int(time.time())
    '''

    self.mt = list()
    self.idx = 0
    self.mt = range(0,624)
    self.mt[0] = seed
    for i in range(1,624):
      self.mt[i] = (0x6c078965 * ( self.mt[i-1] ^ (self.mt[i-1] >> 30)) + i) & 0xffffffff

  def generate_numbers(self):
    '''
    mixing function
    '''
    for i in range(0,624):
      y = (self.mt[i] & 0x80000000) + (self.mt[(i+1) % 624] & 0x7fffffff)
      self.mt[i] = self.mt[(i+397) % 624] ^ (y >> 1)
      if y % 2:
        self.mt[i] ^= 0x9908b0df

  def extract_number(self):
    '''
    the one that produces the actual results
    '''
    if self.idx == 0:
      self.generate_numbers()

    y = self.mt[self.idx]
    y ^= (y >> 11)
    y ^= ((y << 7)  & 0x9d2c5680)
    y ^= ((y << 15) & 0xefc60000)
    y ^= (y >> 18)

    self.idx = (self.idx + 1) % 624
    return y


if __name__ == "__main__":

  test = MT19937()
  for x in range(0,30):
    print test.extract_number()
