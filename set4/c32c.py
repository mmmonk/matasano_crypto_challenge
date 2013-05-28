#!/usr/bin/env python

import urllib2
import time
import c31c
import numpy

url = "http://127.0.0.1:9001/test?file="
fn = "c32s.py"

def checkurl(url,fn,sig):
  import socket
  pass


def test4extream(value ,mean,stddev,multi=1):
  if (value > (mean + (multi * stddev))) or \
    (value < (mean - (multi * stddev))):
    return False
  return True

if __name__ == "__main__":
  '''
  how many samples we need to gather from a single value
  100 is enough for delay of 0.005 s

  '''
  tries = 250 # tune this value

  sig = [0] * 20 # numbers of bytes in the signature

  try:
    # this is just to make sure that the server caches the file
    c31c.checkurl(url,fn,"".join([chr(c) for c in sig]).encode('hex'))

    for idx in range(20):

      a = list()    # this holds the mean values for all the numbers tested
      left = list() # this holds the values of b[] there were not removed due to extreme test
      for i in range(256):
        sig[idx] = i
        b = list()  # this holds the times for all the tests for a give value
        t = 0
        rc = 0
        for j in range(tries):
          t, rc = c31c.checkurl(url,fn,"".join([chr(c) for c in sig]).encode('hex'))
          if rc:
            sig[idx] = i
            print "done, trying: "+url+fn+"&signature="+"".join([chr(c) for c in sig]).encode('hex')
            if c31c.checkurl(url,fn,"".join([chr(c) for c in sig]).encode('hex'))[1]:
              print "Looks good :)"
            else:
              print "Doesn't look good :("
            sys.exit(0)
          else:
            b.append(t)
        # this is to collect some data
        #open("c32c_data_"+str(idx).zfill(3)+"_"+chr(i).encode('hex').zfill(2)+".txt","w").write(str(b))
        if len(b) > 1:
          mean = numpy.mean(b)
          std = numpy.std(b)
          b = [v for v in b if test4extream(v,mean,std,1)]
        a.append(numpy.mean(b))
        left.append(len(b))
      sig[idx] = a.index(max(a))

      print "idx["+str(idx).zfill(2)+"]="+hex(sig[idx]).replace("0x","").zfill(2)+" "+str(max(a))+" "+str(numpy.mean(a)) +" "+str(numpy.mean(left))+"\a"

  except KeyboardInterrupt:
    pass
