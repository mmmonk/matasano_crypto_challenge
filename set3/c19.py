#!/usr/bin/env python

import base64
import c18
import c3
import string
import curses

def hideunprintablechars(s,hc="#"):
  s = list(s)
  for i in range(len(s)):
    if not s[i] in string.printable:
      s[i] = hc
    if s[i] in string.whitespace:
      s[i] = " "
  return "".join(s)

def xors(s1,s2):
  return "".join([ chr(ord(c1)^c2) for (c1,c2) in zip(s1,s2)])

def checkkey(cts,k,i):

  countspecial = 0
  for ct in cts:
    try:
      c = chr(ord(ct[i])^k[i])
    except:
      c = " "
    if not c in string.printable:
      return False
    if c in string.punctuation:
      countspecial += 1
    if c in "#*~`{}[]|":
      return False

  if countspecial > len(cts)*0.2:
    return False
  return True


def basicautoguessing(cts,key,milen):

  lcts = len(cts)

  # do some basic automating guesses
  rev = range(milen)
  for i in range(milen):
    rev[i] = list()

  for i in range(lcts):
    ct = cts[i]
    for j in range(milen):
      rev[j].append(ct[j])

  for i in range(milen):
    out = c3.fcxor(rev[i])
    if out != None:
      key[i] = out[0]

  # finding the first letter (based on the most common ones):
  # from http://www.cryptograms.org/letter-frequencies.php
  for c in "TAISOCMFPWtaisocmfpw ":
    key[0] = ord(cts[0][0])^ord(c)
    revt = [ chr(ord(c1)^key[0]) for c1 in rev[0]]
    good = True
    for i in range(milen):
      if not revt[i] in string.letters+" '":
        good = False
        break
    if good == True:
      break

  return key

def bigrams(cts,key):

  # finding bigrams
  bigrams = ( "th", "he", "in", "er",
  "an", "re", "nd", "on",
  "en", "at", "ou", "ed",
  "ha", "to", "or", "it",
  "is", "hi", "es", "ng",
  ' t', ' a', ' i', ' s',
  ' o', ' c', ' m', ' f',
  ' p', ' w')

  for i in range(len(key)):
    if key[i] == 0:
      for ct in cts:
        try:
          c = ct[i]
        except:
          continue
        pre = chr(ord(ct[i-1])^key[i-1])
        suf = chr(ord(ct[i+1])^key[i+1]) if i < len(ct)-1 else ""
        found = False
        for bi in bigrams:
          if bi[0] == pre:
            k = key[:]
            k[i] = ord(c)^ord(bi[1])
            if checkkey(cts,k,i):
              found = True
              key = k[:]
              break
          elif bi[1] == suf:
            k = key[:]
            k[i] = ord(c)^ord(bi[0])
            if checkkey(cts,k,i):
              found = True
              key = k[:]
              break
        if found:
          break

  return key

def trigrams(cts,key):

  # finding trigrams
  trigrams = ( "the", "and", "ing", "her",
  "hat", "his", "tha", "ere",
  "for", "ent", "ion", "ter",
  "was", "you", "ith", "ver",
  "all", "wit", "thi", "tio")

  for i in range(1,len(key)):
    if key[i] == 0:
      for ct in cts:
        try:
          c = ct[i]
        except:
          continue
        pre = chr(ord(ct[i-1])^key[i-1])
        suf = chr(ord(ct[i+1])^key[i+1]) if i < len(ct)-1 else ""
        found = False
        for tri in trigrams:
          if tri[0] == pre and tri[2] == suf:
            k = key[:]
            k[i] = ord(c)^ord(tri[1])
            if checkkey(cts,k,i):
              found = True
              key = k[:]
              break
        if i > 1:
          pre = chr(ord(ct[i-2])^key[i-2])
          suf = chr(ord(ct[i-1])^key[i-1])
          found = False
          for tri in trigrams:
            if tri[0] == pre and tri[1] == suf:
              k = key[:]
              k[i] = ord(c)^ord(tri[2])
              if checkkey(cts,k,i):
                found = True
                key = k[:]
                break
        if i < len(ct)-2:
          pre = chr(ord(ct[i+1])^key[i+1])
          suf = chr(ord(ct[i+2])^key[i+2])
          found = False
          for tri in trigrams:
            if tri[1] == pre and tri[2] == suf:
              k = key[:]
              k[i] = ord(c)^ord(tri[0])
              if checkkey(cts,k,i):
                found = True
                key = k[:]
                break
        if found:
          break

  return key

def quadrigrams(cts,key):

  quadrigrams = ( "that", "ther", "with", "tion",
  "here", "ould", "ight", "have",
  "hich", "whic", "this", "thin",
  "they", "atio", "ever", "from",
  "ough", "were", "hing", "ment")

  return key

