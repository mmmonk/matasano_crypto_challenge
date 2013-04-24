#!/usr/bin/env python

txt = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"

keys = key*((len(txt)/len(key))+1)
keys = keys[:len(txt)]

enc = [ chr(ord(c1)^ord(c2)) for (c1,c2) in zip(keys,txt) ]

print "".join(enc).encode('hex')
