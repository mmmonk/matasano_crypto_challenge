#!/usr/bin/env python

def xorss(s1,s2): # xor for strings
  if len(s1) > len(s2):
    return "".join([chr(ord(s1[i])^ord(s2[i])) for i in range(len(s1))])
  return "".join([chr(ord(s1[i])^ord(s2[i])) for i in range(len(s2))])

print xorss("1c0111001f010100061a024b53535009181c".decode('hex'),"686974207468652062756c6c277320657965".decode('hex')).encode('hex')
