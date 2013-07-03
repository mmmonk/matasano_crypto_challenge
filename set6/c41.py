#!/usr/bin/env python

from c39 import RSA # RSA
from c36 import i2s, s2i

if __name__ == "__main__":

  msg = "attack after breakfest"

  rsa = RSA()
  pub,priv = rsa.keygen()
  C = rsa.encrypt(msg,pub)
  assert rsa.decrypt(C,priv) == msg, "bug in my RSA"

  S = 3
  C1 = list()
  C1.append(i2s((pow(S,pub[0],pub[1])*s2i(C[0])) % pub[1]))
  if C1[0] != C[0]:
    P1 = rsa.decrypt(C1,priv)
    print i2s((s2i(P1)/S)%pub[1])
  else:
    print "something wrong C1 and C should be different"
