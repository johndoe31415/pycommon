#!/usr/bin/python3
#
#	ColorPalette - Simple color palette abstraction.
#	Copyright (C) 2015-2015 Johannes Bauer
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
#	File UUID ecb7fd95-4db3-4831-9bde-e40cae0e9a50
	
import math
import collections

_Palette = collections.namedtuple("Palette", [ "colors", "order", "columns" ])

class ColorPalette(object):
	_PALETTES = {
		"flatui": _Palette(colors = {
			"turquoise":		0x1abc9c,
			"green-sea":		0x16a085,
			"emerland":			0x2ecc71,
			"nephritis":		0x27ae60,
			"peter-river":		0x3498db,
			"belize-hole":		0x2980b9,
			"amethyst":			0x9b59b6,
			"wisteria":			0x8e44ad,
			"wet-asphalt":		0x34495e,
			"midnight-blue":	0x2c3e50,
			"sun-flower":		0xf1c40f,
			"orange":			0xf39c12,
			"carrot":			0xe67e22,
			"pumpkin":			0xd35400,
			"alizarin":			0xe74c3c,
			"pomegranate":		0xc0392b,
			"clouds":			0xecf0f1,
			"silver":			0xbdc3c7,
			"concrete":			0x95a5a6,
			"asbestos":			0x7f8c8d,
		}, order = [ 
			"turquoise", "emerland", "peter-river", "amethyst", "wet-asphalt", 
			"green-sea", "nephritis", "belize-hole", "wisteria", "midnight-blue",
			"sun-flower", "carrot", "alizarin", "clouds", "concrete",
			"orange", "pumpkin", "pomegranate", "silver", "asbestos",
		], columns = 5),

		"other": _Palette(colors = {
			"black0": 0x20201f,
			"black1": 0x222222,
			"black2": 0x2e2e2e,
			"black3": 0x41403f,
			"black4": 0x5e5d5c,
			"darkblue0": 0x223444,
			"darkblue1": 0x2b3e50,
			"darkblue2": 0x33495e,
			"darkblue3": 0x3f5970,
			"darkblue4": 0x56636d,
			"green0": 0xa9050,
			"green1": 0x19ab60,
			"green2": 0x1dc871,
			"green3": 0x36c677,
			"green4": 0x63c690,
			"purple0": 0x744186,
			"purple1": 0x8f4dad,
			"purple2": 0x9c60b6,
			"purple3": 0x9b69b5,
			"purple4": 0xa37fb5,
			"blue0": 0x3e7699,
			"blue1": 0x4c90bb,
			"blue2": 0x509ac7,
			"blue3": 0x549dcc,
			"blue4": 0x59ade2,
			"yellow0": 0xc5a114,
			"yellow1": 0xd9b017,
			"yellow2": 0xe3b818,
			"yellow3": 0xf2c208,
			"yellow4": 0xefc43a,
			"red0": 0xb23e2a,
			"red1": 0xd34b35,
			"red2": 0xe9533b,
			"red3": 0xe85749,
			"red4": 0xe05f5f,
			"orange0": 0xbf691b,
			"orange1": 0xd27420,
			"orange2": 0xe87f20,
			"orange3": 0xe87f20,
			"orange4": 0xe28c4b,
		}, order = [
			"blue0", "blue1", "blue2", "blue3", "blue4",
			"yellow0", "yellow1", "yellow2", "yellow3", "yellow4",
			"orange0", "orange1", "orange2", "orange3", "orange4",
			"red0", "red1", "red2", "red3", "red4",
			"darkblue0", "darkblue1", "darkblue2", "darkblue3", "darkblue4",
			"green0", "green1", "green2", "green3", "green4",
			"purple0", "purple1", "purple2", "purple3", "purple4",
			"black0", "black1", "black2", "black3", "black4",
		], columns = 5),
	}

	def __init__(self, palettename):
		self._name = palettename
		self._palette = ColorPalette._PALETTES[palettename]

	@staticmethod
	def _coldistance(col1, col2):
		return math.sqrt(sum(((x - y) ** 2) for (x, y) in zip(col1, col2)))

	def orderby(self, colormixer):
		granularity = 100
		reference = { i / (granularity - 1): colormixer[i / (granularity - 1)] for i in range(granularity) }
		result = [ ]
		for color in self:
			mindistance = None
			refscale = None
			for (scalevalue, refcolor) in reference.items():
				distance = self._coldistance(refcolor, color)
				if (mindistance is None) or (distance < mindistance):
					mindistance = distance					
					refscale = scalevalue
			result.append((refscale, color))
		result.sort()
		yield from (x[1] for x in result)

	@property
	def columns(self):
		return self._palette.columns

	def __len__(self):
		return len(self._palette.colors)

	def __iter__(self):
		for name in self._palette.order:
			color = self._palette.colors[name]
			yield ((color >> 16) & 0xff, (color >> 8) & 0xff, (color >> 0) & 0xff)

	def __getitem__(self, colorname):
		return self._palette.colors[colorname]

if __name__ == "__main__":
	from PnmPicture import PnmPicture
	palette_name = "flatui"

	pal = ColorPalette(palette_name)

	width = math.ceil(pal.columns)
	height = math.ceil(len(pal) / width)
	pic = PnmPicture().new(width, height)
	for (index, color) in enumerate(pal):
		x = index % pic.width
		y = index // pic.width
		pic.setpixel(x, y, color)
	pic = pic.upscale(16, 16)
	pic.writefile("palette_%s_base.pnm" % (palette_name))

	from ColorMixer import ColorMixer
	mixer = ColorMixer("rainbow")
	sortedcols = list(pal.orderby(mixer))
	coldef = [ (i / (len(sortedcols) - 1), color[0], color[1], color[2])  for (i, color) in enumerate(sortedcols) ]
	othermixer = ColorMixer(coldef)
	
	pic = PnmPicture().new(512, 2)
	for i in range(pic.width):
		pic.setpixel(i, 0, othermixer[i / ((pic.width) - 1)])
		pic.setpixel(i, 1, mixer[i / ((pic.width) - 1)])
	pic = pic.upscale(ymultiplicity = 20)
	pic.writefile("palette_%s_mixer.pnm" % (palette_name))


	from RGBColor import RGBColor
	pic = PnmPicture().readfile("aaaaaaaa.pnm")
	(w, h) = (5, 8)
	(xstep, ystep) = (pic.width / w, pic.height / h)
	print(pic)
	cols = {
		0:	"blue",
		1:	"yellow",
		2:	"orange",
		3:	"red",
		4:	"darkblue",
		5:	"green",
		6:	"purple",
		7:	"black",
	}
	colors = { }
	for y in range(h):
		for x in range(w):
			xoffset = round((xstep / 2) + x * xstep)
			yoffset = round((ystep / 2) + y * ystep)
			color = pic.getpixel(xoffset, yoffset)

			basecolor = cols[y]
			if basecolor not in colors:
				colors[basecolor] = [ ]
			colors[basecolor].append(RGBColor.frombyte(*color))
	for (basecolor, colors) in colors.items():
		colors.sort(key = lambda col: -col.lightness)
		
		for (index, color) in enumerate(colors):
			print("\"%s%d\": 0x%x," % (basecolor, index, int(color)))
