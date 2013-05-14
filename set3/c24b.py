#!/usr/bin/env python

import c21
import random
import time
import hashlib

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

userid = "forgetfuluser@somedomain.com"
pwdrst = pwdtoken()
token = pwdrst.gen(userid)

print "reset token for user "+str(userid)+" is \""+str(token)+"\""
print "random wait for added suspense"
time.sleep(random.randint(10,120))

# we can narrow down the digest used by the length of the hex string
# the assumption is here that userid is a known value
ts = int(time.time())
for i in range(86400):

  rng = c21.MT19937(ts - i)
  rnv = rng.extract_number()

  # matching the hash both ways - just in case
  if hashlib.md5(str(rnv)+userid).hexdigest() == token or\
      hashlib.md5(userid+str(rnv)).hexdigest() == token:
    print "the reset token was generated using timestamp: "+str(ts)
    break
