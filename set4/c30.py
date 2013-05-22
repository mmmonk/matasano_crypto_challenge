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

      AA = self.A
      BB = self.B
      CC = self.C
      DD = self.D

      for j in xrange(0,80):
        if j < 20:
          f = (b & c) | ((~ b) & d)
        elif j < 40:
          g = b ^ c ^ d
        elif j < 60:
          h = (b & c) | (b & d) | (c & d)

        temp = (rol32(a,5) + f + e + k + w[j]) & 0xffffffff
        e = d
        d = c
        c = rol32(b,30)
        b = a
        a = temp

      self.A = (self.h0 + a) & 0xffffffff
      self.B = (self.h1 + b) & 0xffffffff
      self.C = (self.h2 + c) & 0xffffffff
      self.D = (self.h3 + d) & 0xffffffff

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
