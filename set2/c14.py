#!/usr/bin/env python

def encryption_oracle(s,key="",prefix=""):
  import c10
  import base64
  from Crypto.Cipher import AES

  secret = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n\
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n\
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n\
YnkK"
  s = prefix + s + base64.b64decode(secret)

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
  import random

  # getting random key
  key = open("/dev/urandom").read(16)

  # random prefix
  prefix = open("/dev/urandom").read(random.randint(1,256))

  ct1 = encryption_oracle("a", key, prefix)
  ct2 = encryption_oracle("b", key, prefix)

  offset = 0
  for i in range(len(ct1)):
    if ct1[i] != ct2[i]:
      offset = i
      break

  print "offset for block with our data: "+str(offset)

  # finding out the block size of the cipher
  blksize = 1
  while True:
    s = ("A"*(blksize*2))*3
    c = encryption_oracle(s, key, prefix)
    if c[offset+blksize:offset+blksize*2] == c[offset+blksize*2:offset+blksize*3]:
      break
    blksize += 1

  print "block size: "+str(blksize)

  if findecb(c.encode('hex'),blksize) == None:
    sys.exit(0)

  print "this is ECB mode"

  enclen = len(encryption_oracle("a", key, prefix)) - offset

  offstr = 0
  for i in range(1,blksize*4):
    s = "a"*i
    if encryption_oracle(s, key, prefix)[offset+blksize] == encryption_oracle(s, key, prefix)[offset+(blksize*2)]:
      offstr = i-(blksize*2)
      print str(i-(blksize*2))
      break

  if offstr == blksize:
    offstr = 0
  else:
    offset += blksize

  print "ourdata offset in the block: "+str(offstr)

  output = ""
  nextblock = "A"*offstr+"A"*blksize
  for x in range(0,enclen,blksize):
    attack = "A"*offstr+nextblock
    nextblock = ""
    for i in range(blksize):
      attack = attack[1:]
      encryptedblk = encryption_oracle(attack, key, prefix)[offset+x:offset+x+blksize]
      for c in range(256):
        s = attack + nextblock + chr(c)
        if encryption_oracle(s, key, prefix)[offset:offset+blksize] == encryptedblk:
          nextblock += chr(c)
          break

    output += nextblock
  print "seceret msg:\n"+output
