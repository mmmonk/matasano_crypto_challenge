#!/usr/bin/env python

from random import randint

from c43 import DSA
from c39 import invmod
from c33 import modexp

class DSA_45(DSA):

  def magic_sign(self, y, z = 20):
    # only if g == p+1
    assert (self.g == self.p+1), "only if g == p+1"
    r = modexp(y, z, self.p) % self.q
    s = r * invmod(z, self.q)
    return (r, s)

if __name__ == "__main__":
  d = DSA_45()

  # g == 0 - scenario
  d.g = 0
  # the below tests fails because for signing r = 0 is constantly generated
  #d.test()

  # g == p+1
  d.g = d.p+1
  d.test()

  (x, y) = d.genuserkey()
  print "key:\nx : %s\ny : %s" % (x, y)

  # "magic" signature - basically because g == p+1
  # then y == 1 and because of that r == 1
  # the point here is that you can generate a valid signature
  # in this case with *only* data that is needed for the verification
  # without actually seeing any message

  (r1, s1) = d.magic_sign(y, z = randint(1, 2**32))
  print "\nsign created without seeing any msg:\nr1: %s\ns1: %s" % (r1, s1)

  m = "Hello, world"
  (r, s) = d.sign(m, x)
  print "\nm : %s\nr : %s\ns : %s" % (m, r, s)
  d.verify(m, r1, s1, y)

  m = "Goodbye, world"
  (r, s) = d.sign(m, x)
  print "\nm : %s\nr : %s\ns : %s" % (m, r, s)
  d.verify(m, r1, s1, y)

  print "\n\"magic\" sign valid against both above and all other messages"+\
    " as long as the same keypair (x,y), q and p will be used"

