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

#def egcd(a,b):
#  '''
#  the recursive function breaks on large values of a and b
#  https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
#  '''
#  if a == 0:
#    return (b, 0, 1)
#  else:
#    g, y, x = egcd(b % a, a)
#    return (g, x - (b//a) * y ,y)

def egcd(a, b):
  '''
  https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
  '''
  x,y, u,v = 0,1, 1,0
  while a != 0:
    q,r = b//a, b%a
    m,n = x-u*q,y-v*q
    b,a, x,y, u,v = a,r, u,v, m,n
  return b, x, y

def invmod(a,m):
  '''
  https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
  '''
  g, x, y = egcd(a, m)
  if g != 1:
    return None
  else:
    return x % m

class RSA:

  def keygen(self,l=2048):
    while True:
      p = Crypto.Util.number.getStrongPrime(l)
      q = Crypto.Util.number.getStrongPrime(l)
      n = p * q
      et = (p-1)*(q-1)
      #e = Crypto.Util.number.getStrongPrime(l) # << - this is good
      e = 3  # << - this is bad
      d = invmod(e,et)
      if d != None:
        break

    return (e,n),(d,n)

  def encrypt(self,m,(e,n)):
    m = int(m.encode('hex'),16)
    return i2s(pow(m,e,n))

  def decrypt(self,c,(d,n)):
    c = int(c.encode('hex'),16)
    return i2s(pow(c,d,n))

if __name__ == "__main__":

  k1,k2 = RSA().keygen()
  cleartext  = "this is just a test of a message"
  print cleartext
  ciphertext = RSA().encrypt(cleartext,k1)
  print ciphertext.encode('string_escape')
  decryptedtext = RSA().decrypt(ciphertext,k2)
  print decryptedtext.encode('string_escape')