class gui:
  '''
  a class for manual correction ;)
  '''
  def __init__(self,cts,key):
    self.x = 0
    self.y = 0
    self.pos = 0
    self.cts = cts
    self.limity = len(self.cts)
    self.key = key
    self.limitx = len(self.key)
    self.winscr = curses.initscr()
    self.maxy,self.maxx = self.winscr.getmaxyx()
    self.maxy -= 1
    self.maxx -= 1
    self.stdscr = curses.newpad(self.limity+100,self.limitx*2+20)
    self.stdscr.keypad(1)
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.noecho()
    curses.cbreak()

  def getkey(self):

    c = self.stdscr.getch()

    # normal moving around the screen
    if c == curses.KEY_LEFT:
      self.x = (self.x - 1) % self.limitx
    elif c == curses.KEY_RIGHT:
      self.x = (self.x + 1) % self.limitx
    elif c == curses.KEY_UP:
      self.y = (self.y - 1) % self.limity
    elif c == curses.KEY_DOWN:
      self.y = (self.y + 1) % self.limity
    elif c == curses.KEY_NPAGE:
      self.pos = (self.pos + self.maxy) % self.limity
    elif c == curses.KEY_PPAGE:
      self.pos = (self.pos - self.maxy) % self.limity
    elif c == curses.KEY_HOME:
      self.pos = 0
    # we need to ignore some keys
    elif c == curses.KEY_MOUSE:
      pass
    elif c < 32 or c == 127 or c > 255:
      curses.flash()
    else:
      # modifying the encryption key
      try:
        self.key[self.x] = ord(self.cts[self.y][self.x])^c
      except:
        pass

  def display_footer(self):

    # print the current value for the key in hex format
    pkey = "".join([ chr(k1) for k1 in self.key])
    self.stdscr.addstr("\nkey (hex): "+str(pkey).encode('hex')+"\n\n")

    # print current position of the cursor and its limits
    self.stdscr.addstr("cur:("+str(self.x)+","+str(self.y)+") max:("+str(self.limitx-1)+","+str(self.limity-1)+") - press ctrl+c to exit\n\n")

    # help
    self.stdscr.addstr("Use arrows to move around, at chosen position press key\n\
that you think should be there in a clear text,\nbased on this the key value will be calculated\n\
and all other ciphertext will be recalculated.\nPGDWN and PGUP scroll the whole page. HOME resets.")

  def display(self):
    # always start from top left corner
    self.stdscr.addstr(0,0,"")

    # print what we have so far
    for ct in self.cts:
      self.stdscr.addstr(hideunprintablechars(xors(ct,self.key))+"\n")

    self.display_footer()

    # highlight the current column and current character
    for i in range(self.limity):
      self.stdscr.addstr(i,self.x,chr(self.stdscr.inch(i,self.x) & 0xff),curses.color_pair(1) | curses.A_BOLD)
    self.stdscr.addstr(self.y,self.x,chr(self.stdscr.inch(self.y,self.x) & 0xff),curses.color_pair(1) | curses.A_REVERSE)

    # highlight the current key value that we are modifying
    self.stdscr.addstr(self.limity+1,(self.x*2)+11,chr(self.stdscr.inch(self.limity+1,(self.x*2)+11) & 0xff),curses.color_pair(1))
    self.stdscr.addstr(self.limity+1,(self.x*2)+12,chr(self.stdscr.inch(self.limity+1,(self.x*2)+12) & 0xff),curses.color_pair(1))

    # refresh the screen
    self.stdscr.refresh(self.pos,0,0,0,self.maxy,self.maxx)

  def run(self):
    # the main function

    try:
      while True:
        self.display()
        self.getkey()

    except KeyboardInterrupt:
      pass

    ### cleanup terminal after ncurses
    self.stdscr.keypad(0)
    curses.curs_set(1)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == "__main__":

  msgs = "SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==\n\
Q29taW5nIHdpdGggdml2aWQgZmFjZXM=\n\
RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==\n\
RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=\n\
SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk\n\
T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==\n\
T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=\n\
UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==\n\
QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=\n\
T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl\n\
VG8gcGxlYXNlIGEgY29tcGFuaW9u\n\
QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==\n\
QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=\n\
QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==\n\
QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=\n\
QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=\n\
VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==\n\
SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==\n\
SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==\n\
VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==\n\
V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==\n\
V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==\n\
U2hlIHJvZGUgdG8gaGFycmllcnM/\n\
VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=\n\
QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=\n\
VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=\n\
V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=\n\
SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==\n\
U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==\n\
U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=\n\
VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==\n\
QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu\n\
SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=\n\
VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs\n\
WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=\n\
SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0\n\
SW4gdGhlIGNhc3VhbCBjb21lZHk7\n\
SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=\n\
VHJhbnNmb3JtZWQgdXR0ZXJseTo=\n\
QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4="

  #### encrypting above messages
  key = open("/dev/urandom").read(16)
  cts = list()
  mxlen = 0    # max length of the CT
  milen = 999  # min length of the CT
  for msg in msgs.split("\n"):
    cts.append(c18.ctrencrypt(base64.b64decode(msg),0,key))
    l = len(cts[-1])
    if l > mxlen:
      mxlen = l
    if l < milen:
      milen = l

  #### breaking them

  # prepare the key
  key = [0]*mxlen

  # automated guessing
  key = basicautoguessing(cts,key,milen)
  key = bigrams(cts,key)
  key = trigrams(cts,key)
  #key = quadrigrams(cts,key)

  # manual guessing
  g = gui(cts,key)
  g.run()
