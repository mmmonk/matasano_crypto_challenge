#!/usr/bin/env python

import urllib2
import time
import c31c
import numpy

url = "http://127.0.0.1:9001/test?file="
fn = "c32s.py"

def test4extream(value ,mean,stddev,multi=0):
  if (value > (mean + (multi * stddev))) or \
    (value < (mean - (multi * stddev))):
    return False
  return True

if __name__ == "__main__":
  tries = 20
  sig = [0] * 20

  try:
    # this is just to make sure that the server caches the file
    c31c.checkurl(url,fn,"".join([chr(c) for c in sig]).encode('hex'))
    for idx in range(20):
      print "idx["+str(idx).zfill(2)+"]=",
      a = list()
      for i in range(256):
        sig[idx] = i
        b = list()
        t = 0
        rc = 0
        for i in range(tries):
          t, rc = c31c.checkurl(url,fn,"".join([chr(c) for c in sig]).encode('hex'))
          b.append(t)
        mean = numpy.mean(b)
        stddev = numpy.std(b)
        b = [v for v in b if test4extream(v,mean,stddev,2)]
        a.append(sum(b)/len(b))
      sig[idx] =  a.index(max(a))
      print hex(sig[idx]).replace("0x","").zfill(2)+" "+str(max(a))+" "+str(sum(a)/len(a)) +"\a"

    print "done, try: "+url+fn+"&signature="+"".join([chr(c) for c in sig]).encode('hex')
  except KeyboardInterrupt:
    pass
