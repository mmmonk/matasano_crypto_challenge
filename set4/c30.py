#!/usr/bin/env python

import sys
import struct

def rol32(word,count):
    return (word << count | word >> (32 - count)) & 0xFFFFFFFF

def r1(a, b, c, d, x, s):
  f = ((b & c) | ((~b) & d))
  return rol32(( a + f + x )             & 0xFFFFFFFF,s)
def r2(a, b, c, d, x, s):
  f = ((b & c) | (b & d) | (c & d))
  return rol32(( a + f + x + 0x5A827999) & 0xFFFFFFFF,s)
def r3(a, b, c, d, x, s):
  f = b ^ c ^ d
  return rol32(( a + f + x + 0x6ED9EBA1) & 0xFFFFFFFF,s)

def padding(msglen):

  chunks = int((msglen+9)/64)
  missing_chunks = 64 - abs((chunks*64)-(msglen+9))

  pad = "\x80"
  for i in xrange(0,missing_chunks):
    pad += "\x00"
  pad += struct.pack('<Q',msglen*8)

  return pad

class md4:
  '''
  https://tools.ietf.org/html/rfc1320

  '''

  blocksize = 64

  def __init__(self,imsg=""):

    self.__setinit()
    self.msg = imsg

  def __setinit(self):

    self.A = 0x67452301
    self.B = 0xEFCDAB89
    self.C = 0x98BADCFE
    self.D = 0x10325476

  def extlen(self,orghash):

    hs = struct.unpack(">IIII",orghash.decode('hex'))

    self.A = hs[0]
    self.B = hs[1]
    self.C = hs[2]
    self.D = hs[3]

  def __transform(self,x):

    a = self.A
    b = self.B
    c = self.C
    d = self.D

    a = r1(a, b, c, d, x[ 0], 3)
    d = r1(d, a, b, c, x[ 1], 7)
    c = r1(c, d, a, b, x[ 2], 11)
    b = r1(b, c, d, a, x[ 3], 19)
    a = r1(a, b, c, d, x[ 4], 3)
    d = r1(d, a, b, c, x[ 5], 7)
    c = r1(c, d, a, b, x[ 6], 11)
    b = r1(b, c, d, a, x[ 7], 19)
    a = r1(a, b, c, d, x[ 8], 3)
    d = r1(d, a, b, c, x[ 9], 7)
    c = r1(c, d, a, b, x[10], 11)
    b = r1(b, c, d, a, x[11], 19)
    a = r1(a, b, c, d, x[12], 3)
    d = r1(d, a, b, c, x[13], 7)
    c = r1(c, d, a, b, x[14], 11)
    b = r1(b, c, d, a, x[15], 19)

    a = r2(a, b, c, d, x[ 0], 3)
    d = r2(d, a, b, c, x[ 4], 5)
    c = r2(c, d, a, b, x[ 8], 9)
    b = r2(b, c, d, a, x[12], 13)
    a = r2(a, b, c, d, x[ 1], 3)
    d = r2(d, a, b, c, x[ 5], 5)
    c = r2(c, d, a, b, x[ 9], 9)
    b = r2(b, c, d, a, x[13], 13)
    a = r2(a, b, c, d, x[ 2], 3)
    d = r2(d, a, b, c, x[ 6], 5)
    c = r2(c, d, a, b, x[10], 9)
    b = r2(b, c, d, a, x[14], 13)
    a = r2(a, b, c, d, x[ 3], 3)
    d = r2(d, a, b, c, x[ 7], 5)
    c = r2(c, d, a, b, x[11], 9)
    b = r2(b, c, d, a, x[15], 13)

    a = r3(a, b, c, d, x[ 0], 3)
    d = r3(d, a, b, c, x[ 8], 9)
    c = r3(c, d, a, b, x[ 4], 11)
    b = r3(b, c, d, a, x[12], 15)
    a = r3(a, b, c, d, x[ 2], 3)
    d = r3(d, a, b, c, x[10], 9)
    c = r3(c, d, a, b, x[ 6], 11)
    b = r3(b, c, d, a, x[14], 15)
    a = r3(a, b, c, d, x[ 1], 3)
    d = r3(d, a, b, c, x[ 9], 9)
    c = r3(c, d, a, b, x[ 5], 11)
    b = r3(b, c, d, a, x[13], 15)
    a = r3(a, b, c, d, x[ 3], 3)
    d = r3(d, a, b, c, x[11], 9)
    c = r3(c, d, a, b, x[ 7], 11)
    b = r3(b, c, d, a, x[15], 15)

    self.A = (self.A + a) & 0xFFFFFFFF
    self.B = (self.B + b) & 0xFFFFFFFF
    self.C = (self.C + c) & 0xFFFFFFFF
    self.D = (self.D + d) & 0xFFFFFFFF

  def digest(self,imsg=""):

    msg = self.msg
    if imsg != "":
      msg = imsg

    msg += padding(len(msg))

    for i in range(0,len(msg)/64):
      self.__transform(list(struct.unpack('<IIIIIIIIIIIIIIII',msg[i*64:(i+1)*64])))

    out = struct.pack('<IIII',self.A,self.B,self.C,self.D)
    self.__setinit()
    return out

  def hexdigest(self,imsg=""):
    return self.digest(imsg).encode('hex')

  def test(self):
    '''
    test vectors
    '''
    test_vectors = {
        "": "31d6cfe0d16ae931b73c59d7e0c089c0",
        "a": "bde52cb31de33e46245e05fbdbd6fb24",
        "abc": "a448017aaf21d8525fc10ae87aa6729d",
        "message digest":  "d9130a8164549fe818874806e1c7014b",
        "abcdefghijklmnopqrstuvwxyz": "d79e1c308aa5bbcdeea8ed63df412da9",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "043f8582f241db351ce627e153e7f0e4",
        "12345678901234567890123456789012345678901234567890123456789012345678901234567890": "e33b4ddc9c38f2199c3e7b164fcc0536",
        "The quick brown fox jumps over the lazy dog": "1bee69a46ba811185c194762abaeae90"}

    for tt in test_vectors:
      if self.hexdigest(tt) != test_vectors[tt]:
        print "\""+tt+"\" "+self.hexdigest(tt)+" should be "+test_vectors[tt]
        return False
    return True

if __name__ == "__main__":
  try:
    msg = sys.argv[1]
  except:
    msg = "some test text message"

  if not md4().test():
    print "tests failed"
  else:
    print "all tests OK"
    key = open("/dev/urandom").read(8).encode('hex')
    print md4(key+msg).hexdigest()+" "+key+msg
