#!/usr/bin/env python

def mkobj(s):
  out = "{"
  start = True
  for p in s.split("&"):
    o = p.split("=")
    out += "\n  "+o[0]+": '"+o[1]+"',"
  out = out.rstrip(',')
  out += "\n}"
  return out

def profile_for(s):
  s = s.replace("&","").replace("=","")
  return "email="+s+"&uid=10&role=user"

def encrypt(s,key):
  import c10
  from Crypto.Cipher import AES

  return AES.new(key,AES.MODE_ECB).encrypt(c10.pkcs7pad(s))

def decrypt(s,key):
  import c10
  from Crypto.Cipher import AES

  return c10.pkcs7chk(AES.new(key,AES.MODE_ECB).decrypt(s))

if __name__ == "__main__":

  import sys

  # random key
  key = open("/dev/urandom").read(16)

  out1 = encrypt(profile_for("A"*10+"admin"),key) # this gives me block with "admin....."
  out2 = encrypt(profile_for("testuser@some.not.that.domain"),key) # this gives me the username and "role=" and the end of the block
  out3 = encrypt(profile_for("A"*32),key) # this is to make sure that we have correct paddinig and all vars have values
  test = out2[:48]+out1[16:32]+out3[48:] # putting this all together

  print mkobj(decrypt(test,key))
