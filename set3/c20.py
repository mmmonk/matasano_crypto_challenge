#!/usr/bin/env python

import urllib
import base64
import c19
import c18
import c3
import string

def xors(s1,s2):
  return "".join([ chr(ord(c1)^c2) for (c1,c2) in zip(s1,s2)])

msgs = urllib.urlopen("https://gist.github.com/tqbf/3336141/raw/d601f0b675feef570188ab2c8f347843f965ee14/gistfile1.txt").read()

key = open("/dev/urandom").read(16)

cts = list()
milen = 999
for msg in msgs.split("\n"):
  if len(msg) > 0:
    cts.append(c18.ctrencrypt(base64.b64decode(msg),0,key))
    if len(cts[-1]) > 0 and milen > len(cts[-1]):
      milen = len(cts[-1])

key = [0]*milen

# prepare the list for the one character
rev = range(milen)
for i in range(milen):
  rev[i] = list()

for i in range(len(cts)):
  cts[i] = cts[i][:milen]
  #print cts[i]
  ct = cts[i]
  for j in range(len(ct)):
    rev[j].append(ct[j])

for i in range(len(rev)):
  out = c3.fcxor("".join(rev[i]))
  if out != None:
    key[i] = out[0]

# finding the first letter (based on the most common ones):
# from http://www.cryptograms.org/letter-frequencies.php
for c in "TAISOCMFPWtaisocmfpw":
  key[0] = ord(cts[0][0])^ord(c)
  revt = [ chr(ord(c1)^key[0]) for c1 in rev[0]]
  good = True
  for i in range(milen):
    if not revt[i] in string.letters+" ":
      good = False
      break
  if good == True:
    break

g = c19.gui(cts,key)
g.run()
