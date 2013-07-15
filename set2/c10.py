#!/usr/bin/env python

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
  iv = list(iv)
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
  iv = list(iv)
  out = ""

  for i in range(0,len(s),blksize):
    enc = a.decrypt(s[i:i+blksize])
    out += "".join([chr(ord(c1)^ord(c2)) for (c1,c2) in zip(iv,enc)])
    iv = s[i:i+blksize]

  return pkcs7chk(out)

if __name__ == "__main__":
  import base64
  import urllib

  try:
    txt = base64.b64decode(open("c10.txt").read())
  except:
    data = urllib.urlopen("https://gist.github.com/tqbf/3132976/raw/f0802a5bc9ffa2a69cd92c981438399d4ce1b8e4/gistfile1.txt").read()
    open("c10.txt","w").write(data)
    txt = base64.b64decode(data)
  print cbcdecrypt(txt,"\x00"*16,"YELLOW SUBMARINE")

