#!/usr/bin/env python

import web
import c28
import time
import os

sigs = dict()

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


class hmac_check:

  def GET(self):

    global sigs

    var = web.input(file="c32s.py",signature="0")
    sig = "\x00"
    try:
      if sigs.has_key(var.file) and sigs[var.file][1] > os.stat(var.file)[8]:
        sig = sigs[var.file][0]
      else:
        sig = hmac("secret",open(var.file).read(),c28.sha1).digest()
        sigs[var.file] = (sig,int(time.time()))
    except:
      pass

    if insecure_compare(sig,var.signature):
      return "OK"
    raise web.internalerror()

def insecure_compare(s1,hs2,st=0):

  try:
    s2 = hs2.decode('hex')
  except:
    return False

  if len(s1) != len(s2):
    return False

  for (c1,c2) in zip (s1,s2):
    if c1 != c2:
      return False
    #time.sleep(0.0001) # <<<- DELAY ADJUST THIS
  return True

class MyWrongHmacApp(web.application):
  def run(self, port=9000, *middleware):
    func = self.wsgifunc(*middleware)
    return web.httpserver.runsimple(func, ('127.0.0.1', port))

def internalerror():
  return web.internalerror("nope")

if __name__ == "__main__":
  urls = ( '/test?.*', 'hmac_check')
  app = MyWrongHmacApp(urls, globals())
  app.internalerror = internalerror
  app.run()

