#!/usr/bin/env python

import base64
import c18

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

key = open("/dev/urandom").read(16)

for msg in msgs.split("\n"):
  print c18.ctrencrypt(base64.b64decode(msg),0,key).encode('hex')
