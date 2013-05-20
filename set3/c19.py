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

class gui:

  def __init__(self,cts,key,addx=0,addy=2):
    self.stdscr = curses.initscr()
    self.stdscr.keypad(1)
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.noecho()
    curses.cbreak()
    self.x = 0
    self.y = 0
    self.addx = addx
    self.addy = addy
    self.cts = cts
    self.limity = len(self.cts)
    self.key = key
    self.limitx = len(self.key)

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
    # we need to ignore some keypresses
    elif c == curses.KEY_MOUSE:
      pass
    elif c < 32 or c == 127 or c > 255:
      curses.flash()
    else:
      # modifiying the encryption key
      try:
        self.key[self.x] = ord(self.cts[self.y][self.x])^c
      except:
        pass

  def display(self):

    self.stdscr.addstr(0,0,"cur:("+str(self.x)+","+str(self.y)+") max:("+str(self.limitx)+","+str(self.limity)+") - press ctrl+c to exit\n\n")
    for ct in self.cts:
      self.stdscr.addstr(hideunprintablechars(xors(ct,self.key))+"\n")

    # this prints the current value for the key in hex format
    pkey = "".join([ chr(k1) for k1 in self.key])
    self.stdscr.addstr("\nkey (hex): "+str(pkey).encode('hex')+"\n")

    # this highlights the current column and current character
    for i in range(self.limity):
      self.stdscr.addstr(i+self.addy,self.x,chr(self.stdscr.inch(i+self.addy,self.x) & 0xff),curses.color_pair(1) | curses.A_BOLD)
    self.stdscr.addstr(self.y+self.addy,self.x,chr(self.stdscr.inch(self.y+self.addy,self.x) & 0xff),curses.color_pair(1) | curses.A_REVERSE)

    # highligth the current key value that we are modifying
    self.stdscr.addstr(self.limity+3,(self.x*2)+11,chr(self.stdscr.inch(self.limity+3,(self.x*2)+11) & 0xff),curses.color_pair(1))
    self.stdscr.addstr(self.limity+3,(self.x*2)+12,chr(self.stdscr.inch(self.limity+3,(self.x*2)+12) & 0xff),curses.color_pair(1))

    # refresh the screen
    self.stdscr.refresh()

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


#### breaking it

# prepare the key
key = [0]*mxlen

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
    if not revt[i] in string.letters+" ":
      good = False
      break
  if good == True:
    break


# finding bigrams
bigrams = ( "th", "he", "in", "er",
"an", "re", "nd", "on",
"en", "at", "ou", "ed",
"ha", "to", "or", "it",
"is", "hi", "es", "ng")

for i in range(0,milen):
  if key[i] == "\x00":
    pass

# finding trigrams
trigrams = ( "the", "and", "ing", "her",
"hat", "his", "tha", "ere",
"for", "ent", "ion", "ter",
"was", "you", "ith", "ver",
"all", "wit", "thi", "tio")

quadrigrams = ( "that", "ther", "with", "tion",
"here", "ould", "ight", "have",
"hich", "whic", "this", "thin",
"they", "atio", "ever", "from",
"ough", "were", "hing", "ment")

### manual guessing

g = gui(cts,key)
g.run()
