#!/usr/bin/env python

import Crypto.Util.number

# https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
# https://en.wikipedia.org/wiki/RSA_%28algorithm%29
# Crypto.Util.number.getStrongPrime

def i2s(i):
  '''
  Simple integer to string conversion
  '''
  x = hex(i).replace("0x","").replace("L","")
  if len(x) % 2 == 1:
    x = "0" + x
  return x.decode('hex')

def egcd(a,b):
  '''
  https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
  '''
  if a == 0:
    return (b, 0, 1)
  else:
    g, y, x = egcd(b % a, a)
    return (g, x - (b//a) * y ,y)

def invmod(a,m):
  '''
  https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
  '''
  g, x, y = egcd(a, m)
  if g != 1:
    return None
  else:
    return x % m

class rsa:

  def keygen(self,n=2048):
    p = Crypto.Util.number.getStrongPrime(n)
    q = Crypto.Util.number.getStrongPrime(n)
    n = p * q
    et = (p-1)*(q-1)
    e = 3  # << - this is bad, this should be a large prime
    # e = Crypto.Util.number.getStrongPrime(n)
    d = invmod(e,et)
    if d == None:
      print "error"

    return (e,n),(d,n)

  def encrypt(self,m,(e,n)):
    m = int(m.encode('hex'),16)
    return i2s(pow(m,e,n))

  def decrypt(self,c,(d,n)):
    c = int(c.encode('hex'),16)
    return i2s(pow(c,d,n))

if __name__ == "__main__":

  k1,k2 = rsa().keygen()
  cleartext  = "this is just a test of a message"
  print cleartext
  ciphertext = rsa().encrypt(cleartext,k1)
  print ciphertext.encode('string_escape')
  decryptedtext = rsa().decrypt(ciphertext,k2)
  print decryptedtext.encode('string_escape')

