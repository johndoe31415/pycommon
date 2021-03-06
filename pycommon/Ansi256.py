#!/usr/bin/python3
#
#	Ansi256 - Simple 256 color terminal markup abstraction.
#	Copyright (C) 2011-2019 Johannes Bauer
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
#	File UUID 5ea94190-6a04-4ed8-afd6-a516922e9671

import re
import colorsys

class Ansi256():
	_commoncolors = {
		"red":			"#ff0000",
		"green":		"#0ca300",
		"brightgreen":	"#87ff00",
		"blue":			"#222b88",
		"white":		"#ffffff",
		"black":		"#000000",
		"yellow":		"#ffff00",
		"brown":		"#875f00",
		"cyan":			"#55ffff",
		"gray":			"#888888",
	}

	_colors = {
		1:		(0xaa, 0x00, 0x00),
		2:		(0x00, 0xaa, 0x00),
		3:		(0xaa, 0x55, 0x00),
		4:		(0x00, 0x00, 0xaa),
		5:		(0xaa, 0x00, 0xaa),
		6:		(0x00, 0xaa, 0xaa),
		7:		(0xaa, 0xaa, 0xaa),
		8:		(0x55, 0x55, 0x55),
		9:		(0xff, 0x55, 0x55),
		10:		(0x55, 0xff, 0x55),
		11:		(0xff, 0xff, 0x55),
		12:		(0x55, 0x55, 0xff),
		13:		(0xff, 0x55, 0xff),
		14:		(0x55, 0xff, 0xff),
		15:		(0xff, 0xff, 0xff),
		16:		(0x00, 0x00, 0x00),
		17:		(0x00, 0x00, 0x5f),
		18:		(0x00, 0x00, 0x87),
		19:		(0x00, 0x00, 0xaf),
		20:		(0x00, 0x00, 0xd7),
		21:		(0x00, 0x00, 0xff),
		22:		(0x00, 0x5f, 0x00),
		23:		(0x00, 0x5f, 0x5f),
		24:		(0x00, 0x5f, 0x87),
		25:		(0x00, 0x5f, 0xaf),
		26:		(0x00, 0x5f, 0xd7),
		27:		(0x00, 0x5f, 0xff),
		28:		(0x00, 0x87, 0x00),
		29:		(0x00, 0x87, 0x5f),
		30:		(0x00, 0x87, 0x87),
		31:		(0x00, 0x87, 0xaf),
		32:		(0x00, 0x87, 0xd7),
		33:		(0x00, 0x87, 0xff),
		34:		(0x00, 0xaf, 0x00),
		35:		(0x00, 0xaf, 0x5f),
		36:		(0x00, 0xaf, 0x87),
		37:		(0x00, 0xaf, 0xaf),
		38:		(0x00, 0xaf, 0xd7),
		39:		(0x00, 0xaf, 0xff),
		40:		(0x00, 0xd7, 0x00),
		41:		(0x00, 0xd7, 0x5f),
		42:		(0x00, 0xd7, 0x87),
		43:		(0x00, 0xd7, 0xaf),
		44:		(0x00, 0xd7, 0xd7),
		45:		(0x00, 0xd7, 0xff),
		46:		(0x00, 0xff, 0x00),
		47:		(0x00, 0xff, 0x5f),
		48:		(0x00, 0xff, 0x87),
		49:		(0x00, 0xff, 0xaf),
		50:		(0x00, 0xff, 0xd7),
		51:		(0x00, 0xff, 0xff),
		52:		(0x5f, 0x00, 0x00),
		53:		(0x5f, 0x00, 0x5f),
		54:		(0x5f, 0x00, 0x87),
		55:		(0x5f, 0x00, 0xaf),
		56:		(0x5f, 0x00, 0xd7),
		57:		(0x5f, 0x00, 0xff),
		58:		(0x5f, 0x5f, 0x00),
		59:		(0x5f, 0x5f, 0x5f),
		60:		(0x5f, 0x5f, 0x87),
		61:		(0x5f, 0x5f, 0xaf),
		62:		(0x5f, 0x5f, 0xd7),
		63:		(0x5f, 0x5f, 0xff),
		64:		(0x5f, 0x87, 0x00),
		65:		(0x5f, 0x87, 0x5f),
		66:		(0x5f, 0x87, 0x87),
		67:		(0x5f, 0x87, 0xaf),
		68:		(0x5f, 0x87, 0xd7),
		69:		(0x5f, 0x87, 0xff),
		70:		(0x5f, 0xaf, 0x00),
		71:		(0x5f, 0xaf, 0x5f),
		72:		(0x5f, 0xaf, 0x87),
		73:		(0x5f, 0xaf, 0xaf),
		74:		(0x5f, 0xaf, 0xd7),
		75:		(0x5f, 0xaf, 0xff),
		76:		(0x5f, 0xd7, 0x00),
		77:		(0x5f, 0xd7, 0x5f),
		78:		(0x5f, 0xd7, 0x87),
		79:		(0x5f, 0xd7, 0xaf),
		80:		(0x5f, 0xd7, 0xd7),
		81:		(0x5f, 0xd7, 0xff),
		82:		(0x5f, 0xff, 0x00),
		83:		(0x5f, 0xff, 0x5f),
		84:		(0x5f, 0xff, 0x87),
		85:		(0x5f, 0xff, 0xaf),
		86:		(0x5f, 0xff, 0xd7),
		87:		(0x5f, 0xff, 0xff),
		88:		(0x87, 0x00, 0x00),
		89:		(0x87, 0x00, 0x5f),
		90:		(0x87, 0x00, 0x87),
		91:		(0x87, 0x00, 0xaf),
		92:		(0x87, 0x00, 0xd7),
		93:		(0x87, 0x00, 0xff),
		94:		(0x87, 0x5f, 0x00),
		95:		(0x87, 0x5f, 0x5f),
		96:		(0x87, 0x5f, 0x87),
		97:		(0x87, 0x5f, 0xaf),
		98:		(0x87, 0x5f, 0xd7),
		99:		(0x87, 0x5f, 0xff),
		100:	(0x87, 0x87, 0x00),
		101:	(0x87, 0x87, 0x5f),
		102:	(0x87, 0x87, 0x87),
		103:	(0x87, 0x87, 0xaf),
		104:	(0x87, 0x87, 0xd7),
		105:	(0x87, 0x87, 0xff),
		106:	(0x87, 0xaf, 0x00),
		107:	(0x87, 0xaf, 0x5f),
		108:	(0x87, 0xaf, 0x87),
		109:	(0x87, 0xaf, 0xaf),
		110:	(0x87, 0xaf, 0xd7),
		111:	(0x87, 0xaf, 0xff),
		112:	(0x87, 0xd7, 0x00),
		113:	(0x87, 0xd7, 0x5f),
		114:	(0x87, 0xd7, 0x87),
		115:	(0x87, 0xd7, 0xaf),
		116:	(0x87, 0xd7, 0xd7),
		117:	(0x87, 0xd7, 0xff),
		118:	(0x87, 0xff, 0x00),
		119:	(0x87, 0xff, 0x5f),
		120:	(0x87, 0xff, 0x87),
		121:	(0x87, 0xff, 0xaf),
		122:	(0x87, 0xff, 0xd7),
		123:	(0x87, 0xff, 0xff),
		124:	(0xaf, 0x00, 0x00),
		125:	(0xaf, 0x00, 0x5f),
		126:	(0xaf, 0x00, 0x87),
		127:	(0xaf, 0x00, 0xaf),
		128:	(0xaf, 0x00, 0xd7),
		129:	(0xaf, 0x00, 0xff),
		130:	(0xaf, 0x5f, 0x00),
		131:	(0xaf, 0x5f, 0x5f),
		132:	(0xaf, 0x5f, 0x87),
		133:	(0xaf, 0x5f, 0xaf),
		134:	(0xaf, 0x5f, 0xd7),
		135:	(0xaf, 0x5f, 0xff),
		136:	(0xaf, 0x87, 0x00),
		137:	(0xaf, 0x87, 0x5f),
		138:	(0xaf, 0x87, 0x87),
		139:	(0xaf, 0x87, 0xaf),
		140:	(0xaf, 0x87, 0xd7),
		141:	(0xaf, 0x87, 0xff),
		142:	(0xaf, 0xaf, 0x00),
		143:	(0xaf, 0xaf, 0x5f),
		144:	(0xaf, 0xaf, 0x87),
		145:	(0xaf, 0xaf, 0xaf),
		146:	(0xaf, 0xaf, 0xd7),
		147:	(0xaf, 0xaf, 0xff),
		148:	(0xaf, 0xd7, 0x00),
		149:	(0xaf, 0xd7, 0x5f),
		150:	(0xaf, 0xd7, 0x87),
		151:	(0xaf, 0xd7, 0xaf),
		152:	(0xaf, 0xd7, 0xd7),
		153:	(0xaf, 0xd7, 0xff),
		154:	(0xaf, 0xff, 0x00),
		155:	(0xaf, 0xff, 0x5f),
		156:	(0xaf, 0xff, 0x87),
		157:	(0xaf, 0xff, 0xaf),
		158:	(0xaf, 0xff, 0xd7),
		159:	(0xaf, 0xff, 0xff),
		160:	(0xd7, 0x00, 0x00),
		161:	(0xd7, 0x00, 0x5f),
		162:	(0xd7, 0x00, 0x87),
		163:	(0xd7, 0x00, 0xaf),
		164:	(0xd7, 0x00, 0xd7),
		165:	(0xd7, 0x00, 0xff),
		166:	(0xd7, 0x5f, 0x00),
		167:	(0xd7, 0x5f, 0x5f),
		168:	(0xd7, 0x5f, 0x87),
		169:	(0xd7, 0x5f, 0xaf),
		170:	(0xd7, 0x5f, 0xd7),
		171:	(0xd7, 0x5f, 0xff),
		172:	(0xd7, 0x87, 0x00),
		173:	(0xd7, 0x87, 0x5f),
		174:	(0xd7, 0x87, 0x87),
		175:	(0xd7, 0x87, 0xaf),
		176:	(0xd7, 0x87, 0xd7),
		177:	(0xd7, 0x87, 0xff),
		178:	(0xd7, 0xaf, 0x00),
		179:	(0xd7, 0xaf, 0x5f),
		180:	(0xd7, 0xaf, 0x87),
		181:	(0xd7, 0xaf, 0xaf),
		182:	(0xd7, 0xaf, 0xd7),
		183:	(0xd7, 0xaf, 0xff),
		184:	(0xd7, 0xd7, 0x00),
		185:	(0xd7, 0xd7, 0x5f),
		186:	(0xd7, 0xd7, 0x87),
		187:	(0xd7, 0xd7, 0xaf),
		188:	(0xd7, 0xd7, 0xd7),
		189:	(0xd7, 0xd7, 0xff),
		190:	(0xd7, 0xff, 0x00),
		191:	(0xd7, 0xff, 0x5f),
		192:	(0xd7, 0xff, 0x87),
		193:	(0xd7, 0xff, 0xaf),
		194:	(0xd7, 0xff, 0xd7),
		195:	(0xd7, 0xff, 0xff),
		196:	(0xff, 0x00, 0x00),
		197:	(0xff, 0x00, 0x5f),
		198:	(0xff, 0x00, 0x87),
		199:	(0xff, 0x00, 0xaf),
		200:	(0xff, 0x00, 0xd7),
		201:	(0xff, 0x00, 0xff),
		202:	(0xff, 0x5f, 0x00),
		203:	(0xff, 0x5f, 0x5f),
		204:	(0xff, 0x5f, 0x87),
		205:	(0xff, 0x5f, 0xaf),
		206:	(0xff, 0x5f, 0xd7),
		207:	(0xff, 0x5f, 0xff),
		208:	(0xff, 0x87, 0x00),
		209:	(0xff, 0x87, 0x5f),
		210:	(0xff, 0x87, 0x87),
		211:	(0xff, 0x87, 0xaf),
		212:	(0xff, 0x87, 0xd7),
		213:	(0xff, 0x87, 0xff),
		214:	(0xff, 0xaf, 0x00),
		215:	(0xff, 0xaf, 0x5f),
		216:	(0xff, 0xaf, 0x87),
		217:	(0xff, 0xaf, 0xaf),
		218:	(0xff, 0xaf, 0xd7),
		219:	(0xff, 0xaf, 0xff),
		220:	(0xff, 0xd7, 0x00),
		221:	(0xff, 0xd7, 0x5f),
		222:	(0xff, 0xd7, 0x87),
		223:	(0xff, 0xd7, 0xaf),
		224:	(0xff, 0xd7, 0xd7),
		225:	(0xff, 0xd7, 0xff),
		226:	(0xff, 0xff, 0x00),
		227:	(0xff, 0xff, 0x5f),
		228:	(0xff, 0xff, 0x87),
		229:	(0xff, 0xff, 0xaf),
		230:	(0xff, 0xff, 0xd7),
		231:	(0xff, 0xff, 0xff),
		232:	(0x08, 0x08, 0x08),
		233:	(0x12, 0x12, 0x12),
		234:	(0x1c, 0x1c, 0x1c),
		235:	(0x26, 0x26, 0x26),
		236:	(0x30, 0x30, 0x30),
		237:	(0x3a, 0x3a, 0x3a),
		238:	(0x44, 0x44, 0x44),
		239:	(0x4e, 0x4e, 0x4e),
		240:	(0x58, 0x58, 0x58),
		241:	(0x62, 0x62, 0x62),
		242:	(0x6c, 0x6c, 0x6c),
		243:	(0x76, 0x76, 0x76),
		244:	(0x80, 0x80, 0x80),
		245:	(0x8a, 0x8a, 0x8a),
		246:	(0x94, 0x94, 0x94),
		247:	(0x9e, 0x9e, 0x9e),
		248:	(0xa8, 0xa8, 0xa8),
		249:	(0xb2, 0xb2, 0xb2),
		250:	(0xbc, 0xbc, 0xbc),
		251:	(0xc6, 0xc6, 0xc6),
		252:	(0xd0, 0xd0, 0xd0),
		253:	(0xda, 0xda, 0xda),
		254:	(0xe4, 0xe4, 0xe4),
		255:	(0xee, 0xee, 0xee),
	}

	_cmdregex = re.compile("<(bg|fg|reset)(#[0-9A-Fa-f]{6}|:[a-zA-Z]+)?>")

	def __init__(self):
		self._cache = { }

	def closesthtml(self, htmlcolor):
		assert(htmlcolor[0] == "#")
		sr = int(htmlcolor[1 : 3], 16)
		sg = int(htmlcolor[3 : 5], 16)
		sb = int(htmlcolor[5 : 7], 16)

		# We compare colors in HSV space and try to preserve hue
		(sh, ss, sv) = colorsys.rgb_to_hsv(sr, sg, sb)
		(best, bestdiff) = (None, None)
		for (colnum, (r, g, b)) in Ansi256._colors.items():
			(h, s, v) = colorsys.rgb_to_hsv(r, g, b)
			diff = (abs(h - sh) ** 5.0) + (abs(s - ss) ** 2.0) + (abs(v - sv) ** 2.0) + (abs(sr - r) ** 2.0) + (abs(sg - g) ** 2.0) + (abs(sb - b) ** 2.0)
			if (best is None) or (diff < bestdiff):
				best = colnum
				bestdiff = diff
		self._cache[htmlcolor] = best
		(r, g, b) = Ansi256._colors[best]
