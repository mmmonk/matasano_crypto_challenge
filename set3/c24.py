#!/usr/bin/env python

import c21

def ctrMT(s,key):
  '''
  CTR "cipher" based on the MT19937 RNG
  '''
  rng = c21.MT19937(key)
  out = ""
  for c in s:
    out += chr(ord(c) ^ (rng.extract_number() & 0xff))
  return out

msg = "A"*14
cph = ctrMT(msg,0xaaaa)
out = ctrMT(cph,0xaaaa)

print msg
print cph.encode('string_escape')
print out.encode('string_escape')


