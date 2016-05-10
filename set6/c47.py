#!/usr/bin/env python

# http://archiv.infsec.ethz.ch/education/fs08/secsem/Bleichenbacher98.pdf
# https://en.wikipedia.org/wiki/Adaptive_chosen-ciphertext_attack
# https://tools.ietf.org/html/rfc2313

from c39 import RSA
from c36 import i2s, s2i

class PKCS15t2:
  '''
  very ugly implementation of PKCS#1 1.5
  type 2
  '''

  def pad(self, msg, k):
    fflen = k - 3 - len(msg)
    assert (fflen > 0), "k to short"
    PS = open("/dev/urandom").read(fflen)
    while True:
      try:
        idx = PS.index("\x00")
      except ValueError:
        break
      PS[idx] = open("/dev/urandom").read(1)
    return "\x00\x02%s\x00%s" % ("\xff" * fflen, msg)

  def unpad(self, msg):
    if msg[0:2] == '\x00\x02':
      i = msg.find('\x00', 2)
      return msg[i+1:]
    return None

def oracle(key, c):
  """
  oracle function for c47
  """
  rsa = RSA()
  m = rsa.decrypt(c, key)
  if msg[0:2] == '\x00\x02':
    return True
  return False

if __name__ == "__main__":

  rsa = RSA()
  pkcs = PKCS15t2()

  # clear text message
  text = "kick it, CC"

  # key generation
  (pubkey, prvkey) = rsa.keygen(256)

  #padding PKCS#1 1.5
  m = pkcs.pad(text, len(i2s(pubkey[1])))

  # encrypting
  c = rsa.encrypt(m, pubkey)

  m1 = rsa.decrypt(c, prvkey)
  assert (m == "\x00"+m1), "PKCS#1 1.5 implementation failure"
  assert (text == pkcs.unpad("\x00"+m1)), "RSA implementation failure"


