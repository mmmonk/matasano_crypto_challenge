#!/usr/bin/env python

import urllib
import base64
import c19
import c18
import string

def xors(s1,s2):
  return "".join([ chr(ord(c1)^c2) for (c1,c2) in zip(s1,s2)])

msgs = urllib.urlopen("https://gist.github.com/tqbf/3336141/raw/d601f0b675feef570188ab2c8f347843f965ee14/gistfile1.txt").read()

key = open("/dev/urandom").read(16)

# encryption of the data we got
cts = list()
milen = 999
for msg in msgs.split("\n"):
  if len(msg) > 0:
    cts.append(c18.ctrencrypt(base64.b64decode(msg),0,key))
    if len(cts[-1]) > 0 and milen > len(cts[-1]):
      milen = len(cts[-1])

# decryption of the data
key = [0]*milen
key = c19.basicautoguessing(cts,key,milen)
key = c19.bigrams(cts,key)

g = c19.gui(cts,key)
g.run()
