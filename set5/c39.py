#!/usr/bin/env python

import Crypto.Util.number
from c36 import i2s, s2i

'''
https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
https://en.wikipedia.org/wiki/RSA_%28algorithm%29
'''

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

def invmod(a, m):
  '''
  https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
  '''
  g, x, y = egcd(a, m)
  if g != 1:
    return None
  else:
    return x % m

class RSA:

  def keygen(self, l=2048, s=True):
    while True:
      p = Crypto.Util.number.getPrime(l)
      q = Crypto.Util.number.getPrime(l)
      n = p * q
      et = (p - 1) * (q - 1)
      if s == True:
        e = 2**16+1 # << - this is better
      else:
        e = 3  # << - this is bad
      d = invmod(e, et)
      if d != None:
        break

    return (e, n), (d, n)

  def encrypt(self, m, (e,n)):
    len_n = len(i2s(n))-1
    len_m = len(m)
    if len_n > len_m:
      return [i2s(pow(s2i(m), e, n))]
    else:
      cs = []
      i = 0
      while len_n*i < len_m:
        cs.append(i2s(pow(s2i(m[len_n*i:len_n*(i+1)]), e, n)))
        i += 1
      return cs

  def decrypt(self, cs, (d,n)):
    m = ""
    for c in cs:
      m += i2s(pow(s2i(c), d, n))
    return m

if __name__ == "__main__":

  k1,k2 = RSA().keygen()
  cleartext  = "this is just a test of a message that will be encrypted using RSA private/public key cryptography, lets try something very long to see how this may woRk.\
 We may also try to add some random things here and here, and here. Just a test like I said,"
  #cleartext = open("c39.py").read() # <<-- this also works, but this actually needs padding
  print cleartext
  ciphertext = RSA().encrypt(cleartext,k1)
  print ciphertext
  decryptedtext = RSA().decrypt(ciphertext,k2)
  print decryptedtext

