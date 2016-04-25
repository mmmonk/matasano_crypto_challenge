#!/usr/bin/env python

# https://en.wikipedia.org/wiki/Digital_Signature_Algorithm

import hashlib

from c39 import invmod
from c36 import i2s, s2i
from c33 import modexp

from random import randint

class DSA:

  def __init__(self):
    # https://en.wikipedia.org/wiki/Digital_Signature_Algorithm#Parameter_generation
    self.p = long("800000000000000089e1855218a0e7dac38136ffafa72eda7"+\
     "859f2171e25e65eac698c1702578b07dc2a1076da241c76c6"+\
     "2d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebe"+\
     "ac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2"+\
     "b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc87"+\
     "1a584471bb1", 16)
    self.q = long("f4f47f05794b256174bba6e9b396a7707e563c5b", 16)
    self.g = long("5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119"+\
     "458fef538b8fa4046c8db53039db620c094c9fa077ef389b5"+\
     "322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a047"+\
     "0f5b64c36b625a097f1651fe775323556fe00b3608c887892"+\
     "878480e99041be601a62166ca6894bdd41a7054ec89f756ba"+\
     "9fc95302291", 16)

  def genuserkey(self):
    # https://en.wikipedia.org/wiki/Digital_Signature_Algorithm#Per-user_keys
    x = randint(0, self.q)
    return (x, self.y_gen(x))

  def y_gen(self, x):
    # y generator
    return modexp(self.g, x, self.p)

  def sign(self, m, x, dgst=hashlib.sha1):
    # signing without leaking k
    (r, s, k) = self.signk(m, x, dgst)
    return (r, s)

  def signk(self, m, x, dgst=hashlib.sha1):
    # signing with a leak of the k value
    # m - message
    # x - private key
    # https://en.wikipedia.org/wiki/Digital_Signature_Algorithm#Signing
    r = 0
    k = 0
    while r == 0:
      k = randint(0, self.q)
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

  def test(self):
    # testing if signing and verifying works
    m = "this is the test text for the DSA function"
    (x, y) = self.genuserkey()
    (r, s, k) = self.signk(m, x)
    self.verify(m, r, s, y)
    x1 = self.x_recovery(m, r, s, k)
    assert (x1 == x), "x_recovery failed"

  def x_recovery(self, m, r, s, k, dgst=hashlib.sha1):
    # recovering x knowing k
    # m - message
    # r,s - public signature
    # k - this should be secret (nounce)

    top = (s*k)-s2i(dgst(m).digest())
    return (top * invmod(r, self.q)) % self.q

if __name__ == "__main__":

  # initiate and test
  d = DSA()
  d.test()

  # challenge 43
  y = long("84ad4719d044495496a3201c8ff484feb45b962e7302e56a392aee4"+\
      "abab3e4bdebf2955b4736012f21a08084056b19bcd7fee56048e004"+\
      "e44984e2f411788efdc837a0d2e5abb7b555039fd243ac01f0fb2ed"+\
      "1dec568280ce678e931868d23eb095fde9d3779191b8c0299d6e07b"+\
      "bb283e6633451e535c45513b2d33c99ea17", 16)

  m = "For those that envy a MC it can be hazardous to your health\n"+\
    "So be friendly, a matter of life and death, just like a etch-a-sketch\n"

  r = 548099063082341131477253921760299949438196259240
  s = 857042759984254168557880549501802188789837994940

  msg_check_hash = "d2d0714f014a9784047eaeccf956520045c45265"
  assert (hashlib.sha1(m).hexdigest() == msg_check_hash), "hash doesn't match"

  h_expected = "0954edd5e0afe5542a4adf012611a91912a3ec16"
  # broken implementation k is between 0 and 2^16
  for k in range(0, 2**16):
    x = d.x_recovery(m, r, s, k)
    if hashlib.sha1(i2s(x).encode('hex')).hexdigest() == h_expected:
      (r1, s1) = d.sign(m, x)
      d.verify(m, r1, s1, y)
      print "k : %s" % (k)
      print "x : %s" % (x)
      break
