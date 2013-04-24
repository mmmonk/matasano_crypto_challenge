#!/usr/bin/env python

import urllib
import base64
import itertools
import c5
import c3

def hd(s1, s2):
  assert len(s1) == len(s2)
  return sum(c1 != c2 for c1, c2 in zip(s1, s2))

chars = ''.join([chr(c) for c in range(0,256)])
ct = base64.b64decode(urllib.URLopener().open("https://gist.github.com/tqbf/3132752/raw/cecdb818e3ee4f5dda6f0847bfd90a83edb87e73/gistfile1.txt").read())

possible_key = dict()
for kl in range(2,64):
  a = list()
  for keyc in itertools.product(chars,repeat=kl):
    a.append(c5.mcxor(''.join(keyc),ct))
    if len(a) > 4:
      for i in range(1,5):
        possible_key[kl] = possible_key.get(kl,0)+hd(a[0],a[i])/float(kl)
      possible_key[kl] /= 4
      break

for k in possible_key:
  print str(k)+" "+str(possible_key[k])
#print hamming_distance("this is a test","wokka wokka!!!")
