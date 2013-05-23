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

class sha1:

  # https://en.wikipedia.org/wiki/SHA-1

  blocksize = 64

  def __init__(self,imsg=""):

    self.h0 = 0x67452301
    self.h1 = 0xEFCDAB89
    self.h2 = 0x98BADCFE
    self.h3 = 0x10325476
    self.h4 = 0xC3D2E1F0
    self.mesg = imsg
    self.omsg = ""
    self.omlen = 0

  def extlen(self,orghash,msglen):

    hs = struct.unpack(">IIIII",orghash.decode('hex'))

    self.h0 = hs[0]
    self.h1 = hs[1]
    self.h2 = hs[2]
    self.h3 = hs[3]
    self.h4 = hs[4]

    self.omsg = padding(msglen)
    self.omlen = msglen

  def digest(self,imsg=""):

    msg = imsg
    if imsg != "":
      msg = self.omsg + imsg

    msg += padding(self.omlen+len(msg))

    nchunk = 0
    for i in xrange(0,int(len(msg)/64)):
      chunk = msg[nchunk*64:(nchunk+1)*64]
      nchunk += 1
      w = list(struct.unpack('>IIIIIIIIIIIIIIII',chunk))
      for j in xrange(16,80):
        w.append(rol32(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16],1))

      a = self.h0
      b = self.h1
      c = self.h2
      d = self.h3
      e = self.h4

      for j in xrange(0,80):
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

        temp = (rol32(a,5) + f + e + k + w[j]) & 0xffffffff
        e = d
        d = c
        c = rol32(b,30)
        b = a
        a = temp

      self.h0 = (self.h0 + a) & 0xffffffff
      self.h1 = (self.h1 + b) & 0xffffffff
      self.h2 = (self.h2 + c) & 0xffffffff
      self.h3 = (self.h3 + d) & 0xffffffff
      self.h4 = (self.h4 + e) & 0xffffffff

    return struct.pack('>IIIII',self.h0,self.h1,self.h2,self.h3,self.h4)

  def hexdigest(self,imsg=""):
    return self.digest(imsg).encode('hex')

def SHA1test():
  '''
  test vectors
  '''
  if sha1().hexdigest("The quick brown fox jumps over the lazy dog") != "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12":
    print "1. not OK"
    return False
  if sha1().hexdigest("") != "da39a3ee5e6b4b0d3255bfef95601890afd80709":
    print "2. not OK"
    return False
  return True

if __name__ == "__main__":
  try:
    msg = sys.argv[1]
  except:
    msg = "some test text message"

  if not SHA1test():
    print "NOT OK"
  else:
    key = open("/dev/urandom").read(8).encode('hex')
    print sha1(key+msg).hexdigest()+" "+key+msg
