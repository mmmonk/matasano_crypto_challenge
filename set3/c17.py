#!/usr/bin/env python

import c10
import random
import base64

class cc17:

  def __init__(self):
    self.key = open("/dev/urandom").read(16)

  def fun1 (self):

    iv = open("/dev/urandom").read(16)

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

    return (iv,c10.cbcencrypt(random.choice(msgs.split("\n")),iv,self.key))

  def fun2(self,iv,s):

    try:
      c10.cbcdecrypt(s,iv,self.key)
      return True
    except:
      return False

if __name__ == "__main__":

  c17 = cc17()
  a = c17.fun1() # 0 - iv, 1 - encrypted msg
  print c17.fun2(a[0],a[1])
