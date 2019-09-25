#!/usr/bin/python3
#
#	StatisticalEval - Basic statistics calculation
#	Copyright (C) 2014-2015 Johannes Bauer
#
#	This file is part of jpycommon.
#
#	jpycommon is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	jpycommon is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with jpycommon; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>
#
#	File UUID f61aa4bd-9975-4af0-b97b-9e49644a9815

import numpy

class StatisticalEval(object):
	def __init__(self, values = None):
		if values is None:
			self._values = [ ]
		else:
			self._values = list(values)

	def append(self, value):
		self._values.append(value)

	@property
	def avg(self):
		if len(self) == 0:
			return None
		else:
			return sum(self._values) / len(self)

	@property
	def min(self):
		if len(self) == 0:
			return None
		else:
			return min(self._values)

	@property
	def max(self):
		if len(self) == 0:
			return None
		else:
			return max(self._values)

	@property
	def stddev(self):
		if len(self) == 0:
			return None
		else:
			return numpy.std(self._values)

	def percentile(self, percent):
		if len(self) == 0:
			return None
		else:
			return numpy.percentile(self._values, percent)

	@staticmethod
	def _percentile_minreqs(percentile):
		"""Returns the minimum amount of values required that is necessary to
		determine a somewhat sensible percentile."""
		return 125 / (100 - percentile)

	def percentile_sensible(self, percent):
		return len(self) >= self._percentile_minreqs(percent)

	def dump(self):
		print("Value count         : %d" % (len(self)))
		print("Average             : %.4f" % (self.avg))
		print("Median              : %.4f" % (self.percentile(50)))
		print("Min/Max             : %.4f - %.4f" % (self.min, self.max))
		print("Standard deviation σ: %.4f" % (self.stddev))
		if self.percentile_sensible(95):
			print("95%% percentile      : %.4f" % (self.percentile(95)))
		if self.percentile_sensible(99):
			print("99%% percentile      : %.4f" % (self.percentile(99)))
		if self.percentile_sensible(99.9):
			print("99.9%% percentile    : %.4f" % (self.percentile(99.9)))
		if self.percentile_sensible(99.99):
			print("99.99%% percentile   : %.4f" % (self.percentile(99.99)))

	def write_to_file(self, filename):
		f = open(filename, "w")
		for (index, value) in enumerate(self._values):
			print("%d %.6f" % (index, value), file = f)
		f.close()

	def __len__(self):
		return len(self._values)

	def __str__(self):
		return "Statistics<%d values>" % (len(self))

if __name__ == "__main__":
	import random
	stats = StatisticalEval()
	for i in range(1000000):
		stats.append(random.random())
	stats.dump()
