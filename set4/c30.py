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

class md4:
  '''
  https://tools.ietf.org/html/rfc1320
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

  def digest(self,msg=""):

    if msg == "":
      msg = self.msg

    msg += padding(len(msg))

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

  def hexdigest(self):
    return self.digest().encode('hex')

if __name__ == "__main__":
  try:
    msg = sys.argv[1]
  except:
    msg = "some test text message"

  key = open("/dev/urandom").read(8).encode('hex')
  print md4(key+msg).hexdigest()+" "+key+msg
