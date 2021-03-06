#!/usr/bin/env python

import time

class MT19937:
  '''
  based on the pseudocode from:
  https://en.wikipedia.org/wiki/Mersenne_twister#Pseudocode

  more information on:
  http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/emt.html
  '''

  def __init__(self,seed=int(time.time()),size=624): #{{{
    '''
    if not given the seed is int(time.time())
    '''
    self.idx = 0
    self.size = size
    self.mt = range(0,self.size)
    self.mt[0] = seed & 0xffffffff
    for i in range(1,self.size):
      self.mt[i] = (0x6c078965 * ( self.mt[i-1] ^ (self.mt[i-1] >> 30)) + i) & 0xffffffff #}}}

  def set_state(self,mt,idx=0): #{{{
    '''
    function to overwrite the internal state table
    '''
    assert type(mt) is list and len(mt) == self.size, "mt is a wrong list value"
    self.mt  = mt
    self.idx = idx #}}}

  def get_state(self): #{{{
    print self.mt #}}}

  def generate_numbers(self): #{{{
    '''
    mixing function
    '''
    for i in range(0,self.size):
      y = (self.mt[i] & 0x80000000) + (self.mt[(i+1) % self.size] & 0x7fffffff)
      self.mt[i] = self.mt[(i+397) % self.size] ^ (y >> 1)
      if y % 2:
        self.mt[i] ^= 0x9908b0df #}}}

  def extract_number(self): #{{{
    '''
    the one that produces the actual results
    '''
    if self.idx == 0:
      self.generate_numbers()

    y  = self.mt[self.idx]
    y ^=  (y >> 11)
    y ^= ((y << 7 ) & 0x9d2c5680)
    y ^= ((y << 15) & 0xefc60000)
    y ^=  (y >> 18)

    self.idx = (self.idx + 1) % self.size

    return y #}}}

if __name__ == "__main__":

  test = MT19937(0)
  for i in range(10):
    print test.extract_number()
