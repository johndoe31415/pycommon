#       pycommon - Generate secure passwords.
#       Copyright (C) 2017-2020 Johannes Bauer
#
#       This file is part of pycommon.
#
#       pycommon is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; this program is ONLY licensed under
#       version 3 of the License, later versions are explicitly excluded.
#
#       pycommon is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with pycommon; if not, write to the Free Software
#       Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#       Johannes Bauer <JohannesBauer@gmx.de>

import unittest
from pycommon.PasswordGen import PasswordGen

class PasswordGenTests(unittest.TestCase):
	@classmethod
	def _genlist(cls, pwgen, count):
		passwords = [ ]
		for i in range(count):
			passwords.append(pwgen.generate())
		return passwords

	@classmethod
	def _genstr(cls, pwgen, count):
		return "".join(cls._genlist(pwgen, count))

	@classmethod
	def _gencharset(cls, pwgen, count):
		return set(cls._genstr(pwgen, count))

	def test_not_static(self):
		passwords = self._genlist(PasswordGen(), 100)
		self.assertEqual(len(passwords), len(set(passwords)))

	def test_ambiguous_present(self):
		char_set = self._gencharset(PasswordGen(strip_ambiguous_chars = False), 100)
		self.assertTrue(("o" in char_set) or ("O" in char_set) or ("0" in char_set))

	def test_ambiguous_absent(self):
		char_set = self._gencharset(PasswordGen(), 100)
		self.assertTrue(("o" not in char_set) and ("O" not in char_set) and ("0" not in char_set))

	def test_check_predicate(self):
		pwgen = PasswordGen(include_special = True, check_predicate = PasswordGen.predicate_includes_special)
		for i in range(100):
			char_set = set(pwgen.generate())
			self.assertTrue(len(char_set & PasswordGen._SPECIAL_CHARS) >= 1)

	def test_min_length(self):
		# Even if bit length is given, when a minimum length is given as well
		# it should influence entropy
		pwgen = PasswordGen(min_char_length = 8)
		passwords = [ ]
		for i in range(100):
			password = pwgen.generate(bit_length = 2)
			passwords.append(password)
			self.assertTrue(len(password) >= 8)
		self.assertEqual(len(passwords), len(set(passwords)))

	def test_check_default_predicates(self):
		pwgen = PasswordGen(include_special = True, check_predicate = PasswordGen.predicate_includes_upper_lower_digit_special)
		self.assertTrue(len(pwgen.generate()) > 8)
