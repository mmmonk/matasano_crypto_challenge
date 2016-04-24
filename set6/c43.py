#!/usr/bin/env python

# https://en.wikipedia.org/wiki/Digital_Signature_Algorithm

import Crypto.Util.number
import hashlib

from c39 import invmod
from c36 import i2s, s2i
from c33 import modexp

from decimal import Decimal, setcontext, ExtendedContext
setcontext(ExtendedContext)

import random # <- this is probably not good

class DSA:

  def __init__(self):
    # https://en.wikipedia.org/wiki/Digital_Signature_Algorithm#Parameter_generation
    self.p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
    self.q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
    self.g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291

  def genuserkey(self):
    # https://en.wikipedia.org/wiki/Digital_Signature_Algorithm#Per-user_keys
    x = random.randint(0, self.q)
    y = modexp(self.g, x, self.p)
    return (x, y)

  def sign(self, m, x, dgst=hashlib.sha1):
    (r, s, k) = signk(self, m, x, dgst=hashlib.sha1)
    return (r, s)

  def signk(self, m, x, dgst=hashlib.sha1):
    # signing with a leak of the k value
    # m - message
    # x - private key
    # https://en.wikipedia.org/wiki/Digital_Signature_Algorithm#Signing
    k = random.randint(0, self.q)
    r = 0
    while r == 0:
      r = modexp(self.g, k, self.p) % self.q
    s = (invmod(k, self.q) * (s2i(dgst(m).digest())+(x*r))) % self.q

    return (r, s, k)

  def verify(self, m, r, s, y, dgst=hashlib.sha1):
    # signature verification
    # https://en.wikipedia.org/wiki/Digital_Signature_Algorithm#Verifying
    assert (r > 0 and r < self.q), "wrong r: 0 < r < q"
    assert (s > 0 and s < self.q), "wrong s: 0 < s < q"
    w = invmod(s, self.q)
    u1 = (s2i(dgst(m).digest())*w) % self.q
    u2 = (r*w) % self.q
    v = ((modexp(self.g, u1, self.p)*modexp(y, u2, self.p)) % self.p )% self.q
    assert (v == r), "verification failed, v != r"
    return True

  def x_recovery(self, m, r, s, k, x, dgst=hashlib.sha1):
    # recovering x knowing k
    # m - message
    # r,s - public signature
    # k - this should be secret

    top = (s*k)-s2i(dgst(m).digest())

    a1 = top % self.q
    a2 = (x*r) % self.q

    if a1 == a2:
      print "match"

    print a1//(r % self.q)
    print (top/r) % self.q
    x = (top//r) % self.q
    print x
    return x

if __name__ == "__main__":
  d = DSA()
  m = "this is the test text for the DSA function"
  (x, y) = d.genuserkey()
  (r, s, k) = d.signk(m, x)
  d.verify(m, r, s, y)
  if x == d.x_recovery(m, r, s, k, x):
    print "ok"
  else:
    print "bad"
  print x
