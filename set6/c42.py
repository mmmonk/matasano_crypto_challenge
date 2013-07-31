#!/usr/bin/env python

# http://www.imc.org/ietf-openpgp/mail-archive/msg06063.html
# https://tools.ietf.org/html/rfc3447

from c39 import RSA # RSA
from c36 import i2s, s2i
import math
import hashlib
from decimal import *

class PKCS15:
  '''
  very ugly implementation of PKCS 1.5
  '''

  def pad(self,msg,k):
    fflen = k - 20 - 13
    return "\x00\x01%s\x00%s" % ("\xff" * fflen, msg)

  def unpad(self,msg):
    if msg[0:2] == '\x00\x01':
      i = msg.find('\x00', 2)
      return msg[i+1:i+1+20] # we need to set the upper limit here
    return None

class RSAsign:

  def make(self,msg,key):
    pkcs15 = PKCS15()
    rsa = RSA()
    dgst = hashlib.sha1(message).digest()
    paddgst = pkcs15.pad(dgst,len(i2s(key[1])))
    return rsa.encrypt(paddgst,key)

  def verify(self,msg,sign,key):
    pkcs15 = PKCS15()
    rsa = RSA()
    dgst = hashlib.sha1(message).digest()
    return pkcs15.unpad("\x00"+rsa.decrypt(sign,key)) == dgst

def forging(mesg,key):

  e = key[0]
  n = key[1]

  if e != 3:
    raise Exception("e not equal 3")
  pkcs15 = PKCS15()
  dgst = hashlib.sha1(mesg).digest()
  keylen = len(i2s(n))

  getcontext().prec = keylen * 8

  # this is the valid beginning
  forge = "\x00\x01%s\x00%s" % ("\xff" * 8, dgst)
  # this will be garbge
  garbage = "\x00" * (keylen - 8 - len(dgst) - 13)
  whole = s2i(forge+garbage)
  cr = int(pow(whole,Decimal(1)/Decimal(3)))+1

  return i2s(cr)

if __name__ == "__main__":

  message = "hi mom"

  re = RSA()
  pub1,priv1 = re.keygen(l=512,s=False)

  rs = RSAsign()
  sign = rs.make(message,priv1)
  assert rs.verify(message,sign,pub1), "signature algo wrong"

  signf = [ forging(message,pub1) ]
  if rs.verify(message,signf,pub1):
    print "ok"
