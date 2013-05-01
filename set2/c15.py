#!/usr/bin/env python

def pkcs7chk(s,blksize=16):
  padlen = ord(s[-1])
  assert padlen <= blksize, 'pad length wrong'

  sl = len(s)-1
  for i in range(padlen):
    assert ord(s[sl - i]) == padlen, "wrong padding"
  return s[:sl-padlen+1]

