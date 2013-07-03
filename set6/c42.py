#!/usr/bin/env python

# http://www.imc.org/ietf-openpgp/mail-archive/msg06063.html
# https://tools.ietf.org/html/rfc3447

from c39 import RSA # RSA
from c36 import i2s, s2i

import hashlib

class PKCS15:
  '''
  very ugly implementation of PKCS 1.5
  '''

  def pad(self,msg,k):
    mlen = len(msg)
    fflen = k - mlen - 3
    return "\x00\x02%s\x00%s" % ("\xff" * fflen, msg)

  def unpad(self,msg):
    if msg[0:2] == '\x00\x02':
      i = msg.find('\x00', 2)
      return msg[i+1:]
    return None

class RSAsign:

  def make(self,msg,key):
    pkcs15 = PKCS15()
    rsa = RSA()
    dgst = hashlib.md5(message).digest()
    paddgst = pkcs15.pad(dgst,len(i2s(key[1])))
    return rsa.encrypt(paddgst,key)

  def verify(self,msg,sign,key):
    pkcs15 = PKCS15()
    rsa = RSA()
    dgst = hashlib.md5(message).digest()
    if pkcs15.unpad("\x00"+rsa.decrypt(sign,key)) == dgst:
      return True
    else:
      return False

if __name__ == "__main__":

  message = "hi mom"

  re = RSA()
  pub1,priv1 = re.keygen(s=False)

  rs = RSAsign()
  sign = rs.make(message,priv1)
  print rs.verify(message,sign,pub1)
