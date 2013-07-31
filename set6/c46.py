#!/usr/bin/env python

# http://secgroup.ext.dsi.unive.it/wp-content/uploads/2012/11/Practical-Padding-Oracle-Attacks-on-RSA.html#S3

from c39 import RSA # RSA
from c36 import i2s, s2i
import base64
import math
from decimal import *

class oracle:

  def __init__(self):
    self.rsa = RSA()
    self.pub,self.priv = self.rsa.keygen(l=512) # 1024 bits key

  def getpubkey(self):
    return self.pub

  def iseven(self,ct):
    return ord(self.rsa.decrypt(ct,self.priv)[-1]) & 1 == 0

def attack(enc,key,iseven):

  e = key[0]         # e - from the pub key
  n = key[1]         # n - from the pub key
  ct = s2i(enc[0])   # encrypted message
  c2 = pow(2,e,n)    # (2**e)%n)
  ct = (ct * c2) % n # we need to do this before we start counting
  limit = int(math.log(n,2))+1 # number of bits in the key
  getcontext().prec = limit # how precise our floats should be

  a = Decimal(0)
  b = Decimal(n)
  for x in range(limit):
    t = (a+b)/2
    if iseven([i2s(ct)]):
      b = t
    else:
      a = t
    ct = (ct * c2) % n

  return i2s(int(b)).encode('string_escape')

if __name__ == "__main__":

  txt = "VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ=="

  c46 = oracle()
  pub = c46.getpubkey()

  rsa = RSA()
  enc = rsa.encrypt(base64.b64decode(txt),pub)
  print attack(enc,pub,c46.iseven)
