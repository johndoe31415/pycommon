#!/usr/bin/python3
#
#	ColorMixer - Simple color mixer.
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
#	File UUID c5951334-92bb-47a1-933a-d6b16beca294

import bisect

class ColorMixer(object):
	_predef = {
		"rainbow":	[
			(None, 251, 12, 9),
			(None, 249, 108, 52),
			(None, 247, 244, 27),
			(None, 48, 156, 44),
			(None, 28, 14, 128),
			(None, 149, 7, 129),
			(None, 95, 12, 130),
		],
		"bgrmap1": [
			(0.000,   0,  14, 255),
			(0.098,   0, 255, 246),
			(0.202,   4, 255,   0),
			(0.616, 255, 243,   0),
			(1.000, 255,   0,   0),
		],
		"bgrmap2": [
			(0.000,   5,   3, 126),
			(0.126,   1,  11, 254),
			(0.374,   8, 255, 245),
			(0.625, 254, 248,   2),
			(0.879, 243,   0,   2),
			(1.000, 119,   3,   7),
		],
		"bgrmap3": [
			(0.000,   0,   0, 255),
			(0.252,   0, 255, 243),
			(0.492,  10, 255,   0),
			(0.735, 255, 242,   0),
			(0.990, 255,   0,   0),
			(1.000, 255,   0,   0),
		],
		"heatmap1": [
			(0.000, 255, 255, 244),
			(0.116, 255, 255, 154),
			(0.263, 255, 250,   8),
			(1.000, 255,   0,   0),
		],
		"heatmap2": [
			(0.000,   3,   3,   5),
			(0.195,  78,   1, 139),
			(0.450, 195,   7, 182),
			(0.600, 255,  57, 110),
			(0.729, 255, 154,   2),
			(0.857, 255, 244,  28),
			(1.000, 255, 255, 255),
		],
		"traffic": [
			(0,		255,   0,   0),
			(0.5,	255, 255,   0),
			(0.75,	50,  255,   0),
			(1,		42,  159,   15),
		],
		"warmcol":	[

		],
	}

	def __init__(self, definitions):
		if isinstance(definitions, str):
			definitions = ColorMixer._predef[definitions]
		assert(isinstance(definitions, list))
		assert(len(definitions) >= 2)

		defs = [ ]
		number = 0
		for (index, r, g, b) in definitions:
			if index is None:
				index = number / (len(definitions) - 1)
			if (number == 0):
				index = 0
			elif (number == (len(definitions) - 1)):
				index = 1
			assert(0 <= index <= 1)
			defs.append((index, r, g, b))
			number += 1

		defs = sorted(defs)
		self._cutpoints = [ defn[0] for defn in defs ]
		self._colors = [ defn[1 : 4] for defn in defs ]

	def __getitem__(self, key):
		assert(isinstance(key, int) or isinstance(key, float))
		if key < 0:
			return self._colors[0]
		elif key > 1:
			return self._colors[-1]

		index = bisect.bisect(self._cutpoints, key) - 1
		assert(0 <= index < len(self._cutpoints))
		if index == len(self._cutpoints) - 1:
			return self._colors[-1]

		assert(self._cutpoints[index] <= key < self._cutpoints[index + 1])
		low = self._colors[index]
		high = self._colors[index + 1]
		inbetween = (key - self._cutpoints[index]) / (self._cutpoints[index + 1] - self._cutpoints[index])

		mixcolor = [ round((low[i] * (1 - inbetween)) + (high[i] * inbetween)) for i in range(3) ]
		return tuple(mixcolor)

	def getallcolorschemes():
		return iter(ColorMixer._predef.keys())

if __name__ == "__main__":
	from PnmPicture import PnmPicture

	def scmexport(scheme, width):
		pic = PnmPicture().new(width, 10)

		c = ColorMixer(scheme)
		for x in range(width):
			frac = x / (width - 1)
			for y in range(pic.getheight()):
				pic.setpixel(x, y, c[frac])
		pic.writefile("export_" + scheme + ".pnm")

	def scmimport(scheme):
		sample_y = 0
		maxerror = 25

		def mix(col1, col2, pos):
			ratio = (pos - col1[0]) / (col2[0] - col1[0])
			mixcol = [ round((ratio * col2[1][i]) + ((1 - ratio) * col1[1][i]))  for i in range(3) ]
			return mixcol

		def coldiff(col1, col2):
			return sum([ abs(col1[i] - col2[i]) for i in range(3) ])

		pic = PnmPicture().readfile("input_" + scheme + ".pnm")
		# Sample all colors
		colors = [ ]
		for x in range(pic.getwidth()):
			prcntile = x / (pic.getwidth() - 1)
			colors.append((prcntile, (pic.getpixel(x, sample_y))))

		# Elimination phase
		reducedcolors = [ colors[0] ]
		index = 1
		while index < (len(colors) - 1):
#			print("NEW LOOP ", index)
			left = reducedcolors[-1]
			tryright = 1

			right = None
			added = False
			for tryright in range(1, len(colors) - index):
				lastright = right
				right = colors[index + tryright]
#				print("Try idx %d try %d" % (index, tryright))
				maxdiff = 0
				for i in range(tryright):
					middle = colors[index + i]
#					print(middle)
					mixcol = mix(left, right, middle[0])
					diff = coldiff(mixcol, middle[1])
					maxdiff = max(maxdiff, diff)
#					print("   ",left, middle, right, diff)
#				print("-> tr=",tryright, "diff", maxdiff)
				if maxdiff >= maxerror:
#					print(maxdiff)
					reducedcolors.append(lastright)
					index += tryright
					added = True
					break
			if not added:
				# We're at the end
				reducedcolors.append(colors[-1])
				break
		print("%d items" % (len(reducedcolors)))
		print("		\"%s\": [" % (scheme))
		for (perc, (r, g, b)) in reducedcolors:
			print("			(%.3f, %3d, %3d, %3d)," % (perc, r, g, b))
		print("		],")

	def scmexportall():
		for name in ColorMixer.getallcolorschemes():
			scmexport(name, 800)


#	scmimport("map3")
#	scmexport("heatmap", 347)
#	scmexport("heatmap2", 499)
	scmexportall()

