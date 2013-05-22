#!/usr/bin/env python

import BaseHTTPServer
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

def run(server_class=BaseHTTPServer.HTTPServer, handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
  server_address = ('', 8000)
  httpd = server_class(server_address, handler_class)
  httpd.serve_forever()

if __name__ == "__main__":

  print hmac("key","The quick brown fox jumps over the lazy dog",c28.sha1).hexdigest()
  print hmac("","",c28.sha1).hexdigest()
  run()

