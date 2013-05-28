#!/usr/bin/env python

import urllib
import c18
import base64


class ctredit:

  def __init__(self,data):
    self.key = open("/dev/urandom").read(16)
    self.nounce = int(open("/dev/urandom").read(8).encode('hex'),16)
    self.encdata = c18.ctrencrypt(data,self.nounce,self.key)

  def getdata(self):
    return self.encdata

  def edit(self,offset,text):

    if offset < 0:
      return False
    if offset + len(text) > len(self.encdata):
      return False
    if len(text) == 0:
      return False

    data = c18.ctrencrypt(self.encdata,self.nounce,self.key)
    tmp = data[:offset]+text+data[len(text)+offset:]
    self.encdata = c18.ctrencrypt(tmp,self.nounce,self.key)
    return True

if __name__ == "__main__":

  try:
    data = open("c25.txt").read()
  except:
    data = urllib.urlopen("https://gist.github.com/tqbf/3132853/raw/c02ff8a08ccf872f4cd278396379f4bb1ef337d8/gistfile1.txt").read()
    open("c25.txt","w").write(data)

  obj = ctredit(base64.b64decode(data))
  enc0 = obj.getdata()

  if obj.edit(0,"a"*len(enc0)):

    enc1 = obj.getdata()

    key = "".join([ chr(ord(c)^ord("a")) for c in enc1])
    txt0 = "".join([ chr(ord(k)^ord(c)) for k,c in zip(key,enc0)])
    print txt0.encode('hex')
