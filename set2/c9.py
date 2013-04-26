#!/usr/bin/env python

def pkcs7pad(s,blksize=8):
  missing = abs(len(s) - (len(s)/blksize+1) * blksize)
  return s+(chr(missing)*missing)

if __name__ == "__main__":
  print pkcs7pad("YELLOW SUBMARINE",20).encode('string_escape')
