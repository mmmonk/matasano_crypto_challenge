#!/usr/bin/env python

import base64
from Crypto.Cipher import AES

ct = base64.b64decode(open("c7.txt").read())
a = AES.new("YELLOW SUBMARINE",AES.MODE_ECB)
print a.decrypt(ct)
