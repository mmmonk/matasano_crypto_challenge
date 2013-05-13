#!/usr/bin/env python

import c21
import random
import time
import hashlib

def ctrMT(s,key):
  '''
  CTR "cipher" based on the MT19937 RNG
  '''
  rng = c21.MT19937(key)
  out = ""
  for c in s:
    out += chr(ord(c) ^ (rng.extract_number() & 0xff))
  return out


class pwdtoken:
  '''
  reset token class
  '''
  def gen(self,uid):
    self.uid = uid
    rng = c21.MT19937(int(time.time()))
    self.rv = rng.extract_number() # this should be stored and linked to the user account
    return hashlib.md5(str(self.rv)+str(self.uid)).hexdigest()

  def check(self,s):
    if hashlib.md5(str(self.rv)+str(self.uid)).hexdigest() == s:
      return True
    else:
      return False

##############################################
print "######### stream cipher #########"
key = int(open("/dev/urandom").read(2).encode('hex'),16)

### finding the key for the known plaintext
msg = ""
for i in range(random.randint(10,64)):
  msg += chr(random.randint(0,255))

msg += "A"*14
cph = ctrMT(msg,key)

print "encrypted mesg: "+cph.encode('string_escape')

for x in xrange(2**16):
  out2 =  ctrMT(cph,x)
  if out2[-14:] == "A" * 14:
    print "   broken mesg: "+ctrMT(cph,x).encode('string_escape')
    break

##############################################
### this is the password reset token
print "######### Reset token #########"
pwdrst = pwdtoken()
token = pwdrst.gen("forgetfuluser@somedomain.using")

time.sleep(random.randint(10,120))

# we can narrow down the digest used by the length of the hex string
uid = "forgetfuluser@somedomain.using" # we assume this is a known value
ts = int(time.time())
for i in range(86400):
  rng = c21.MT19937(ts - i)
  if hashlib.md5(str(rng.extract_number())+uid).hexdigest() == token:
    print "we got the reset token, it was generated using ts: "+str(ts)
    break
