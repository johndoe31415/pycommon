#!/usr/bin/python3
#
#	SyncAverager - Calculate an average over a time interval
#	Copyright (C) 2011-2013 Johannes Bauer
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
#	File UUID 04e2811c-5dd5-4338-a9b1-fe7c5b95cc40

import time
import random

class SyncAverager():
	def __init__(self, **kwargs):
		self._interval = kwargs.get("interval", 60)
		self._maxpts = kwargs.get("maxpts", 200)
		self._data = [ ]
		assert(self._maxpts >= 10)

	def _thindata(self):
		# Delete oldest data points first
		oldest = time.time() - self._interval		
		while (len(self._data) > 0) and (self._data[0][0] < oldest):
			self._data.pop(0)

		while len(self._data) > self._maxpts:
			rindex = random.randint(0, len(self._data) - 1)
			self._data.pop(rindex)

		assert(len(self._data) <= self._maxpts)

	def datapoint(self, value):
		now = time.time()
		self._data.append((now, value))
		self._thindata()

	def average(self, unavailable = None):
		if len(self._data) < 2:
			return unavailable
		else:
			(t0, v0) = self._data[0]
			(t1, v1) = self._data[-1]
			tdiff = t1 - t0
			vdiff = v1 - v0
			if abs(tdiff) < 1e-3:
				return unavailable
			return vdiff / tdiff

	def reset(self):
		self._data = [ ]

if __name__ == "__main__":
	savg = SyncAverager(interval = 3, maxpts = 10)

	foo = 500
	for i in range(100):
		foo += 10
		savg.datapoint(foo)
		print(savg.average())
		time.sleep(0.1)

