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

if __name__ == "__main__":
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

  print blksize

