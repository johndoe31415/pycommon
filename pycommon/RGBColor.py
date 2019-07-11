#!/usr/bin/python3
#
#	RGBColor - Simple RGB color abstraction
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
#	File UUID debfabc7-91a4-448f-89e4-bc9a5caeec5a

import colorsys

class RGBColor(object):
	def __init__(self, r, g, b):
		self._r = r
		self._g = g
		self._b = b

	@property
	def bytetuple(self):
		return (round(255 * self._r), round(255 * self._g), round(255 * self._b))
	
	@property
	def hexstr(self):
		return "#%02x%02x%02x" % self.bytetuple

	@property
	def lightness(self):
		return (self._r + self._g + self._b) / 3

	def __int__(self):
		(r, g, b) = self.bytetuple
		return (r << 16) | (g << 8) | b


	@classmethod
	def frombyte(cls, r, g, b):
		return RGBColor(r / 255, g / 255, b / 255)
