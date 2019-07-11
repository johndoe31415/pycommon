#!/usr/bin/python3
#
#	AESDMH - Implementation of the AES-Davies-Meyer hash algorithm.
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
#	File UUID cbaa7c26-6e3b-472e-831e-01a3bfdf06f4

import collections
import Crypto.Cipher.AES

_CipherSpec = collections.namedtuple("CipherSpec", [ "module", "blocksize", "keylen" ])

class DMH():
	_KNOWN_CIPHERS = {
		"AES128":	_CipherSpec(module = getattr(Crypto.Cipher, "AES", None), blocksize = 16, keylen = 16),
		"AES192":	_CipherSpec(module = getattr(Crypto.Cipher, "AES", None), blocksize = 16, keylen = 24),
		"AES256":	_CipherSpec(module = getattr(Crypto.Cipher, "AES", None), blocksize = 16, keylen = 32),
	}

	def __init__(self, blockcipher, iv = None):
		if blockcipher not in DMH._KNOWN_CIPHERS:
			raise Exception("Cipher '%s' is not known." % (blockcipher))
		self._cipher = DMH._KNOWN_CIPHERS[blockcipher]
		if self._cipher.module is None:
			raise Exception("Cipher '%s' is not imported (maybe crypto module missing?)" % (blockcipher))

		if iv is None:
			self._iv = bytes([ 0xff ] * self._cipher.blocksize)
		else:
			self._iv = iv
			assert(isinstance(iv, bytes))
			assert(len(iv) == self._cipher.blocksize)
		self.reset()
	
	def reset(self):
		self._bitlength = 0
		self._block = self._iv
		return self
	
	def _update_block(self, datablock):
		assert(isinstance(datablock, bytes))
		assert(len(datablock) == self._cipher.blocksize)
		self._bitlength += (8 * len(datablock))
		engine = self._cipher.module.new(key = datablock)
		cipherblock = engine.encrypt(self._block)
		self._block = bytes([ self._block[i] ^ cipherblock[i] for i in range(self._cipher.blocksize) ])

	def finalize(self):
		bitblock = bytes([ (self._bitlength & (0xff << (i * 8))) >> (i * 8) for i in range(self._cipher.blocksize -1, -1, -1) ])
		self._update_block(bitblock)
		self._bitlength = None
		return self

	def update(self, data):
		if (len(data) % self._cipher.blocksize) != 0:
			raise Exception("Blocksize %d" % (self._cipher.blocksize))
		for i in range(0, len(data), self._cipher.blocksize):
			self._update_block(data[i : i + self._cipher.blocksize])
		return self

	def digest(self):
		assert(self._bitlength is None)
		return self._block


if __name__ == "__main__":
	hfnc = DMH("AES256")
	print(hfnc.finalize().digest())
#	print(hfnc.reset().update(b"\x00" * 16).finalize().digest())
#	print(hfnc.reset().update(b"\x00" * 32).finalize().digest())
