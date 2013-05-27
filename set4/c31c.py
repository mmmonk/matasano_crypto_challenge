#!/usr/bin/env python

import urllib2
import time


url = "http://127.0.0.1:9000/test?file="
fn = "c31s.py"

def checkurl(url,fn,sig):
  ok = False
  st = time.time()
  try:
    res = urllib2.urlopen(url+fn+"&signature="+sig)
    ok = True
  except urllib2.HTTPError:
    pass
  en = time.time()-st
  return (en,ok)

if __name__ == "__main__":
  sig = [0] * 20

  try:
    # this is just to make sure that the server caches the file
    checkurl(url,fn,"".join([chr(c) for c in sig]).encode('hex'))
    for idx in range(20):
      print "idx["+str(idx).zfill(2)+"]=",
      a = list()
      for i in range(256):
        sig[idx] = i
        t, rc = checkurl(url,fn,"".join([chr(c) for c in sig]).encode('hex'))
        a.append(t)
        if len(a) > 1 and abs(a[-2]-a[-1]) > 0.1:
          break

      sig[idx] =  a.index(max(a))
      print hex(sig[idx]).replace("0x","").zfill(2)+"\a"

    print "done, try: "+url+fn+"&signature="+"".join([chr(c) for c in sig]).encode('hex')
  except KeyboardInterrupt:
    pass
