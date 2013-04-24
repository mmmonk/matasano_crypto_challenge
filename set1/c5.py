#!/usr/bin/env python

def mcxor(key,msg):

  keys = key*((len(msg)/len(key))+1)
  keys = keys[:len(msg)]

  return "".join([ chr(ord(c1)^ord(c2)) for (c1,c2) in zip(keys,msg) ]).encode('hex')


if __name__ == "__main__":

  txt = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
  key = "ICE"

  print mcxor(key,txt)
