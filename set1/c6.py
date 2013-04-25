#!/usr/bin/env python

import base64
import c3

def findkeylen(ct,keylen,blocks=5): # calculates Hamming distance for few blocks for the same keylength
  return sum(hd(ct[i:i+keylen],ct[i+keylen:i+keylen*2])/float(keylen) for i in range(0,keylen*blocks,keylen))/blocks

def ch2bin(s): # changing chars to bits
  return "".join([ bin(ord(c)).replace("0b","").zfill(8) for c in s ])

def hd(s1, s2): # calculations for the Hamming distance
  return sum(c1 != c2 for c1, c2 in zip(ch2bin(s1), ch2bin(s2)))

def reorderblk(ct,keylen):
  blks = [ list() for i in range(keylen) ]

  for i in range(0,len(ct),keylen):
    if i+keylen < len(ct):
      txt = ct[i:i+keylen]
      for j in range(keylen):
        blks[j].append(txt[j])
  return blks

ct = base64.b64decode(open("c6.txt").read())

key_len = dict()
for kl in range(2,40):
  key_len[kl] = findkeylen(ct,kl)

for kl in sorted(key_len , key = key_len.get):
  sxor = reorderblk(ct,kl)
  key = ""
  for i in range(kl):
    txt = c3.fcxor("".join(sxor[i]))
    if txt != None:
      key += chr(txt[0])
    else:
      key += chr(0)

  if not '\x00' in key:
    print str((kl,key))
    break

