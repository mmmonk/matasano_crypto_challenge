#!/usr/bin/env python

import urllib2
import time
import c31c

url = "http://127.0.0.1:9001/test?file="
fn = "c32s.py"

if __name__ == "__main__":
  tries = 10
  sig = [0] * 20

  try:
    for idx in range(20):
      print "idx["+str(idx)+"]=",
      a = list()
      for i in range(256):
        sig[idx] = i
        b = list()
        t = 0
        rc = 0
        for i in range(tries):
          t, rc = c31c.checkurl(url,fn,"".join([chr(c) for c in sig]).encode('hex'))
          b.append(t)
        a.append(sum(b)/tries)

      sig[idx] =  a.index(max(a))
      print hex(sig[idx]).replace("0x","").zfill(2)+"\a"

    print "done, try: "+url+fn+"&signature="+"".join([chr(c) for c in sig]).encode('hex')
  except KeyboardInterrupt:
    pass
