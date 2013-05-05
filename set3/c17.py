#!/usr/bin/env python

import c10
import random
import base64

class cc17:

  def __init__(self,blksize=16):
    self.blksize = blksize
    self.key = open("/dev/urandom").read(self.blksize)
    self.iv = open("/dev/urandom").read(self.blksize)

  def fun1 (self):

    msgs = "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=\n\
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=\n\
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==\n\
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==\n\
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl\n\
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==\n\
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==\n\
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=\n\
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=\n\
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"

    return (self.iv,c10.cbcencrypt(base64.b64decode(random.choice(msgs.split("\n"))),self.iv,self.key))

  def fun2(self,s):

    try:
      c10.cbcdecrypt(s,self.iv,self.key)
      return True
    except:
      return False

def padding_oracle_attack(oracfunc, pblk, blk, blksize=16):
  '''
  based on http://www.skullsecurity.org/blog/2013/padding-oracle-attacks-in-depth

  oracfunc - function that provides the oracle
  iv       - IV
  pblk     - previous block to the attacked one
  blk      - the block we want to decrypt
  blksize  - block size
  '''

  # index at which we start - the last character
  idx = blksize - 1

  # start value for the padding
  pad = 1

  # last used index
  lidx = 0

  # this is the "attack" block
  ablk = ["\x00"] * blksize

  while idx >= 0:

    for c in range(0, 256):

      ablk[idx] = chr( ord(pblk[idx]) ^ pad ^ c)

      if oracfunc("".join(ablk) + blk):

        if idx == 0:
          idx -= 1
          break

        ablk[idx - 1] = chr( ord(pblk[idx - 1]) ^ pad ^ 0x01)

        if oracfunc("".join(ablk) + blk):
          idx -= 1

          # new padding value
          pad = blksize - idx

          # recalculate the padding done so far
          for j in range(idx + 1, blksize):
            ablk[j] = chr( ord(ablk[j]) ^ (pad - 1) ^ pad)

          break
        ablk[idx - 1] = chr( ord(pblk[idx - 1]) ^ pad ^ 0x01)

      # if we get here then we calculated something wrong, we need to go back
      if c == 255 and idx < blksize - 1:
        idx += 1

  # xoring our block, padding and known block
  out = [ chr( ord(c1) ^ blksize ^ ord(c2) ) for (c1,c2) in zip(ablk,pblk) ]
  return "".join(out).encode('string_escape')

if __name__ == "__main__":

  blksize = 16

  c17 = cc17(blksize)
  (iv,ct) = c17.fun1() # iv is only needed to decode the first block

  txt = padding_oracle_attack(c17.fun2,iv,ct[:blksize],blksize)
  for x in range(blksize,len(ct),blksize):
    txt += padding_oracle_attack(c17.fun2,ct[x-blksize:x],ct[x:x+blksize],blksize)
  print txt