#		print("Resolved %s to %d (diff %d), i.e. #%02x%02x%02x (%+3d %+3d %+3d)" % (htmlcolor, best, bestdiff, r, g, b, r - sr, g - sg, b - sb))
		return best

	def closestcommon(self, colorname):
		return self.closesthtml(Ansi256._commoncolors[colorname])

	def closest(self, color):
		if color.startswith("#"):
			return self.closesthtml(color)
		elif color.startswith(":"):
			return self.closestcommon(color[1 : ])
		
	def _escape(text):
		return text.replace("\e", "\x1b")

	def format(self, string):
		result = Ansi256._cmdregex.search(string)

		while result:
			if result.group(1) == "reset":
				replacement = Ansi256._escape("\e[0m")
			else:
				color = self.closest(result.group(2))
				if result.group(1) == "bg":
					replacement = Ansi256._escape("\e[48;5;%dm" % (color))
				else:
					replacement = Ansi256._escape("\e[38;5;%dm" % (color))

			string = string[: result.start()] + replacement + string[ result.end() : ]
			result = Ansi256._cmdregex.search(string)
		return string

	def print(self, string):
		print(self.format(string))

	def getcolornames():
		return iter(Ansi256._commoncolors.keys())

if __name__ == "__main__":
	x = Ansi256()
#	print(x.closest("#5f1212"))
	x.print("Foo <fg:red><bg#00aa28>Bar<reset>Normal<fg:blue><bg:white>blue<reset> normal <bg:blue><fg:white>Invert<reset>")
	for color in sorted(list(Ansi256.getcolornames())):
		x.print("Foreground color: <fg:%s>%s<reset>" % (color, color))


