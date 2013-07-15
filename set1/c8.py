#!/usr/bin/env python

def findecb(cte,blksize=16):
  ct = cte.decode('hex')
  a = dict()
  for i in range(0,len(ct),blksize):
    c = ct[i:i+blksize]
    a[c] = a.get(c,0) + 1
    if a[c] > 1:
      return cte

if __name__ == "__main__":
  import urllib

  try:
    data = open("c8.txt").read()
  except:
    data = urllib.urlopen("https://gist.github.com/tqbf/3132928/raw/6f74d4131d02dee3dd0766bd99a6b46c965491cc/gistfile1.txt").read()
    open("c8.txt","w").write(data)

  for l in data.split("\n"):
    ct = findecb(l.rstrip())
    if ct != None:
      print ct

