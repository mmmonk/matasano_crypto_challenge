#!/usr/bin/env python

from c36 import i2s,s2i
import hashlib
import hmac
import math
import random
import multiprocessing

class sSRP_server :

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
    self.B = (pow(self.g,self.b,self.N))
    self.u = random.randint(2**127,(2**128)-1)

  def send1(self):
    return self.salt,self.B,self.u

  def recv2(self,hks):
    S = pow(self.A * pow(self.v,self.u,self.N),self.b,self.N)
    K = hashlib.sha256(i2s(S)).digest()

    if hks == hmac.HMAC(K,self.salt,hashlib.sha256).digest() and self.I == self.Ic:
      return "OK"
    else:
      return "No way"

class sSRP_client :

  def __init__(self,N,g,k,I,P):
    self.N = N
    self.g = g
    self.k = k
    self.I = I
    self.P = P
    self.a = s2i(open("/dev/urandom").read(2)) # in normal operations this should be bigger
    self.A = pow(self.g,self.a,self.N)

  def send1(self):
    return self.I,self.A

  def recv1(self,salt,B,u):
    self.salt = salt
    x = s2i(hashlib.sha256(self.salt+self.P).digest())
    S = pow(B,(self.a+u*x),self.N)
    self.K = hashlib.sha256(i2s(S)).digest()

  def send2(self):
    return hmac.HMAC(self.K,self.salt,hashlib.sha256).digest()


def testsSRP(N):
  g = 2
  p = 3
  s = sSRP_server(N,g,p,'a@a.com','abc')
  c = sSRP_client(N,g,p,'a@a.com','abc')
  I,A = c.send1()
  s.recv1(I,A)
  salt,B,u = s.send1()
  c.recv1(salt,B,u)
  if s.recv2(c.send2()) == "OK":
    return True
  return False

def tworker1(A,start,step,g,N,q):
  '''
  this BF a
  '''
  a = start
  A_c = 0
  while True:
    A_c = pow(g,a,N)
    if A_c == A:
      q.put(a)
      break
    a += step

def tworker2(hpass,a,words,start,step,g,N,q):
  '''
  dictionary attack
  '''
  i = start
  while i < len(words):
    x = s2i(hashlib.sha256(words[i]).digest())
    S = pow(2,a+x,N)
    K = hashlib.sha256(i2s(S)).digest()
    if hmac.HMAC(K,"",hashlib.sha256).digest() == hpass:
      q.put(words[i])
      break
    i += step

def tworker3(hpass,a,start,step,g,N,q):
  '''
  this BF password
  '''
  sc = ord('a')+start
  ec = ord('z')
  cc = [sc]
  while True:
    h_c = "".join([chr(c) for c in cc])

    x = s2i(hashlib.sha256(h_c).digest())
    S = pow(2,a+x,N)
    K = hashlib.sha256(i2s(S)).digest()

    if hmac.HMAC(K,"",hashlib.sha256).digest() == hpass:
      q.put(h_c)
      break

    cc[0] += step
    for i in range(0,len(cc)):
      if cc[i] > ec:
        try:
          cc[i+1] += 1
        except:
          cc.append(sc)
        cc[i] %= (ec+1)
        cc[i] += sc
      else:
        break


def attack1(A,a0,hpass,g,p,N):
  '''
  simples possible brute force + dictionary attack,
  the only optimization is done via multiprocessing
  '''
  ncpu = multiprocessing.cpu_count()
  q = multiprocessing.Queue()

  print "guessing a"
  mps = []
  for i in range(ncpu):
    mp = multiprocessing.Process(target=tworker1, args=(A,a0+i,ncpu,g,N,q))
    mp.start()
    mps.append(mp)

  while True:
    try:
      a_c = q.get(timeout=1)
      for mp in mps:
        mp.terminate()
    except:
      searching = False
      for mp in mps:
        if mp.is_alive():
          searching = True
      if searching == False:
        break

  print "possible a: "+str(a_c)

  words = list()
  try:
    words = [ w.strip() for w in open("/usr/share/dict/words").readlines()]
  except:
    pass

  print "trying dictionary attack on the password"
  pw = ""
  mps = []
  for i in range(ncpu):
    mp = multiprocessing.Process(target=tworker2, args=(hpass,a_c,words,i,ncpu,g,N,q))
    mp.start()
    mps.append(mp)

  while True:
    try:
      pw = q.get(timeout=1)
      for mp in mps:
        mp.terminate()
    except:
      searching = False
      for mp in mps:
        if mp.is_alive():
          searching = True
      if searching == False:
        break

  if pw == "":
    print "trying brute force attack on the password"
    mps = []
    for i in range(ncpu):
      mp = multiprocessing.Process(target=tworker3, args=(hpass,a_c,i,ncpu,g,N,q))
      mp.start()
      mps.append(mp)

    while True:
      try:
        pw = q.get(timeout=1)
        for mp in mps:
          mp.terminate()
      except:
        searching = False
        for mp in mps:
          if mp.is_alive():
            searching = True
        if searching == False:
          break

  print "possible pass: "+str(pw)

if __name__ == "__main__":

  NISTprime = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff

  if not testsSRP(NISTprime):
    raise Exception("sSRP doesn't work correctly - test failed.")

  # MITM
  g = 2
  p = 3
  c = sSRP_client(NISTprime,g,p,'a@a.com','abc')
  I,A = c.send1()  # <-- MITM captures client I and A
  c.recv1("",2,1)  # <-- MITM sends salt="" B=2 u=1
  client_pass = c.send2() #  <-- client sends HMAC

  a0 = int(math.log(A,g))
  attack1(A,a0,client_pass,g,p,NISTprime)
