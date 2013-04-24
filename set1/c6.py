#!/usr/bin/env python

import urllib
import base64

def hamming_distance(s1, s2):
  assert len(s1) == len(s2)
  return sum(c1 != c2 for c1, c2 in zip(s1, s2))

#ct = base64.b64decode(urllib.URLopener().open("https://gist.github.com/tqbf/3132752/raw/cecdb818e3ee4f5dda6f0847bfd90a83edb87e73/gistfile1.txt").read())

#print hamming_distance("this is a test","wokka wokka!!!")
