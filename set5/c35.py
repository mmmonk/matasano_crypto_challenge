#!/usr/bin/env python

import c33 # DH
import c10 # CBC mode
import c28 # SHA1

import random

def exchange(p,g,Mallory=False,mg=0):

  # A->B            Send "p", "g"
  # B->A            Send ACK

  # with Mallory, M would send NACK to Alice suggesting new p and g values
  # and would send the same weak values to Bob, assuming there is no
  # check on weak values, the communications would be screwed

  if Mallory:
    g = mg

  Alice = c33.dh(random.randint(0,10000),p,g)

  # A->B            Send "p", "g", "A"
  Bob = c33.dh(random.randint(0,10000),p,g)
  Bob_secret = Bob.shsecret(Alice.A)

  # B->A            Send "B"
  Alice_secret = Alice.shsecret(Bob.A)

  # on Alice
  Alice_msg = "Alice says Hi"
  Alice_iv = open("/dev/urandom").read(16)
  Alice_enc = c10.cbcencrypt(Alice_msg,Alice_iv,c28.sha1(str(Alice_secret)).digest()[:16])
  print "msg Alice send: "+Alice_msg

  # A->B            Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
  if Mallory:
    print "Mallory intercepts:",
    if g == 1:
      print c10.cbcdecrypt(Alice_enc,Alice_iv,c28.sha1(str(1)).digest()[:16])
    elif g == p:
      print c10.cbcdecrypt(Alice_enc,Alice_iv,c28.sha1(str(0)).digest()[:16])
    elif g == p - 1:
      try:
        msg = c10.cbcdecrypt(Alice_enc,Alice_iv,c28.sha1(str(1)).digest()[:16])
      except:
        msg = c10.cbcdecrypt(Alice_enc,Alice_iv,c28.sha1(str(p-1)).digest()[:16])
      print msg
    else:
      print ""

  # on Bob
  print "msg Bob received: "+c10.cbcdecrypt(Alice_enc,Alice_iv,c28.sha1(str(Bob_secret)).digest()[:16])
  Bob_msg = "Bob says Hi"
  Bob_iv = open("/dev/urandom").read(16)
  Bob_enc = c10.cbcencrypt(Bob_msg,Bob_iv,c28.sha1(str(Bob_secret)).digest()[:16])
  print "msg Bob send: "+Bob_msg
  # B->A            Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv

  if Mallory:
    print "Mallory intercepts:",
    if g == 1:
      print c10.cbcdecrypt(Bob_enc,Bob_iv,c28.sha1(str(1)).digest()[:16])
    elif g == p:
      print c10.cbcdecrypt(Bob_enc,Bob_iv,c28.sha1(str(0)).digest()[:16])
    elif g == p - 1:
      try:
        msg = c10.cbcdecrypt(Bob_enc,Bob_iv,c28.sha1(str(1)).digest()[:16])
      except:
        msg = c10.cbcdecrypt(Bob_enc,Bob_iv,c28.sha1(str(p-1)).digest()[:16])
      print msg
    else:
      print ""

  # on Alice
  print "msg Alice received: "+c10.cbcdecrypt(Bob_enc,Bob_iv,c28.sha1(str(Alice_secret)).digest()[:16])

if __name__ == "__main__":

  p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
  g = 2
  print "############### normal exchange"
  exchange(p,g)
  print "\n############### Mallory g = 1 KEY is 1"
  exchange(p,g,True,1)
  print "\n############### Mallory g = p KEY is 0"
  exchange(p,g,True,p)
  print "\n############### Mallory g = p - 1 KEY is either p - 1 or 1"
  exchange(p,g,True,p-1)

