#!/usr/bin/python3
#
#	DateRange - Format date ranges or instants in language.
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
#	File UUID b5728c2b-bcf7-4518-878b-096693c55135

import datetime


class Timerange():
	def __init__(self, secs):
		if isinstance(secs, datetime.timedelta):
			self._secs = (secs.microseconds + (secs.seconds + secs.days * 86400) * 10 ** 6) / 10 ** 6
		else:
			self._secs = secs

	def secs(self):
		return self._secs

	def _singularplural(self, i, singular, plural, onenum = None):
		if i == 1:
			if (onenum is None):
				return "%d %s" % (i, singular)
			else:
				return "%s %s" % (onenum, singular)
		else:
			return "%d %s" % (i, plural)

	def __str__(self):
		s = ""
		abssecs = abs(self.secs())

		if abssecs > 86400:
			s += "%s und %s" % (Dayrange._singularplural(abssecs // 86400, "Tag", "Tage", "einen"), Dayrange._singularplural(abssecs % 86400 // 3600, "Stunde", "Stunden", "eine"))
		else:
			s += "%s und %s" % (Dayrange._singularplural(abssecs // 3600, "Stunde", "Stunden", "eine"), Dayrange._singularplural(abssecs % 3600 // 60, "Minute", "Minuten", "eine"))

		return s

if __name__ == "__main__":
	for i in range(-800, 800):
		print(("%4d: %s" % (i, str(DayInstant(i)))))
