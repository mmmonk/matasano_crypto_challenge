#!/usr/bin/env python

from c36 import SRP_client,i2s
import hashlib
import hmac
import socket
import os


if __name__ == "__main__":
  NISTprime = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff

  print "Normal login:",
  c = SRP_client(NISTprime,2,3,'a@a.com','abc')
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(("127.0.0.1", 9001))

  I,A = c.send1()
  client.send(str(I)+","+str(A))
  data = client.recv(4096)
  salt,B = data.split(",")
  c.recv1(salt,int(B))
  client.send(c.send2())
  print client.recv(4096)
  client.shutdown(2)

  print "Attack A=0 (because of this S = 0):",

  client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client1.connect(("127.0.0.1", 9001))
  client1.send("a@a.com,0")
  data = client1.recv(4096)
  salt = data.split(",")[0]
  K = hashlib.sha256(i2s(0)).digest()
  client1.send(hmac.HMAC(K,salt,hashlib.sha256).digest())
  print client1.recv(4096)
  client1.shutdown(2)

  print "Attack A=N (because of this S = 0):",

  client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client2.connect(("127.0.0.1", 9001))
  client2.send("a@a.com,"+str(NISTprime))
  data = client2.recv(4096)
  salt = data.split(",")[0]
  K = hashlib.sha256(i2s(0)).digest()
  client2.send(hmac.HMAC(K,salt,hashlib.sha256).digest())
  print client2.recv(4096)
  client2.shutdown(2)

  print "Attack A=N*2 (because of this S = 0):",

  client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client3.connect(("127.0.0.1", 9001))
  client3.send("a@a.com,"+str(NISTprime*2))
  data = client3.recv(4096)
  salt = data.split(",")[0]
  K = hashlib.sha256(i2s(0)).digest()
  client3.send(hmac.HMAC(K,salt,hashlib.sha256).digest())
  print client3.recv(4096)
  client3.shutdown(2)
