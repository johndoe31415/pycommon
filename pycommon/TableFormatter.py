#!/usr/bin/python3
#
#	TableFormatter - Print tables nicely on ASCII terminals
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
#	File UUID c769b4e3-0303-4558-96b1-5fa444b8199d

import sys
import io

class TableCellFormatter():
	def __init__(self, **kwargs):
		self._minlen = kwargs.get("minlen", None)
		self._maxlen = kwargs.get("maxlen", None)
		self._align = kwargs.get("align", "L")
		self._prefix = kwargs.get("prefix", None)
		self._postfix = kwargs.get("postfix", None)
		assert((self._minlen is None) or (self._minlen >= 4))
		assert((self._minlen is None) or (self._maxlen is None) or (self._minlen <= self._maxlen))
		assert(self._align in [ "R", "L" ])

	def setprefix(self, prefix):
		self._prefix = prefix
	
	def setpostfix(self, postfix):
		self._postfix = postfix

	# returns min(self._maxlen, inheritfmtr._maxlen) and handles None appropriately
	def _getmaxlen(self, inheritfmtr):
		lengths = [ x for x in [ self._maxlen ] if (x is not None) ]
		if (inheritfmtr is not None) and (inheritfmtr._maxlen is not None):
			lengths.append(inheritfmtr._maxlen)
		if len(lengths) == 0:
			return None
		else:
			return max(lengths)

	# returns max(self._minlen, inheritfmtr._minlen, tolen) and handles None appropriately
	def _getpadlen(self, tolen, inheritfmtr):
		lengths = [ x for x in [ self._minlen, tolen ] if (x is not None) ]
		if (inheritfmtr is not None) and (inheritfmtr._minlen is not None):
			lengths.append(inheritfmtr._minlen)
		if len(lengths) == 0:
			return None
		else:
			return max(lengths)

	def _getprefix(self):
		if self._prefix is None:
			return ""
		else:
			return self._prefix
	
	def _getpostfix(self):
		if self._postfix is None:
			return ""
		else:
			return self._postfix

	def fmt(self, instr, tolen = None, inheritfmtr = None):
		orig = instr
		# Truncation if too long
		maxlen = self._getmaxlen(inheritfmtr)
		if (maxlen is not None) and (len(instr) > maxlen):
			instr = instr[:maxlen - 3] + "..."

		# Padding if too short
		padlen = self._getpadlen(tolen, inheritfmtr)
		if (padlen is not None) and (len(instr) < padlen):
			if self._align == "L":
				instr = self._getprefix() + instr + self._getpostfix() + (" " * (padlen - len(instr)))
			else:
				instr = (" " * (padlen - len(instr))) + self._getprefix() + instr + self._getpostfix()
		else:
			instr = self._getprefix() + instr + self._getpostfix()

		return instr


class SimpleTableFormat():
	def getcolsep(self):
		return "   "
	
	def getleftcolborder(self):
		return ""
	
	def getrightcolborder(self):
		return ""

	def getleftspacerborder(self, spacertype):
		return ""
	
	def getrightspacerborder(self, spacertype):
		return ""
	
	def getspacersep(self, spacertype):
		return ""
	
	def getspacerhorizontal(self, spacertype):
		return ""


class ASCIITableFormat(SimpleTableFormat):
	def getcolsep(self):
		return " | "
	
	def getleftcolborder(self):
		return "| "
	
	def getrightcolborder(self):
		return " |"
	
	def getleftspacerborder(self, spacertype):
		return "+-"
	
	def getrightspacerborder(self, spacertype):
		return "-+"
	
	def getspacersep(self, spacertype):
		return "-+-"
	
	def getspacerhorizontal(self, spacertype):
		return "-"


