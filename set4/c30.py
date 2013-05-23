#!/usr/bin/env python

import sys
import struct

def rol32(word,count):
  word = (word << count | word >> (32 - count)) & 0xFFFFFFFF
  return word

def padding(msglen):

  chunks = int((msglen+9)/64)
  missing_chunks = 64 - abs((chunks*64)-(msglen+9))

  pad = "\x80"
  for i in xrange(0,missing_chunks):
    pad += "\x00"
  pad += struct.pack('>Q',msglen*8)

  return pad


def f(x,y,z):
  return ((x&y) | ((~x)&z))

def g(x,y,z):
  return ((x&y) | (x&z) | (y&z))

def h(x.y.z):
  return (x ^ y ^ z)

def ff(a, b, c, d, x, s):
  return (a + f(b,c,d) + x ) << s

def gg(a, b, c, d, x, s):
  return (a + g(b,c,d) + x + 0x5A827999) << s

def hh(a, b, c, d, x, s):
  return (a + h(b,c,d) + x + 0x6ED9EBA1) << s


class md4:
  '''
  https://tools.ietf.org/html/rfc1320

  test vectors:
  MD4 ("") = 31d6cfe0d16ae931b73c59d7e0c089c0
  MD4 ("a") = bde52cb31de33e46245e05fbdbd6fb24
  MD4 ("abc") = a448017aaf21d8525fc10ae87aa6729d
  MD4 ("message digest") = d9130a8164549fe818874806e1c7014b
  MD4 ("abcdefghijklmnopqrstuvwxyz") = d79e1c308aa5bbcdeea8ed63df412da9
  MD4 ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") = 043f8582f241db351ce627e153e7f0e4
  MD4 ("12345678901234567890123456789012345678901234567890123456789012345678901234567890") = e33b4ddc9c38f2199c3e7b164fcc0536
  '''

  blocksize = 64

  def __init__(self,msg):

    self.A = 0x01234567
    self.B = 0x89abcdef
    self.C = 0xfedcba98
    self.D = 0x76543210
    self.msg = msg

  def extlen(self,orghash):

    hs = struct.unpack(">IIII",orghash.decode('hex'))

    self.A = hs[0]
    self.B = hs[1]
    self.C = hs[2]
    self.D = hs[3]

  def digest(self,imsg=""):

    msg = self.msg
    if imsg != "":
      msg = imsg

    msg += padding(len(msg))

    nchunk = 0
    for i in xrange(0,int(len(msg)/64)):
      X = list(struct.unpack('>IIIIIIIIIIIIIIII',msg[nchunk*64:(nchunk+1)*64]))

      a = self.A
      b = self.B
      c = self.C
      d = self.D

      FF (a, b, c, d, x[ 0], S11)
      FF (d, a, b, c, x[ 1], S12)
      FF (c, d, a, b, x[ 2], S13)
      FF (b, c, d, a, x[ 3], S14)
      FF (a, b, c, d, x[ 4], S11)
      FF (d, a, b, c, x[ 5], S12)
      FF (c, d, a, b, x[ 6], S13)
      FF (b, c, d, a, x[ 7], S14)
      FF (a, b, c, d, x[ 8], S11)
      FF (d, a, b, c, x[ 9], S12)
      FF (c, d, a, b, x[10], S13)
      FF (b, c, d, a, x[11], S14)
      FF (a, b, c, d, x[12], S11)
      FF (d, a, b, c, x[13], S12)
      FF (c, d, a, b, x[14], S13)
      FF (b, c, d, a, x[15], S14)

      GG (a, b, c, d, x[ 0], S21)
      GG (d, a, b, c, x[ 4], S22)
      GG (c, d, a, b, x[ 8], S23)
      GG (b, c, d, a, x[12], S24)
      GG (a, b, c, d, x[ 1], S21)
      GG (d, a, b, c, x[ 5], S22)
      GG (c, d, a, b, x[ 9], S23)
      GG (b, c, d, a, x[13], S24)
      GG (a, b, c, d, x[ 2], S21)
      GG (d, a, b, c, x[ 6], S22)
      GG (c, d, a, b, x[10], S23)
      GG (b, c, d, a, x[14], S24)
      GG (a, b, c, d, x[ 3], S21)
      GG (d, a, b, c, x[ 7], S22)
      GG (c, d, a, b, x[11], S23)
      GG (b, c, d, a, x[15], S24)

      HH (a, b, c, d, x[ 0], S31)
      HH (d, a, b, c, x[ 8], S32)
      HH (c, d, a, b, x[ 4], S33)
      HH (b, c, d, a, x[12], S34)
      HH (a, b, c, d, x[ 2], S31)
      HH (d, a, b, c, x[10], S32)
      HH (c, d, a, b, x[ 6], S33)
      HH (b, c, d, a, x[14], S34)
      HH (a, b, c, d, x[ 1], S31)
      HH (d, a, b, c, x[ 9], S32)
      HH (c, d, a, b, x[ 5], S33)
      HH (b, c, d, a, x[13], S34)
      HH (a, b, c, d, x[ 3], S31)
      HH (d, a, b, c, x[11], S32)
      HH (c, d, a, b, x[ 7], S33)
      HH (b, c, d, a, x[15], S34)


      self.A = (self.A + a) & 0xffffffff
      self.B = (self.B + b) & 0xffffffff
      self.C = (self.C + c) & 0xffffffff
      self.D = (self.D + d) & 0xffffffff

    return struct.pack('>IIIII',self.h0,self.h1,self.h2,self.h3,self.h4)

  def hexdigest(self,imsg=""):
    return self.digest(imsg).encode('hex')

if __name__ == "__main__":
  try:
    msg = sys.argv[1]
  except:
    msg = "some test text message"

  key = open("/dev/urandom").read(8).encode('hex')
  print md4(key+msg).hexdigest()+" "+key+msg
