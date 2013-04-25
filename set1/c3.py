#!/usr/bin/env python

import string

def lfet(cc): # letter frequency for english test
  lfe = { "e": 12,"t": 9,"a": 8,"o": 7,"h": 6,"i": 6,"n": 6,"s": 6,"r": 5,"d": 4,"l": 4,"c": 2,"f": 2,"g": 2,"m": 2,"u": 2,"w": 2,"b": 1,"p": 1,"y": 1 }
  count = 0
  for c in lfe:
    if cc.get(c,0) >= lfe[c]/float(100):
      count += 1
    if count > 2:
      return True
  return False

def fcxor(ct): # find one character xor

  for x in range(256):
    mesg = list()
    chars = dict()
    lct = len(ct)

    for i in range(lct):
      c = chr(x^ord(ct[i]))
      mesg.append(c)
      chars[c.lower()] = chars.get(c.lower(),0) + 1

      if not c in string.printable:
        break

    if len(mesg) == lct:
      for c in chars:
        chars[c] = round(chars[c]/float(lct),2)
      if chars.get(' ',0) > 0.1 and lfet(chars):
        return (x,"".join(mesg))

if __name__ == '__main__':
  ct = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
  print fcxor(ct.decode('hex'))
