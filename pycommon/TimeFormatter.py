#!/usr/bin/python3
#
#	TimeFormatter - Format a period of seconds
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
#	File UUID 1e0e682e-5dae-4b03-a806-14ecd012ec64

class TimeFormatter():
	def fmt(t):
		if t < 0:
			return "-" + TimeFormatter.fmt(-t)

		if t < 1:
			return "%d ms" % (round(1000 * t))
		elif t < 10:
			return "%.1f sec" % (t)
		else:
			tint = round(t)
			if tint < 60:
				return "%d sec" % (tint)
			elif tint < 3600:
				return "%d:%02d m:s" % (tint // 60, tint % 60)
			elif tint < 86400:
				return "%d:%02d:%02d h:m:s" % (tint // 3600, tint % 3600 // 60, tint % 3600 % 60)
			else:
				return "%d-%d:%02d:%02d d-h:m:s" % (tint // 86400, tint % 86400 // 3600, tint % 86400 % 3600 // 60, tint % 86400 % 3600 % 60)

	def __call__(self, t):
		return TimeFormatter.fmt(t)

if __name__ == "__main__":
	print(TimeFormatter.fmt(12345))
	print(TimeFormatter.fmt(-12345))

