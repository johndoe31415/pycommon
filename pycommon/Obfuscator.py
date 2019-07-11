#!/usr/bin/python3
#
#	Obfuscator - Obfuscate and deobfuscate strings or bytes.
#	Copyright (C) 2011-2012 Johannes Bauer
#	
#	This file is part of pycommon.
#
#	pycommon is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pycommon is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pycommon; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>
#
#	File UUID 28238641-7db8-4c9d-af40-3e5259dd3566

import hashlib
import base64
import random

class Obfuscator(object):
	def _genkeystream(bytecnt, key = None):
		if key is None:
			key = "x8kaSVdQsZ"
		if isinstance(key, str):
			key = key.encode("utf-8")

		hashkey = hashlib.md5(key).digest()
		inthashkey = sum([ (hashkey[i] * (256 ** i)) for i in range(len(hashkey)) ])
		#(x, y, z, w) = (123456789, 362436069, 521288629, 88675123)
		(x, y, z, w) = [ (inthashkey & (0xffffffff << (32 * i))) >> (32 * i) for i in range(4) ]

		keystream = [ ]
		while len(keystream) < bytecnt:
			t = (x ^ (x << 11)) & 0xffffffff
			x = y
			y = z
			z = w
			w = ((w ^ (w >> 19)) ^ (t ^ (t >> 8))) & 0xffffffff
			keystream += [ (w & (0xff << (8 * i))) >> (8 * i) for i in range(4) ]
		keystream = keystream[ : bytecnt]
		return keystream

	def _obfuscatebytes(indata, key = None):
		assert(isinstance(indata, bytes))
		stream = Obfuscator._genkeystream(len(indata), key)
		output = bytes([ (indata[i] ^ stream[i]) for i in range(len(indata)) ])
		return output

	def _interleave(indata):
		interleaved = [ ]
		for c in indata:
			interleaved += [ random.randint(0, 255), c ]
		interleaved += [ random.randint(0, 255) ]
		return bytes(interleaved)
	
	def _deinterleave(indata):
		origdatalen = (len(indata) - 1) // 2
		outdata = [ indata[1 + (2 * i) ] for i in range(origdatalen) ]
		return bytes(outdata)

	def obfuscate(indata, key = None):
		inputstring = isinstance(indata, str)
		if inputstring:
			indata = indata.encode("utf-8")
		outdata = Obfuscator._obfuscatebytes(indata, key)
		outdata = Obfuscator._interleave(outdata)
		if inputstring:			
			outdata = base64.b64encode(outdata).decode("utf-8")
		return outdata

	def deobfuscate(indata, key = None):
		inputstring = isinstance(indata, str)
		if inputstring:
			indata = base64.b64decode(indata.encode("utf-8"))
		outdata = Obfuscator._deinterleave(indata)
		outdata = Obfuscator._obfuscatebytes(outdata, key)
		if inputstring:
			outdata = outdata.decode("utf-8")
		return outdata

if __name__ == "__main__":
	import string
	import getpass

	def randstr(l):
		source = string.ascii_letters + string.digits
		return "".join([ source[random.randint(0, len(source) - 1) ] for i in range(l) ])

	for key in [ None, "", randstr(5), randstr(10) ]:
		for textlen in range(32):
			text = randstr(textlen)
			obfuscated = Obfuscator.obfuscate(text, key)
			deobfuscated = Obfuscator.deobfuscate(obfuscated, key)
			assert(text == deobfuscated)

			text = text.encode("utf-8")
			obfuscated = Obfuscator.obfuscate(text, key)
			deobfuscated = Obfuscator.deobfuscate(obfuscated, key)
			assert(text == deobfuscated)

	passwd = getpass.getpass("Password: ")
	print(Obfuscator.obfuscate(passwd))

