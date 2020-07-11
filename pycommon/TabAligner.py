#!/usr/bin/python3
#
#	TabAligner - Print values so they are aligned using tabs
#	Copyright (C) 2020-2020 Johannes Bauer
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
#	File UUID cb909aad-8642-42a8-a171-8b7be71c8ce9

class TabAligner():
	def __init__(self, columns, tabsize = 4):
		assert(all((column % tabsize) == 1 for column in columns))
		self._columns = [ column - 1 for column in columns ]
		self._tabsize = tabsize

	def __call__(self, *values):
		assert(len(values) == len(self._columns))
		current_pos = 0
		line = [ ]
		for (value_no, (want_pos, value)) in enumerate(zip(self._columns, values)):
			if current_pos < want_pos:
				tabs_required = ((want_pos - current_pos) + self._tabsize - 1) // self._tabsize
				line.append(tabs_required * "\t")
				current_pos = want_pos
			else:
				if value_no != 0:
					# Need at least one tab
					line.append("\t")
					if (current_pos % self._tabsize) == 0:
						current_pos += self._tabsize
					else:
						current_pos = (current_pos + self._tabsize - 1) // self._tabsize * self._tabsize

			line.append(value)
			current_pos += len(value)
		return "".join(line)


if __name__ == "__main__":
	tal = TabAligner([ 1, 13, 41 ])
	print(tal("foo", "bar", "moo"))
	print(tal("foox", "bar", "moo"))
	print(tal("fooxx", "bar", "moo"))
	print(tal("fooxxx", "bar", "moo"))
	print(tal("fooxxxx", "bar", "moo"))
	print(tal("fooxxxxx", "bar", "moo"))
	print(tal("fooxxxxxx", "bar", "moo"))
	print(tal("fooxxxxxxx", "bar", "moo"))
	print(tal("fooxxxxxxxx", "bar", "moo"))
	print(tal("fooxxxxxxxxx", "bar", "moo"))
	print(tal("fooxxxxxxxxxx", "bar", "moo"))
	print(tal("fooxxxxxxxxxxx", "bar", "moo"))
