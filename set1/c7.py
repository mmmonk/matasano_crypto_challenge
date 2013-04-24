#!/usr/bin/env python

import urllib
import base64
from Crypto.Cipher import AES

ct = base64.b64decode(urllib.URLopener().open("https://gist.github.com/tqbf/3132853/raw/c02ff8a08ccf872f4cd278396379f4bb1ef337d8/gistfile1.txt").read())
a = AES.new("YELLOW SUBMARINE",AES.MODE_ECB)
print a.decrypt(ct)
