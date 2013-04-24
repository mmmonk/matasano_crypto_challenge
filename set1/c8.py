#!/usr/bin/env python

import urllib
import base64

ct = base64.b64decode(urllib.URLopener().open("https://gist.github.com/tqbf/3132928/raw/6f74d4131d02dee3dd0766bd99a6b46c965491cc/gistfile1.txt").read())
