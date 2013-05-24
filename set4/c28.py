#!/usr/bin/env python

import sys
import struct


def rol32(word,count):
  return (word << count | word >> (32 - count)) & 0xFFFFFFFF

def padding(msglen):

  chunks = int((msglen+9)/64)
  missing_chunks = 64 - abs((chunks*64)-(msglen+9))

  pad = "\x80"
  for i in xrange(0,missing_chunks):
    pad += "\x00"
  pad += struct.pack('>Q',msglen*8)

  return pad

class sha1:
  '''
  https://en.wikipedia.org/wiki/SHA-1
  http://www.ietf.org/rfc/rfc3174.txt
  '''

  blocksize = 64

  def __init__(self,imsg=""):

    self.__setinit()
    self.mesg = imsg
    self.lmsg = len(imsg)

  def __setinit(self):

    self.h0 = 0x67452301
    self.h1 = 0xEFCDAB89
    self.h2 = 0x98BADCFE
    self.h3 = 0x10325476
    self.h4 = 0xC3D2E1F0

  def __transform(self,w):

    for j in range(16,80):
      w.append(rol32(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16],1))

    a = self.h0
    b = self.h1
    c = self.h2
    d = self.h3
    e = self.h4

    for j in range(0,80):
      if j < 20:
        f = (b & c) | ((~ b) & d)
        k = 0x5A827999
      elif j < 40:
        f = b ^ c ^ d
        k = 0x6ED9EBA1
      elif j < 60:
        f = (b & c) | (b & d) | (c & d)
        k = 0x8F1BBCDC
      else:
        f = b ^ c ^ d
        k = 0xCA62C1D6

      temp = (rol32(a,5) + f + e + k + w[j]) & 0xFFFFFFFF
      e = d
      d = c
      c = rol32(b,30)
      b = a
      a = temp

    self.h0 = (self.h0 + a) & 0xFFFFFFFF
    self.h1 = (self.h1 + b) & 0xFFFFFFFF
    self.h2 = (self.h2 + c) & 0xFFFFFFFF
    self.h3 = (self.h3 + d) & 0xFFFFFFFF
    self.h4 = (self.h4 + e) & 0xFFFFFFFF

  def digest(self,imsg=""):

    msg = self.mesg
    lmsg = self.lmsg
    if imsg != "":
      msg = imsg
      lmsg = len(imsg)

    msg += padding(lmsg)

    for i in range(0,len(msg)/64):
      self.__transform(list(struct.unpack('>IIIIIIIIIIIIIIII',msg[i*64:(i+1)*64])))

    out = struct.pack('>IIIII',self.h0,self.h1,self.h2,self.h3,self.h4)
    self.__setinit()
    return out

  def hexdigest(self,imsg=""):
    return self.digest(imsg).encode('hex')

  def test(self):
    '''
    test vectors
    '''

    test_vectors = {
      "": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
      "a": "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8",
      "abc": "a9993e364706816aba3e25717850c26c9cd0d89d",
      "message digest": "c12252ceda8be8994d5fa0290a47231c1d16aae3",
      "abcdefghijklmnopqrstuvwxyz": "32d10c7b8cf96570ca04ce37f2a19d84240d3a89",
      "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "761c457bf73b14d27e9e9265c46f4b4dda11f940",
      "12345678901234567890123456789012345678901234567890123456789012345678901234567890": "50abf5706a150990a08b2c5ea40fa0e585554732",
      "The quick brown fox jumps over the lazy dog": "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12"}

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

  if not sha1().test():
    print "NOT OK"
  else:
    key = "da39a3ee5e6"
    print sha1(key+msg).hexdigest()+" => "+key+msg
