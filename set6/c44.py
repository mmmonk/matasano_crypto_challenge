#!/usr/bin/env python

import urllib


if __name__ == "__main__":
  try:
    data = open("c44.txt").read()
  except:
    data = urllib.urlopen("https://gist.github.com/anonymous/f83e6b6e6889f2e8b7ff/raw/3eea46b071376679c9cde13dd27c4fb22a56e601/challenge+44").read()
    open("c44.txt","w").write(data)

