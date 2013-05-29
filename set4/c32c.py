#!/usr/bin/env python

import time
import c31c
import numpy
import socket
import sys

url = "http://127.0.0.1:9001/test?file="
fn = "c32s.py"

def checkurl(fn,sig):

  msg = "GET /test?file="+fn+"&signature="+sig+" HTTP/1.1\r\nHost: 127.0.0.1:9001\r\nConnection: close\r\n\r\n"

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
  s.connect(("127.0.0.1",9001))

  ts = time.time()
  s.send(msg)
  data = s.recv(30)
  ts = time.time() - ts
  s.shutdown(socket.SHUT_RDWR)

  ok = False
  if "200" in data:
    ok = True

  return ts, ok

def test4extream(value, mean, stddev):
  if (value > (mean + stddev)) or (value < (mean - stddev)):
    return False
  return True

def test1char(sig,idx,tries,url,fn):

  a = range(256)    # this holds the mean values for all the numbers tested
  left = range(256) # this holds the values of b[] there were not removed due to extreme test
  for i in range(256):
    sig[idx] = i
    b = list()      # this holds the times for all the tests for a give value
    for j in range(tries):
      t, rc = checkurl(fn,"".join([chr(c) for c in sig]).encode('hex'))
      if rc:
        print "done, this works: "+url+fn+"&signature="+"".join([chr(c) for c in sig]).encode('hex')
        sys.exit(0)
      else:
        b.append(t)
    # this is to collect some data
    #open("c32c_data_"+str(idx).zfill(3)+"_"+chr(i).encode('hex').zfill(2)+".txt","w").write(str(b))
    mean = numpy.mean(b)
    std = numpy.std(b)
    b = [v for v in b if test4extream(v,mean,std)]
    a[i] = numpy.mean(b)
    left[i] = len(b)

  return a.index(max(a)),a,left

if __name__ == "__main__":

  tries = 1 # initial value this will be auto adjusted later
  sig = [0] * 20 # numbers of bytes in the signature

  try:

    # this is just to make sure that the server has the file in memory/cache
    checkurl(fn,"".join([chr(c) for c in sig]).encode('hex'))

    for idx in range(20):

      autoadj = 1  # reset this for each new idx
      prev = [0,0]
      a = [0]
      left = [0]
      first = True

      while True:
        ans,a,left = test1char(sig,idx,tries,url,fn)
        if ans == prev[0]: # if we get three times in a row the same answer, this is a good start
          if ans == prev[1]:
            sig[idx] = ans
            break
          else:
            prev[1] = prev[0]
        elif first:
          first = False
        else:
          tries += autoadj    # increase the number of tries
          autoadj += 1        # increase the autoadj
        prev[0] = ans
        print hex(ans)+" "+str(tries)+" "+str(autoadj)+"\r",
        sys.stdout.flush()
      print "idx["+str(idx).zfill(2)+"]="+hex(sig[idx]).replace("0x","").zfill(2)+" "+str(max(a)).rjust(15)+" "+str(numpy.mean(a)).rjust(15)+" "+str(numpy.mean(left)).rjust(15)+" "+str(tries)+"\a"
    print "done, probably this doesn't work by try it anyway:\n"+url+fn+"&signature="+"".join([chr(c) for c in sig]).encode('hex')

  except KeyboardInterrupt:
    pass
