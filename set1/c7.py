#!/usr/bin/env python

import base64
from Crypto.Cipher import AES
import urllib

try:
  data = open("c7.txt").read()
except:
  data = urllib.urlopen("https://gist.github.com/tqbf/3132853/raw/c02ff8a08ccf872f4cd278396379f4bb1ef337d8/gistfile1.txt").read()
  open("c7.txt","w").write(data)

ct = base64.b64decode(data)
a = AES.new("YELLOW SUBMARINE",AES.MODE_ECB)
print a.decrypt(ct)
