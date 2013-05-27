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
  tries = 1 # 10 is enough for 0.005 seconds (5 ms)
  sig = [0] * 20

  try:
    for idx in range(20):
      print "idx["+str(idx)+"] =",
      a = list()
      for i in range(256):
        sig[idx] = i
        b = list()
        t = 0
        rc = 0
        for i in range(tries):
          t, rc = checkurl(url,fn,"".join([chr(c) for c in sig]).encode('hex'))
          b.append(t)
        a.append(sum(b)/tries)

      sig[idx] =  a.index(max(a))
      print hex(sig[idx]).replace("0x","").zfill(2)+"\a"

    print "done, try: "+url+fn+"&signature="+"".join([chr(c) for c in sig]).encode('hex')
  except KeyboardInterrupt:
    pass
