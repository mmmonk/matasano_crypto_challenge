#!/usr/bin/env python

import urllib
import hashlib
from c43 import DSA
from c36 import i2s, s2i
from c39 import invmod

class DSA_44(DSA):

  def k_dup(self, m1, s1, m2, s2):
    return ((m1-m2) * invmod((s1-s2) % self.q, self.q)) % self.q

if __name__ == "__main__":
  try:
    data = open("c44.txt").read()
  except:
    data = urllib.urlopen("https://gist.github.com/anonymous/f83e6b6e6889f2e8b7ff/raw/3eea46b071376679c9cde13dd27c4fb22a56e601/challenge+44").read()
    open("c44.txt","w").write(data)

  y = long("2d026f4bf30195ede3a088da85e398ef869611d0f68f07"+\
    "13d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b8"+\
    "5519b1c23cc3ecdc6062650462e3063bd179c2a6581519"+\
    "f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430"+\
    "f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d3"+\
    "2971c3de5084cce04a2e147821", 16)

  # expected hash for the searched x
  h_expected = "ca8f6f7c66fa362d40760d135b763eb8527d3d52"

  msgs = list()  # list of all messages (msg, s, r, m)
  dups = list()  # index of duplicated

  rs = dict()    # dictionary to check for duplicated R
  msg = list()   # temp variable to create (msg, s, r, m)

  c = 0
  # the duplicated k is easy to spot because it will produce the same r
  for l in data.split("\n"):
    (k, v) = l.split(" ", 1)
    if k == "msg:" and msg:
      # we have a full (msg, s, r, m) to add to msgs
      msgs.append(msg)
      msg = list()
      c += 1
    msg.append(v)

    if k == "r:":
      if rs.has_key(v):
        # we found a duplicate
        dups.append((rs[v], c))
      else:
        rs[v] = c

  # this appends the last msg to the msgs
  msgs.append(msg)

  # we now know which messages have duplicated k
  d = DSA_44()
  for p in dups:
    m1 = long(msgs[p[0]][3], 16) # this is sha1 hash of the first message
    s1 = long(msgs[p[0]][1])
    r1 = long(msgs[p[0]][2])
    msg1 = msgs[p[0]][0] # text of the first message

    m2 = long(msgs[p[1]][3], 16) # this is sha1 hash of the second message
    s2 = long(msgs[p[1]][1])

    # calculating k and checking it
    k = d.k_dup(m1, s1, m2, s2)

    # calculate x and check with the expected hash
    x = d.x_recovery(msg1, r1, s1, k)
    if hashlib.sha1(i2s(x).encode('hex')).hexdigest() == h_expected:
      # seems legit, lets verify by signing and verifying a signature
      (r1, s1) = d.sign(msg1, x)
      d.verify(msg1, r1, s1, y)
      print "k: %s" % (k)
      print "x: %s" % (x)
