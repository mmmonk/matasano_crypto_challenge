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
    print "ECB"
    return c10.cbcencrypt(s,open("/dev/urandom").read(16),key)
  else:
    print "CBC"
    return AES.new(key,AES.MODE_ECB).encrypt(c10.pkcs7pad(s))

if __name__ == "__main__":
  import c8

  print c8.findecb(encryption_oracle("0"*128).encode('hex'))
