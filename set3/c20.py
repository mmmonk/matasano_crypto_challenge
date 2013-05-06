#!/usr/bin/env python

import base64
import c18
import urllib

msgs = urllib.urlopen("https://gist.github.com/tqbf/3336141/raw/d601f0b675feef570188ab2c8f347843f965ee14/gistfile1.txt").read()

key = open("/dev/urandom").read(16)

cts = list()
minl = 999
for msg in msgs.split("\n"):
    cts.append(c18.ctrencrypt(base64.b64decode(msg),0,key).encode('hex'))
    if len(cts[-1]) > 0 and minl > len(cts[-1]):
      minl = len(cts[-1])

for i in range(0,len(cts)):
  cts[i] = cts[i][:minl]
  print cts[i]
