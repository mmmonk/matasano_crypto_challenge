#!/usr/bin/env python

def encryption_oracle(s):
  import c10
  import random
  from Crypto.Cipher import AES

  key = open("/dev/urandom").read(16)

  prefix = open("/dev/urandom").read(random.randint(5,10))
  suffix = open("/dev/urandom").read(random.randint(5,10))

  s = str(prefix)+str(s)+str(suffix)
  if random.randint(0,1) == 1:
    return c10.cbcencrypt(s,open("/dev/urandom").read(16),key)
  else:
    return AES.new(key,AES.MODE_ECB).encrypt(c10.pkcs7pad(s))


def findecb(cte,blksize=16):
  ct = cte.decode('hex')
  a = dict()
  for i in range(0,len(ct),blksize):
    c = ct[i:i+blksize]
    a[c] = a.get(c,0) + 1
    if a[c] > 1:
      return cte

if __name__ == "__main__":

  out = findecb(encryption_oracle("0"*128).encode('hex'))
  if out != None:
    print "ECB"
  else:
    print "CBC"
