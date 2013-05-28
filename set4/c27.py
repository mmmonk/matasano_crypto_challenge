#!/usr/bin/env python

import c16
import sys

class c27:

  def __init__(self):
    self.key = open("/dev/urandom").read(16)
    self.iv = self.key
    self.prefix = "comment1=cooking%20MCs;userdata="
    self.suffix = ";comment2=%20like%20a%20pound%20of%20bacon"

  def myinput(self,s):
    s = s.replace(";","\;").replace("=","\=")

    return c16.cbcencrypt(self.prefix+s+self.suffix,self.iv,self.key)

  def check(self,s):
    txt = c16.cbcdecrypt(s,self.iv,self.key)
    for c in txt:
      if ord(c) > 126 or ord(c) < 32:
        raise Exception(txt)
    return True

if __name__ == "__main__":

  t = c27()
  enc = list(t.myinput(""))
  test = "".join(enc[:16]+["\x00"]*16+enc[:16]+enc[16:])

  dec = ""
  try:
    out = t.check(test)
    print "no exception, try one more time"
    sys.exit(1)
  except Exception, e:
    dec = str(e)

  key = [chr(ord(c1)^ord(c2)) for c1,c2 in zip(dec[:16],dec[32:48])]

  txt = c16.cbcdecrypt("".join(enc),"".join(key),"".join(key))
  print txt.encode('string_escape')
