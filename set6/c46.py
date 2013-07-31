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

  e = key[0]
  n = key[1]
  ct = s2i(enc[0]) # encrypted message
  c2 = pow(2,e,n) # (2**e)%n)
  limit = int(math.log(n,2))+1
  getcontext().prec = limit

  l = Decimal(0)
  u = Decimal(n)

  la = 0
  ua = 0
  for x in range(limit):
    t = (l+u)/2
    if iseven([i2s(ct)]):
      u = t
      ua += 1
    else:
      l = t
      la += 1
    ct = (ct * c2) % n

  print limit
  #print (l,u)
  print (la,ua)
  print i2s(int(l)).encode('string_escape')
  print i2s(int(u)).encode('string_escape')

if __name__ == "__main__":

  txt = "VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ=="

  c46 = oracle()
  pub = c46.getpubkey()

  rsa = RSA()
  enc = rsa.encrypt("this is just a test please ignore this message",pub)
  attack(enc,pub,c46.iseven)
