#!/usr/bin/env python

from c36 import SRP_server
from select import select
import socket
import os
import sys

if __name__ == "__main__":
  NISTprime = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff

  s = SRP_server(NISTprime,2,3,'a@a.com','abc')

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.bind(("127.0.0.1", 9001))
  server.setblocking(False)
  server.listen(1)

  while 1:
    accept,[],[] = select([server],[],[],60)

    if server in accept:
      conn,addr = server.accept()

      if os.fork() == 0:
        data = conn.recv(4096)
        I,A = data.split(",")
        s.recv1(I,int(A))
        salt,B = s.send1()
        conn.send(str(salt)+","+str(B))
        data = conn.recv(4096)
        status = s.recv2(data)
        conn.send(status)
        sys.exit() # killing the child

    # cleaning old children
    try:
      os.waitpid(0,os.WNOHANG)
    except OSError:
        pass
