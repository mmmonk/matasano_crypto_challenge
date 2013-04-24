#!/usr/bin/env python

import string

def fcxor(cte):
  ct = cte.decode('hex')

  for x in range(256):
    mesg = []
    chars = dict()
    lct = len(ct)

    for i in range(lct):
      c = chr(x^ord(ct[i]))
      mesg.append(c)
      chars[c.lower()] = chars.get(c.lower(),0) + 1

      if not c in string.printable or c in '^~\\#@*/{}':
        break

    if len(mesg) == lct:
      for c in chars:
        chars[c] = round(chars[c]/float(lct),2)
      charss = sorted(chars.iteritems(),key=lambda (k,v): (v,k), reverse=True)
      if (charss[0][0] in string.letters or charss[0][0] == " ") and \
      (chars.get('a',0) > 0.07 or chars.get('e',0) > 0.11 or chars.get('n',0) > 0.06 or chars.get('o',0) > 0.06 or chars.get('t',0) > 0.07):
        print "enc:"+cte+" key:"+str(x)+" txt:'"+"".join(mesg)+"'"

if __name__ == '__main__':
  ct = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
  fcxor(ct)
