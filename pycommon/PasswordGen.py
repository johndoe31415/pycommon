#!/usr/bin/python3
#
#	PasswordGen - Generate secure passwords.
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
#	File UUID 2dcdfca8-2c20-4feb-b2a0-b4d0273a52a7

import os
import string

class PasswordGen():
	_AMBIGUOUS_CHARS = set("oO0" + "Iil1" + "uv" + "UV" + "B8" + "2Z" + "6G")
	_SPECIAL_CHARS = set("!$%/-_:#")

	def __init__(self, include_uppercase = True, include_numbers = True, include_special = False, strip_ambiguous_chars = True, check_predicate = None, min_char_length = 0):
		"""Using a predicate to validate the password after random generation
		is really bad security practice, but sometimes we cannot get around it.
		For example, many services make the misguided decision of requiring at
		least one special character in the passphrase, making this a necessity.
		For maximum security, leave check_predicate as None."""
		alphabet = set(string.ascii_lowercase)
		if include_uppercase:
			alphabet |= set(string.ascii_uppercase)
		if include_numbers:
			alphabet |= set(string.digits)
		if include_special:
			alphabet |= self._SPECIAL_CHARS
		if strip_ambiguous_chars:
			alphabet = alphabet - self._AMBIGUOUS_CHARS
		self._alphabet = "".join(sorted(alphabet))
		self._check_predicate = check_predicate
		self._min_char_length = min_char_length
		assert(len(self._alphabet) >= 2)

	def _gen_value(self, bit_length):
		byte_length = (bit_length + 7) // 8
		random_data = os.urandom(byte_length)
		assert(len(random_data) == byte_length)
		return int.from_bytes(random_data, byteorder = "little")

	def _generate(self, bit_length, min_pass_length):
		assert(bit_length > 0)
		value = self._gen_value(bit_length)
		password = ""
		while (value > 0) or (len(password) < min_pass_length):
			(value, charno) = divmod(value, len(self._alphabet))
			password += self._alphabet[charno]
		return password

	@classmethod
	def predicate_satisfies_alphabets(cls, password, *alphabets):
		password = set(password)
		return all(len(password & set(alphabet)) > 0 for alphabet in alphabets)

	@classmethod
	def predicate_includes_special(cls, password):
		return cls.predicate_satisfies_alphabets(password, cls._SPECIAL_CHARS)

	@classmethod
	def predicate_includes_upper_lower_digit_special(cls, password):
		return cls.predicate_satisfies_alphabets(password, string.ascii_uppercase, string.ascii_lowercase, string.digits, cls._SPECIAL_CHARS)

	def generate(self, bit_length = 128):
		min_char_bit_length = (len(self._alphabet) ** self._min_char_length).bit_length()
		bit_length = max(bit_length, min_char_bit_length)
		while True:
			candidate = self._generate(bit_length, self._min_char_length)
			if self._check_predicate is None:
				break
			if self._check_predicate(candidate):
				break
		return candidate
