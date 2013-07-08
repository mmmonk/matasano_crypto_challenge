#!/usr/bin/env python

# https://en.wikipedia.org/wiki/Digital_Signature_Algorithm

import Crypto.Util.number

class DSA:

  def __init__(self,L = 3072, N = 256):
    q = Crypto.Util.number.getPrime(N)
    p =
    g =


