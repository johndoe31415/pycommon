#!/usr/bin/python3
#
#	TempFile - Simple temporary file abstraction with cleanup.
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
#	File UUID 2bf63bf0-d909-4fd8-b06d-0895e46c02e0

import os
import random
import string
import shutil

class TempFile():
	def __init__(self, **kwargs):
		path = kwargs.get("path", "/tmp/")
		self._path = path
		if not self._path.endswith("/"):
			self._path += "/"
		self._prefix = kwargs.get("prefix", "pytmp_")
		self._suffix = kwargs.get("suffix", "")
		self._directory = kwargs.get("directory", False)
		if not self._suffix.endswith("/") and self._directory:
			self._suffix += "/"
		self._filename = self._gennonexistingfilename()

	def _notexists(self, filename):
		try:
			os.stat(filename)
		except OSError as e:
			if e.errno == 2:
				return True
		return False

	def _maywrite(self, filename):
		if not self._directory:
			try:
				f = open(filename, "w")
			except IOError:
				return False
			f.close()
			os.unlink(filename)
			return True
		else:
			try:
				os.mkdir(filename)
			except IOError:
				return False
			return True

	def _genfilename(self):
		alphabet = string.ascii_lowercase + string.digits
		length = 20
		return self._path + self._prefix + "".join([ alphabet[random.randint(0, len(alphabet) - 1)] for i in range(length) ]) + self._suffix

	def _gennonexistingfilename(self):
		for i in range(100):
			filename = self._genfilename()
			if (self._notexists(filename)) and self._maywrite(filename):
				return filename
		raise Exception("Could not create a tempfile in %s" % (self._path))

	def cleanup(self):
		try:
			if not self._directory:
				os.unlink(self.filename)
			else:
				shutil.rmtree(self.filename, ignore_errors = True)
		except OSError:
			pass

	def __str__(self):
		return "TempFile<" + self._filename + ">"
	
	def __enter__(self):
		pass

	def __exit__(self, type, value, traceback):
		self.cleanup()

	@property
	def filename(self):
		return self._filename

if __name__ == "__main__":
	import time

	x = TempFile()
	with x:
		with x:
			f = open(x.filename, "w")
			f.write("FOO")
			print(x.filename)


	y = TempFile(directory = True)
	with y:
		print(y.filename)
		time.sleep(100)
