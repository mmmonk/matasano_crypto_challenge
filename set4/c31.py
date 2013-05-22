#!/usr/bin/env python

import c28

def hmac(key,msg,algo):
  '''
  generic HMAC function
  https://en.wikipedia.org/wiki/Hash-based_message_authentication_code
  https://tools.ietf.org/html/rfc2104
  '''
  if len(key) > algo.blocksize:
    key = algo(key).digest()

  key += "\x00" * (algo.blocksize - len(key))
  ipad = "".join([chr(ord(c1)^ord(c2)) for (c1,c2) in zip(key,"\x36" * algo.blocksize) ])
  opad = "".join([chr(ord(c1)^ord(c2)) for (c1,c2) in zip(key,"\x5c" * algo.blocksize) ])

  return algo(opad + algo(ipad + msg).digest())

if __name__ == "__main__":

  print hmac("key","The quick brown fox jumps over the lazy dog",c28.sha1).hexdigest()
  print hmac("","",c28.sha1).hexdigest()
