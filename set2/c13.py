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

  # random key
  key = open("/dev/urandom").read(16)

  encprofile = encrypt(profile_for("test@test.company"),key)

  print mkobj(decrypt(encprofile,key))
