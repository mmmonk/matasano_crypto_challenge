#!/usr/bin/env python

'''
You're relying on the fact that in CBC mode, a 1-bit error in a
ciphertext block:

* Completely scrambles the block the error occurs in

* Produces the identical 1-bit error (/edit) in the next ciphertext
 block.

Before you implement this attack, answer this question: why does CBC
mode have this property?

----
Because the next plaintext block is XORed with the encrypted output from
the previous block (or IV if we try to encrypt

'''

from Crypto.Cipher import AES

def pkcs7pad(s,blksize=16):
  missing = abs(len(s) - (len(s)/blksize+1) * blksize)
  return s+(chr(missing)*missing)

def pkcs7chk(s,blksize=16):
  padlen = ord(s[-1])
  assert padlen <= blksize, 'pad length wrong'

  sl = len(s)-1
  for i in range(padlen):
    assert ord(s[sl - i]) == padlen, "wrong padding"
  return s[:sl-padlen+1]

def cbcencrypt(s,iv,key,blksize=16):

  assert len(iv) == blksize, 'IV is not equal to blocksize'
  a = AES.new(key,AES.MODE_ECB)
  s = pkcs7pad(s,blksize)
  out = ""

  for i in range(0,len(s),blksize):
    mx = "".join([chr( ord(c1) ^ ord(c2) ) for (c1, c2) in zip(  iv, s[i:i+blksize])])
    iv = a.encrypt(mx)
    out += iv
  return out

def cbcdecrypt(s,iv,key,blksize=16):

  assert len(iv) == blksize, 'IV is not equal to blocksize'
  a = AES.new(key,AES.MODE_ECB)
  out = ""

  for i in range(0,len(s),blksize):
    enc = a.decrypt(s[i:i+blksize])
    out += "".join([chr(ord(c1)^ord(c2)) for (c1,c2) in zip(iv,enc)])
    iv = s[i:i+blksize]

  return pkcs7chk(out)

def myinput(s,iv,key):
  s = s.replace(";","\;").replace("=","\=")
  prefix = "comment1=cooking%20MCs;userdata="
  suffix = ";comment2=%20like%20a%20pound%20of%20bacon"

  return cbcencrypt(prefix+s+suffix,iv,key)

def checkadmin(s,iv,key):
  if ";admin=true;" in cbcdecrypt(s,iv,key):
    return True
  return False

if __name__ == "__main__":

  iv = open("/dev/urandom").read(16)
  key = open("/dev/urandom").read(16)

  '''
  we move the ":admin<true" to the beginning of the next block
  we chose the ":" and "<" to be just one bit different then
  our targets ";" and "=" what is left is to modify the corresponding
  characters in previous block (the encoding is one to one, one plain text byte
  corresponds to one ciphertext byte) by XORing them with 1.
  '''
  enc = myinput("a"*16+":admin<true",iv,key) # our input
  test1 = chr(ord(enc[32])^1)+enc[33:38]+chr(ord(enc[38])^1)+enc[39:48] # XORing by one two characters
  test = enc[:32]+test1+enc[48:] # recreating the ciphertext

  if checkadmin(test,iv,key) == True: # keeping fingers crossed
    print "we did good ;)"
  else:
    print ":("

