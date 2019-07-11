#!/usr/bin/python3
#
#	BaseConversion - Integer conversion between bases.
#	Copyright (C) 2011-2014 Johannes Bauer
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
#	File UUID c1e18706-9643-43d2-b11d-b2ba96965b65

class BaseConversion(object):
	def __init__(self, *digits):
		if len(digits) < 2:
			raise Exception("There need to be at least two digits.")
		if any([ not isinstance(digit, str) for digit in digits ]):
			raise Exception("All digits must be strings.")
		if any([ len(digits[0]) != len(digit) for digit in digits ]):
			raise Exception("All digits must have the same length.")
		self._digits = tuple(digits)
		self._digittoint = { digit: index for (index, digit) in enumerate(self._digits) }
		if len(self._digits) != len(self._digittoint):
			raise Exception("Duplicate digits aren't allowed.")

	@property
	def base(self):
		return len(self._digits)

	@property
	def digitlen(self):
		return len(self._digits[0])

	def tobase(self, value, padtolen = None):
		if not isinstance(value, int):
			raise Exception("Can only convert integer values to base")

		negative = value < 0
		if negative:
			value = -value
			
		digits = [ ]
		while value != 0:
			nextdigit = value % self.base
			value = value // self.base
			digits.append(self._digits[nextdigit])

		if len(digits) == 0:
			digits.append(self._digits[0])

		if (padtolen is not None) and (len(digits) < padtolen):
			padlen = padtolen - len(digits)
			digits = digits + ([ digits[0] ] * padlen)

		if negative:
			digits.append("-")
			
		digits = digits[::-1]
		return "".join(digits)

	def toint(self, value, errors = "raise"):
		if not isinstance(value, str):
			raise Exception("Can only convert strings to integers")
		if errors not in [ "raise", "ignore" ]:
			raise Exception("'errors' keyword must be either 'raise' or 'ignore'")

		negative = (value[0] == "-")
		if negative:
			value = value[1:]

		sumvalue = 0
		index = 0
		while index < len(value):
			nextdigit = value[index : index + self.digitlen]
			digitvalue = self._digittoint.get(nextdigit)
			if (digitvalue is None):
				if errors == "raise":
					raise Exception("'%s' is not a valid digit." % (nextdigit))
				index += 1
				continue
			sumvalue = (sumvalue * self.base) + digitvalue
			index += self.digitlen

		if negative:
			sumvalue = -sumvalue
		return sumvalue

def alphabaseconverter(alphabet):
	return BaseConversion(*[ digit for digit in alphabet ])

def namedbaseconverter(name):
	if name == "bin":
		return alphabaseconverter("01")
	elif name == "oct":
		return alphabaseconverter("01234567")
	elif name == "hex":
		return alphabaseconverter("0123456789abcdef")
	raise Exception("Unknown base '%s'" % (name))

if __name__ == "__main__":
	bconv = namedbaseconverter("hex")

	for i in range(3000):
		x = bconv.tobase(i)
		assert(x == hex(i)[2:])
		y = bconv.toint(x)
		assert(y == i)



