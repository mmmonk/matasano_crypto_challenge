#!/usr/bin/env python

import c21
import random
import time

def ctrMT(s,key):
  '''
  CTR "cipher" based on the MT19937 RNG
  '''
  rng = c21.MT19937(key)
  out = ""
  for c in s:
    out += chr(ord(c) ^ (rng.extract_number() & 0xff))
  return out

key = int(open("/dev/urandom").read(2).encode('hex'),16)

### finding the key for the known plaintext
msg = ""
for i in range(random.randint(10,64)):
  msg += chr(random.randint(0,255))

msg += "A"*14
print hex(key)+" "+str(key)
cph = ctrMT(msg,key)
out = ctrMT(cph,key)

print msg.encode('string_escape')
print cph.encode('string_escape')
print out.encode('string_escape')

for x in xrange(2**16):
  out2 =  ctrMT(cph,x)
  if out2[-14:] == "A" * 14:
    print x
    break

###


