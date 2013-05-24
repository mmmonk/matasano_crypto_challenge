#!/usr/bin/env python

import c28
import random
import struct

class sha1ext(c28.sha1):

  def extlen(self,orghash,msglen,imsg):

    hs = struct.unpack(">IIIII",orghash.decode('hex'))

    self.h0 = hs[0]
    self.h1 = hs[1]
    self.h2 = hs[2]
    self.h3 = hs[3]
    self.h4 = hs[4]

    self.mesg = imsg
    tempmsg = c28.padding(msglen)+imsg
    self.lmsg = msglen + len(tempmsg)
    return tempmsg

def random_line(afile):
  line = next(afile)
  for num, aline in enumerate(afile):
    if random.randrange(num + 2): continue
    line = aline
  return line.strip()+"::"

if __name__ == "__main__":
  try:
    key = random_line(open("/usr/share/dict/words"))
  except:
    print "can't open /usr/share/dict/words will use secret word \"secret\""
    key = "secret"

  msg = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
  orghash = c28.sha1(key+msg).hexdigest()
  print orghash+" => "+key+msg

  msg2add = ";admin=true"
  att = sha1ext()
  add = att.extlen(orghash,len(key+msg),msg2add)
  print att.hexdigest()
  print c28.sha1(key+msg+add).hexdigest()+" => "+key+msg+add.encode('string_escape')
