#!/usr/bin/env python

import urllib
import base64
import c18
import c3

msgs = urllib.urlopen("https://gist.github.com/tqbf/3336141/raw/d601f0b675feef570188ab2c8f347843f965ee14/gistfile1.txt").read()

key = open("/dev/urandom").read(16)

cts = list()
minl = 999
for msg in msgs.split("\n"):
    cts.append(c18.ctrencrypt(base64.b64decode(msg),0,key).encode('hex'))
    if len(cts[-1]) > 0 and minl > len(cts[-1]):
      minl = len(cts[-1])

# prepare the list for the one character
rcts = range(minl)
for i in range(minl):
  rcts[i] = list()

for i in range(len(cts)):
  cts[i] = cts[i][:minl]
  print cts[i]
  ct = cts[i]
  for j in range(len(ct)):
    rcts[j].append(ct[j])

for i in range(len(rcts)):
  print c3.fcxor("".join(rcts[i]))
