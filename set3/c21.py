#!/usr/bin/env python

# https://en.wikipedia.org/wiki/Mersenne_twister#Pseudocode

class MT19937:

  def __init__(self,seed):
    self.mt = list()
    self.mt.append(seed)
    for i in range(1,624):
      self.mt.append()
