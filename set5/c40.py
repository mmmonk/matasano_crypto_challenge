#!/usr/bin/python

from c39 import RSA, invmod
from c36 import i2s, s2i
from decimal import *
setcontext(ExtendedContext)
getcontext().prec = 100

if __name__ == "__main__":

  cleartext  = "attack at dawn"

  print "0. key generation"
  pub0,priv0 = RSA().keygen(l=2048,s=False) # s=False gives e=3
  print "0. encrypting using pub key"
  ct0 = RSA().encrypt(cleartext,pub0)

  print "1. key generation"
  pub1,priv1 = RSA().keygen(l=2048,s=False) # s=False gives e=3
  print "1. encrypting using pub key"
  ct1 = RSA().encrypt(cleartext,pub1)

  print "2. key generation"
  pub2,priv2 = RSA().keygen(l=2048,s=False) # s=False gives e=3
  print "2. encrypting using pub key"
  ct2 = RSA().encrypt(cleartext,pub2)

  assert RSA().decrypt(ct0,priv0) == cleartext, "error on key0"
  assert RSA().decrypt(ct1,priv1) == cleartext, "error on key1"
  assert RSA().decrypt(ct2,priv2) == cleartext, "error on key2"

  # https://en.wikipedia.org/wiki/Coppersmith%27s_Attack#H.C3.A5stad.27s_Broadcast_Attack
  # https://en.wikipedia.org/wiki/Chinese_remainder_theorem

  c_0 = s2i(ct0[0])
  c_1 = s2i(ct1[0])
  c_2 = s2i(ct2[0])
  n_0 = pub0[1]
  n_1 = pub1[1]
  n_2 = pub2[1]
  m_s_0 = n_1 * n_2
  m_s_1 = n_0 * n_2
  m_s_2 = n_0 * n_1

  result  = (c_0 * m_s_0 * invmod(m_s_0, n_0))
  result += (c_1 * m_s_1 * invmod(m_s_1, n_1))
  result += (c_2 * m_s_2 * invmod(m_s_2, n_2))
  result %= (n_0 * n_1 * n_2)

  print i2s(int(pow(Decimal(result),Decimal(1)/Decimal(3)))+1)
