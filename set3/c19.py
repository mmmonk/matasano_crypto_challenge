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
for c in "TAISOCMFPWtaisocmfpw":
  key[0] = ord(cts[0][0])^ord(c)
  revt = [ chr(ord(c1)^key[0]) for c1 in rev[0]]
  good = True
  for i in range(milen):
    if not revt[i] in string.letters:
      good = False
      break
  if good == True:
    break

# finding bigrams
for i in range(1,milen-1):
  pass

### init ncurses and do manual guessing
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
curses.curs_set(0)
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_RED, -1)
x = 0
y = 0
try:
  while True:
    stdscr.addstr(0,0,"("+str(x)+","+str(y)+") - press ctrl+c to exit\n\n")
    for ct in cts:
      out = "".join([ chr(ord(c1)^c2) for (c1,c2) in zip(ct,key)])
      stdscr.addstr(hideunprintablechars(out)+"\n")

    # this prints the current value for the key in hex format
    pkey = "".join([ chr(k1) for k1 in key])
    stdscr.addstr("\nkey (hex): "+str(pkey).encode('hex')+"\n")

    # this highlights the current column and current character
    for i in range(lcts):
      stdscr.addstr(i+2,x,chr(stdscr.inch(i+2,x) & 0xff),curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(y+2,x,chr(stdscr.inch(y+2,x) & 0xff),curses.color_pair(1) | curses.A_REVERSE)

    # highligth the current key value that we are modifying
    stdscr.addstr(lcts+3,(x*2)+11,chr(stdscr.inch(lcts+3,(x*2)+11) & 0xff),curses.color_pair(1))
    stdscr.addstr(lcts+3,(x*2)+12,chr(stdscr.inch(lcts+3,(x*2)+12) & 0xff),curses.color_pair(1))

    # refresh the screen
    stdscr.refresh()

    # wait for input
    c = stdscr.getch()

    # normal moving around the screen
    if c == curses.KEY_LEFT:
      x = (x - 1) % mxlen
    elif c == curses.KEY_RIGHT:
      x = (x + 1) % mxlen
    elif c == curses.KEY_UP:
      y = (y - 1) % lcts
    elif c == curses.KEY_DOWN:
      y = (y + 1) % lcts
    elif c == curses.KEY_MOUSE:
      pass
    # modifiying the key
    else:
      try:
        key[x] = ord(cts[y][x])^c
      except:
        pass

except KeyboardInterrupt:
  pass

### cleanup terminal after ncurses
curses.curs_set(1)
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