class FancyTableFormat(SimpleTableFormat):
	_charsets = {
		"normal": {
			"V":	"│",
			"H":	"─",
			"TL":	"┌",
			"ML":	"├",
			"BL":	"└",
			"TR":	"┐",
			"MR":	"┤",
			"BR":	"┘",
			"TM":	"┬",
			"MM":	"┼",
			"BM":	"┴",
		},
		"fat": {
			"V":	"┃",
			"H":	"━",
			"TL":	"┏",
			"ML":	"┣",
			"BL":	"┗",
			"TR":	"┓",
			"MR":	"┫",
			"BR":	"┛",
			"TM":	"┳",
			"MM":	"╋",
			"BM":	"┻",
		},
		"double": {
			"V":	"║",
			"H":	"═",
			"TL":	"╔",
			"ML":	"╠",
			"BL":	"╚",
			"TR":	"╗",
			"MR":	"╣",
			"BR":	"╝",
			"TM":	"╦",
			"MM":	"╬",
			"BM":	"╩",
		},
		"sngdouble": {
			"V":	"│",
			"H":	"═",
			"TL":	"╒",
			"ML":	"╞",
			"BL":	"╘",
			"TR":	"╕",
			"MR":	"╡",
			"BR":	"╛",
			"TM":	"╤",
			"MM":	"╪",
			"BM":	"╧",
		},
		"horiz-only": {
			"V":	" ",
			"H":	"─",
			"TL":	" ",
			"ML":	" ",
			"BL":	" ",
			"TR":	" ",
			"MR":	" ",
			"BR":	" ",
			"TM":	"┄",
			"MM":	"┄",
			"BM":	"┄",
		},
	}

	def __init__(self, tabletype = None):
		if tabletype is None:
			tabletype = "normal"
		self._charset = FancyTableFormat._charsets[tabletype]

	def __getitem__(self, key):
		return self._charset[key]

	def getcolsep(self):
		return " " + self["V"] + " "
	
	def getleftcolborder(self):
		return self["V"] + " "
	
	def getrightcolborder(self):
		return " " + self["V"]
	
	def getleftspacerborder(self, spacertype):
		return self[spacertype + "L"] + self["H"]
	
	def getrightspacerborder(self, spacertype):
		return self["H"] + self[spacertype + "R"]
	
	def getspacersep(self, spacertype):
		return self["H"] + self[spacertype + "M"] + self["H"]
	
	def getspacerhorizontal(self, spacertype):
		return self["H"]


class TableFormatter():
	def __init__(self, tableformat = None):
		self._rows = [ ]
		self._rowformatters = { }
		self._cellformatters = { }
		if tableformat is None:
			self._tableformat = SimpleTableFormat()
		else:
			self._tableformat = tableformat
		self._colwidths = None

	def add(self, *row):
		self._rows.append(row)
		self._colwidths = None
		return self

	def addspacer(self):
		self._rows.append(None)
		self._colwidths = None
		return self

	def addcellformatter(self, colid, rowid, fmtr):
		assert(colid >= 0)
		if rowid < 0:
			rowid += len(self._rows)
		self._cellformatters[(colid, rowid)] = fmtr

	def getcolcnt(self):
		return max([ len(r) for r in self._rows if (r is not None)])

	def colfmt(self, colid, colfmter):
		assert(isinstance(colid, int))
		self._rowformatters[colid] = colfmter
		self._colwidths = None
		
	def _calccolwidths(self):
		if self._colwidths is not None:
			return

		self._colwidths = { }
		for rowid in range(len(self._rows)):
			row = self._rows[rowid]
			if row is not None:
				for colid in range(len(row)):
					cellid = (colid, rowid)
					coltext = row[colid]
					if self._rowformatters.get(colid) is not None:
						coltext = self._rowformatters[colid].fmt(coltext)
					self._colwidths[colid] = max(self._colwidths.get(colid, 0), len(coltext))

	def print(self, f = None):
		if f is None:
			f = sys.stdout
		self._calccolwidths()

		stdfmt = TableCellFormatter()
		colcnt = self.getcolcnt()
		for rowid in range(len(self._rows)):
			row = self._rows[rowid]
			if row is not None:
				rowtext = self._tableformat.getleftcolborder()
				for colid in range(colcnt):
					cellid = (colid, rowid)
					if colid < len(row):
						coltext = row[colid]
					else:
						coltext = ""

					if self._cellformatters.get(cellid) is not None:
						coltext = self._cellformatters[cellid].fmt(coltext, self._colwidths[colid], self._rowformatters.get(colid))
					elif self._rowformatters.get(colid) is not None:
						coltext = self._rowformatters[colid].fmt(coltext, self._colwidths[colid])
					else:
						coltext = stdfmt.fmt(coltext, self._colwidths[colid])
					rowtext += coltext
					if colid < colcnt - 1:
						rowtext += self._tableformat.getcolsep()
				rowtext += self._tableformat.getrightcolborder()
			else:
				# Spacer row
				if rowid == 0:
					spacertype = "T"
				elif rowid == len(self._rows) - 1:
					spacertype = "B"
				else:
					spacertype = "M"
				rowtext = self._tableformat.getleftspacerborder(spacertype)
				for colid in range(colcnt):
					rowtext += self._tableformat.getspacerhorizontal(spacertype) * self._colwidths[colid]
					if colid < colcnt - 1:
						rowtext += self._tableformat.getspacersep(spacertype)
				rowtext += self._tableformat.getrightspacerborder(spacertype)
			print(rowtext, file = f)

	def __str__(self):
		s = io.StringIO()
		self.print(s)
		return s.getvalue()
		

