#!/usr/bin/env python

def lfet(cc): # letter frequency for english test
  lfe = { "e": 12,"t": 9,"a": 8,"o": 7,"h": 6,"i": 6,"n": 6,"s": 6,"r": 5,"d": 4,"l": 4,"c": 2,"f": 2,"g": 2,"m": 2,"u": 2,"w": 2,"b": 1,"p": 1,"y": 1 }
  count = 0
  for c in lfe:
    if cc.get(c,0) >= lfe[c]/float(100):
      count += 1
    if count > 2:
      return True
  return False

def cfs(k,s): # character frequency from string
  chars = dict()

  for cc in s:
    c = chr(k^ord(cc)).lower()

    if not c in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c':
      return None

    chars[c] = chars.get(c,0) + 1
  return chars


def fcxor(ct): # find one character xor

  for key in range(256): # check all possible values
    chars = cfs(key,ct)
    if chars == None:
      continue

    for c in chars:
      chars[c] = chars[c]/float(len(ct))
    if chars.get(' ',0) > 0.1 and lfet(chars):
      return (key, "".join([chr(key^ord(c)) for c in ct]))

if __name__ == '__main__':
  ct = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
  print fcxor(ct.decode('hex'))
