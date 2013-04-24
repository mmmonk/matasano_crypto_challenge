#!/usr/bin/env python

def xorss(s1,s2):
  ml = len(s2)
  if len(s1) > len(s2):
    ml = len(s1)
  return "".join([chr(ord(s1[i])^ord(s2[i])) for i in range(ml)])

print xorss("1c0111001f010100061a024b53535009181c".decode('hex'),"686974207468652062756c6c277320657965".decode('hex')).encode('hex')
