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
#	File UUID 95aa265b-97c2-42d9-bf79-d2372e044f76

import datetime

class SingularPlural(object):
	def __init__(self, singular, plural, one_word = None):
		self._singular = singular
		self._plural = plural
		self._one_word = one_word

	def __call__(self, i):
		if i == 1:
			if self._one_word is None:
				return "%d %s" % (i, self._singular)
			else:
				return "%s %s" % (self._one_word, self._singular)
		else:
			return "%d %s" % (i, self._plural)

class DayInstantGerman(object):
	"""Formats an instant in time, i.e something like 'tomorrow' or 'in 10
	weeks' or '4 months ago'."""
	_DAY_FORMAT = SingularPlural("Tag", "Tagen", "einem")
	_WEEK_FORMAT = SingularPlural("Woche", "Wochen", "einer")
	_MONTH_FORMAT = SingularPlural("Monat", "Monaten", "einem")
	_YEAR_FORMAT = SingularPlural("Jahr", "Jahren", "einem")

	def __init__(self, days):
		if isinstance(days, datetime.timedelta):
			self._days = round(days.total_seconds() / 86400)
		else:
			self._days = days

	@staticmethod
	def _convertlarge(days):
		days = abs(days)
		if days <= (8 * 7):
			if (days % 7) == 0:
				return DayInstant._WEEK_FORMAT(days // 7)
			else:
				return "%s und %s" % (DayInstant._WEEK_FORMAT(days // 7), DayInstant._DAY_FORMAT(days % 7))
		else:
			approxmonths = round(days / 365 * 12)
			if approxmonths == 6:
				return "etwa einem halben Jahr"
			elif approxmonths == 9:
				return "etwa einem dreiviertel Jahr"
			elif approxmonths < 12:
				return "etwa %s" % (DayInstant._MONTH_FORMAT(approxmonths))
			else:
				approxyears = round(days / 365)
				return "etwa %s" % (DayInstant._YEAR_FORMAT(approxyears))

	def __str__(self):
		s = ""

		if self._days < -7:
			s += "vor %s" % (DayInstant._convertlarge(self._days))
		elif self._days < -2:
			s += "vor %d Tagen" % (abs(self._days))
		elif self._days == -2:
			s += "vorgestern"
		elif self._days == -1:
			s += "gestern"
		elif self._days == 0:
			s += "heute"
		elif self._days == 1:
			s += "morgen"
		elif self._days == 2:
			s += "übermorgen"
		elif self._days < 7:
			s += "in %d Tagen" % (abs(self._days))
		elif self._days == 7:
			s += "heute in einer Woche"
		elif self._days == 8:
			s += "morgen in einer Woche"
		else:
			s += "in %s" % (DayInstant._convertlarge(self._days))

		return s

class DayInstantEnglish(object):
	"""Formats an instant in time, i.e something like 'tomorrow' or 'in 10
	weeks' or '4 months ago'."""
	_DAY_FORMAT = SingularPlural("day", "days", "one")
	_WEEK_FORMAT = SingularPlural("week", "weeks", "one")
	_MONTH_FORMAT = SingularPlural("month", "months", "one")
	_YEAR_FORMAT = SingularPlural("year", "years", "one")

	def __init__(self, days):
		if isinstance(days, datetime.timedelta):
			self._days = round(days.total_seconds() / 86400)
		else:
			self._days = days

	@classmethod
	def _convertlarge(cls, days):
		days = abs(days)
		if days <= (8 * 7):
			if (days % 7) == 0:
				return cls._WEEK_FORMAT(days // 7)
			else:
				return "%s and %s" % (cls._WEEK_FORMAT(days // 7), cls._DAY_FORMAT(days % 7))
		else:
			approxmonths = round(days / 365 * 12)
			if approxmonths == 6:
				return "about half a year"
			elif approxmonths < 12:
				return "about %s" % (cls._MONTH_FORMAT(approxmonths))
			else:
				approxyears = round(days / 365)
				return "about %s" % (cls._YEAR_FORMAT(approxyears))

	def __str__(self):
		s = ""

		if self._days < -7:
			s += "%s ago" % (self._convertlarge(self._days))
		elif self._days < -2:
			s += "%d days ago" % (abs(self._days))
		elif self._days == -2:
			s += "the day before yesterday"
		elif self._days == -1:
			s += "yesterday"
		elif self._days == 0:
			s += "today"
		elif self._days == 1:
			s += "tomorrow"
		elif self._days == 2:
			s += "the day after tomorrow"
		elif self._days < 7:
			s += "in %d days" % (abs(self._days))
		elif self._days == 7:
			s += "a week today"
		elif self._days == 8:
			s += "a week tomorrow"
		else:
			s += "in %s" % (self._convertlarge(self._days))

		return s


class DayPeriodEnglish(object):
	"""Formats a period of time, i.e something like 'three months' or 'two
	days'."""
	_DAY_FORMAT = SingularPlural("day", "days", "one")
	_WEEK_FORMAT = SingularPlural("week", "weeks", "one")
	_MONTH_FORMAT = SingularPlural("month", "months", "one")
	_YEAR_FORMAT = SingularPlural("year", "years", "one")

	def __init__(self, days):
		if isinstance(days, datetime.timedelta):
			self._days = round(days.total_seconds() / 86400)
		else:
			self._days = days
		self._days = abs(self._days)

	@classmethod
	def _convertlarge(cls, days):
		days = abs(days)
		if days <= (8 * 7):
			if (days % 7) == 0:
				return cls._WEEK_FORMAT(days // 7)
			else:
				return "%s and %s" % (cls._WEEK_FORMAT(days // 7), cls._DAY_FORMAT(days % 7))
		else:
			approxmonths = round(days / 365 * 12)
			if approxmonths == 6:
				return "about half a year"
			elif approxmonths < 12:
				return "about %s" % (cls._MONTH_FORMAT(approxmonths))
			else:
				approxyears = round(days / 365)
				return "about %s" % (cls._YEAR_FORMAT(approxyears))

	def __str__(self):
		s = ""
		if self._days == 0:
			s += "no amount of time"
		elif self._days < 7:
			s += self._DAY_FORMAT(self._days)
		elif self._days == 7:
			s += "one week"
		else:
			s += "%s" % (self._convertlarge(self._days))

		return s

if __name__ == "__main__":
	laststringrepr = None
	#for i in range(-4000, 4000):
	for i in range(4000):
		stringrepr = str(DayPeriodEnglish(i))
		if stringrepr != laststringrepr:
			print("%5d %5.1f yrs: %s " % (i, i / 365, stringrepr))
			laststringrepr = stringrepr
