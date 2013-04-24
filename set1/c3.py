#!/usr/bin/env python

import string

ct = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def fcxor(cte):
  ct = cte.decode('hex')

  for x in range(256):
    mesg = []
    chars = dict()

    for i in range(len(ct)):
      c =  chr(x^ord(ct[i]))
      mesg.append(c)
      chars[c] = chars.get(c,0) + 1

      if not c in string.printable:
        break

      if i + 1 == len(ct):
        charss = sorted(chars.iteritems(),key=lambda (k,v): (v,k), reverse=True)
        if charss[0][0] in string.letters or charss[0][0] == " ":
          print charss
          print cte+" => "+str(x)+" '"+"".join(mesg)+"'"

if __name__ == '__main__':
  fcxor(ct)
