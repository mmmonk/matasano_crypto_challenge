#!/usr/bin/python

from c39 import RSA, invmod
from c36 import i2s, s2i
import math

if __name__ == "__main__":
  cleartext  = "a"
  pub0,priv0 = RSA().keygen(l=2048,s=False) # s=False gives e=3
  ct0 = RSA().encrypt(cleartext,pub0)
  pub1,priv1 = RSA().keygen(l=2048,s=False) # s=False gives e=3
  ct1 = RSA().encrypt(cleartext,pub1)
  pub2,priv2 = RSA().keygen(l=2048,s=False) # s=False gives e=3
  ct2 = RSA().encrypt(cleartext,pub2)

  # https://en.wikipedia.org/wiki/Coppersmith%27s_Attack#H.C3.A5stad.27s_Broadcast_Attack
  # https://en.wikipedia.org/wiki/Chinese_remainder_theorem

  c_0 = s2i(ct0)
  c_1 = s2i(ct1)
  c_2 = s2i(ct2)
  n_0 = pub0[1]
  n_1 = pub1[1]
  n_2 = pub2[1]
  m_s_0 = pub0[0]
  m_s_1 = pub1[0]
  m_s_2 = pub2[0]

  result  = (c_0 * m_s_0 * invmod(m_s_0, n_0))
  result += (c_1 * m_s_1 * invmod(m_s_1, n_1))
  result += (c_2 * m_s_2 * invmod(m_s_2, n_2))

  result = pow(result,1/3.0)

  print i2s(result)