if __name__ == "__main__":
#	table = TableFormatter()
#	table = TableFormatter(ASCIITableFormat())
#	table = TableFormatter(FancyTableFormat())
	table = TableFormatter(FancyTableFormat("fat"))
#	table = TableFormatter(FancyTableFormat("double"))
#	table = TableFormatter(FancyTableFormat("sngdouble"))
#	table = TableFormatter(FancyTableFormat("horiz-only"))
	table.addspacer()
	table.add("Foobar", "Barfoo")
	table.addspacer()
	table.add("Hier ist ein foobar", "%5.3f" % (1.23456))
	table.addcellformatter(0, -1, TableCellFormatter(prefix = "moo", postfix = "koo"))
	table.add("Und dort auch", "%5.3f" % (873.56))
	table.add("Das hier ist eine viel zu lange sehr sehr lange zeile, die nicht ganz reinpasst", "%5.3f" % (873.56))
	table.addspacer()
	table.addcellformatter(0, 5, TableCellFormatter(prefix = "$$$", postfix = "###"))

	table.colfmt(0, TableCellFormatter(maxlen = 30, align = "L"))
	table.colfmt(1, TableCellFormatter(align = "R"))
	table.print()


	testwithansi = True
	if testwithansi:
		from Ansi256 import Ansi256

		table = TableFormatter(FancyTableFormat("fat"))
		table.addspacer()
		table.add("Foobar", "Barfoo")
		table.addspacer()
		table.add("Hier ist ein foobar", "%5.3f" % (1.23456))
		table.addcellformatter(0, -1, TableCellFormatter(prefix = "<fg:green>", postfix = "<reset>"))
		table.addcellformatter(1, -1, TableCellFormatter(prefix = "<fg:yellow>", postfix = "<reset>"))
		table.add("Und dort auch", "%5.3f" % (873.56))
		table.addcellformatter(1, -1, TableCellFormatter(prefix = "<fg:red>", postfix = "<reset>"))
		table.add("Das hier ist eine viel zu lange sehr sehr lange zeile, die nicht ganz reinpasst", "%5.3f" % (873.56))
		table.addcellformatter(0, -1, TableCellFormatter(prefix = "<fg:green>", postfix = "<reset>"))
		table.addspacer()

		table.colfmt(0, TableCellFormatter(maxlen = 30, align = "L"))
		table.colfmt(1, TableCellFormatter(align = "R"))
		Ansi256().print(str(table))

