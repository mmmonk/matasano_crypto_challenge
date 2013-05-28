#!/usr/bin/env python

import c18

class c26:

  def __init__(self):
    self.n = int(open("/dev/urandom").read(8).encode('hex'),16)
    self.k = open("/dev/urandom").read(16)

  def myinput(self,s):
    s = s.replace(";","\;").replace("=","\=")
    prefix = "comment1=cooking%20MCs;userdata="
    suffix = ";comment2=%20like%20a%20pound%20of%20bacon"

    return c18.ctrencrypt(prefix+s+suffix,self.n,self.k)

  def checkadmin(self,s):
    if ";admin=true;" in c18.ctrdecrypt(s,self.n,self.k):
      return True
    return False

if __name__ == "__main__":

  txt = "abc;admin=true"
  t = c26()
  enc = t.myinput("a"*len(txt))
  key = [ ord(c)^ord("a") for c in enc[32:32+len(txt)] ]
  test = enc[:32]+"".join([chr(ord(c)^k) for c,k in zip(txt,key)])+enc[32+len(txt):]

  if t.checkadmin(test): # keeping fingers crossed
    print "we did good ;)"
  else:
    print ":("

