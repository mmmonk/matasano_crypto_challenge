#!/usr/bin/env python

from Crypto.Cipher import AES
import struct

def ctrencrypt(s,nonce,key,blksize=16):

  return ctrdecrypt(s,nonce,key,blksize)


def ctrdecrypt(s,nonce,key,blksize=16):

  a = AES.new(key,AES.MODE_ECB)
  out = ""
  ctr = 0
  for i in range(0,len(s),blksize):
    stream = a.encrypt(struct.pack("<Q",nonce)+struct.pack("<Q",ctr))
    out += "".join([chr(ord(c1)^ord(c2)) for (c1,c2) in zip(stream,s[i:i+blksize])])
    ctr += 1

  return out

if __name__ == "__main__":
  import base64

  txt = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
  print ctrdecrypt(txt,0,"YELLOW SUBMARINE")
