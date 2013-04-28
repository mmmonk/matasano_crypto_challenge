#!/usr/bin/env python

def encryption_oracle(s,key):
  import c10
  import base64
  from Crypto.Cipher import AES

  secret = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n\
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n\
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n\
YnkK"

  s = s + base64.b64decode(secret)

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
  import sys

  # getting random key
  key = open("/dev/urandom").read(16)

  # finding out the block size of the cipher
  blksize = 1
  while True:
    s = "A"*(blksize*2)
    c = encryption_oracle(s,key)
    if c[:blksize] == c[blksize:blksize*2]:
      break
    blksize += 1

  print "block size: "+str(blksize)

  if findecb(c.encode('hex'),blksize) == None:
    sys.exit(0)

  print "this is ECB mode"

  enclen = len(encryption_oracle("a",key))

  output = ""
  nextblock = "A"*blksize
  for x in range(0,enclen,blksize):
    attack = nextblock
    nextblock = ""
    for i in range(blksize):
      attack = attack[1:]
      encryptedblk = encryption_oracle(attack,key)[x:x+blksize]
      for c in range(256):
        s = attack + nextblock + chr(c)
        if encryption_oracle(s,key)[:blksize] == encryptedblk:
          nextblock += chr(c)
          break

    output += nextblock
  print "seceret msg:\n"+output
