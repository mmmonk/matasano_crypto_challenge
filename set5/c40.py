#!/usr/bin/python

from c39 import RSA # rsa

if __name__ == "__main__":
  cleartext  = "this is just a test of a message that will be encrypted using RSA private/public key cryptography"
  pub1,priv1 = RSA().keygen(l=2048,s=False) # s=False gives e=3
  ct1 = RSA().encrypt(cleartext,pub1)
  pub2,priv2 = RSA().keygen(l=2048,s=False) # s=False gives e=3
  ct2 = RSA().encrypt(cleartext,pub1)
  pub3,priv3 = RSA().keygen(l=2048,s=False) # s=False gives e=3
  ct3 = RSA().encrypt(cleartext,pub1)

  # https://en.wikipedia.org/wiki/Coppersmith%27s_Attack#H.C3.A5stad.27s_Broadcast_Attack

