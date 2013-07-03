#!/usr/bin/env python

from c39 import RSA # RSA
from c36 import i2s, s2i

if __name__ == "__main__":

  msg = "attack after the breakfast"

  rsa = RSA()
  pub,priv = rsa.keygen()
  C = rsa.encrypt(msg,pub)
  assert rsa.decrypt(C,priv) == msg, "bug in my RSA, decryption didn't provide the same clear text"

  S = 3       # lowest possible S
  C1 = list() # the cipher text is a list
  for ct in C: # lets iterate over the ciphertext
    C1.append(i2s((pow(S,pub[0],pub[1])*s2i(ct)) % pub[1])) #

  if C1 != C: # the C1 has to be different the C
    P1 = rsa.decrypt(C1,priv)
    print i2s((s2i(P1)/S)%pub[1])
  else:
    print "something wrong C1 and C should be different"
