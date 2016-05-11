#!/usr/bin/env python

# http://archiv.infsec.ethz.ch/education/fs08/secsem/Bleichenbacher98.pdf
# https://en.wikipedia.org/wiki/Adaptive_chosen-ciphertext_attack
# https://tools.ietf.org/html/rfc2313

from c39 import RSA
from c36 import i2s, s2i
from c39 import invmod
from c33 import modexp

import sys

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
      PS.replace("\x00", open("/dev/urandom").read(1), 1)
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
  try:
    m = rsa.decrypt(c, key)
  except:
    return False

  if m[0:2] == '\x00\x02':
    return True
  return False

def b_step2a (pubkey, prvkey, c, oracle):
  """
  Bleichenbacher step 2a
  """
  e = pubkey[0]
  n = pubkey[1]

  c = s2i("".join(c))
  c0 = (c * modexp(1, e, n)) % n

  s1 = n // 0x3B
  count = 0
  while True:
    c1 = (c0 * modexp(s1, e, n)) % n
    if oracle(prvkey, list(i2s(c1))):
      break
    s1 += 1
    if count % 10 == 0:
      sys.stdout.write("%s   \r" % (count))
      sys.stdout.flush()
    count += 1

  return s1

if __name__ == "__main__":

  rsa = RSA()
  pkcs = PKCS15t2()

  # clear text message
  text = "kick it, CC"

  # 256 bit key generation
  (pubkey, prvkey) = rsa.keygen(256)

  # padding PKCS#1 1.5
  m = pkcs.pad(text, len(i2s(pubkey[1])))

  # encrypting
  c = rsa.encrypt(m, pubkey)

  m1 = rsa.decrypt(c, prvkey)
  assert (m == "\x00"+m1), "PKCS#1 1.5 implementation failure"
  assert (text == pkcs.unpad("\x00"+m1)), "RSA implementation failure"

  # Bleichenbacher
  print b_step2a(pubkey, prvkey, c, oracle)
