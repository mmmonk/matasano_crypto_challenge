#!/usr/bin/env python

import c10
import random
import base64

class cc17:

  def __init__(self,blksize=16):
    self.blksize = blksize
    self.key = open("/dev/urandom").read(self.blksize)

  def fun1 (self):

    iv = open("/dev/urandom").read(self.blksize)

    msgs = "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=\n\
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=\n\
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==\n\
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==\n\
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl\n\
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==\n\
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==\n\
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=\n\
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=\n\
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"

    #return (iv,c10.cbcencrypt(random.choice(msgs.split("\n")),iv,self.key))
    return (iv,c10.cbcencrypt("marek",iv,self.key))

  def fun2(self,iv,s):

    try:
      c10.cbcdecrypt(s,iv,self.key)
      return True
    except:
      return False

if __name__ == "__main__":

  blksize = 16

  c17 = cc17(blksize)
  (iv,ct) = c17.fun1()

  ct = list(ct)

  ablk = ["\x00"] * blksize

  # first block
  for i in reversed(range(0,blksize)):
    pad = blksize-i
    print str(i)+" "+str(pad)
    if pad > 1:
      for j in range(i+1,blksize):
        ablk[j] = chr(ord(ablk[j])^(pad-1)^pad)

    for c in range(0,256):
      ablk[i] = chr(c)
      if c17.fun2(ablk,"".join(ct[:blksize])):
        print str(i)+" "+str(pad)+" "+str(c)
        break

  out = [ chr(ord(c)^16) for c in ablk ]
  print "".join(out).encode("string_escape")

  #print c17.fun2(a[0],a[1])
