#!/usr/bin/env python

import hashlib
import hmac

def i2s(i):
  x = hex(i).replace("0x","").replace("L","")
  if len(x) % 2 == 1:
    x = "0" + x
  return x.decode('hex')

def s2i(s):
  return long(s.encode('hex'),16)

class SRP_server :

  def __init__(self,N,g,k,I,P):
    self.N = N
    self.g = g
    self.k = k
    self.I = I
    self.P = P   # <<- this should not be here in reality, only hash or scrypt/bcrypt should be avalible

  def recv1(self,I,A):
    self.A = A
    self.Ic = I # <<- incoming user, we will compare this after calcualting the recevied HMAC
    self.b = s2i(open("/dev/urandom").read(4)) # <<- random number
    self.salt = open("/dev/urandom").read(4) # <<- should be taken from a db
    x = s2i(hashlib.sha256(self.salt+self.P).digest())  # <<- this should be taken from a DB, although maybe scrypt/bcrypt/sth similar ?
    self.v = pow(self.g,x,self.N)
    self.B = (self.k*self.v)+(pow(self.g,self.b,self.N))

  def send1(self):
    return self.salt,self.B

  def recv2(self,hks):
    u = s2i(hashlib.sha256(i2s(self.A)+i2s(self.B)).digest())
    S = pow(self.A * pow(self.v,u,self.N),self.b,self.N)
    K = hashlib.sha256(i2s(S)).digest()

    if hks == hmac.HMAC(K,self.salt,hashlib.sha256).digest() and self.I == self.Ic:
      return "OK"
    else:
      return "No way"

class SRP_client :

  def __init__(self,N,g,k,I,P):
    self.N = N
    self.g = g
    self.k = k
    self.I = I
    self.P = P
    self.a = s2i(open("/dev/urandom").read(4))
    self.A = pow(self.g,self.a,self.N)

  def send1(self):
    return self.I,self.A

  def recv1(self,salt,B):
    self.salt = salt
    u = s2i(hashlib.sha256(i2s(self.A)+i2s(B)).digest())
    x = s2i(hashlib.sha256(self.salt+self.P).digest())
    S = pow(B - self.k * pow(self.g,x,self.N),(self.a+u*x),self.N)
    self.K = hashlib.sha256(i2s(S)).digest()

  def send2(self):
    return hmac.HMAC(self.K,self.salt,hashlib.sha256).digest()

if __name__ == "__main__":

  NISTprime = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff

  s = SRP_server(NISTprime,2,3,'a@a.com','abc')
  c = SRP_client(NISTprime,2,3,'a@a.com','abc')
  I,A = c.send1()
  s.recv1(I,A)
  salt,B = s.send1()
  c.recv1(salt,B)
  print s.recv2(c.send2())

