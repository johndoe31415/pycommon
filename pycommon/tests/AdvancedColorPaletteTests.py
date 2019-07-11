#	pycommon - Collection of various useful Python utilities.
#	Copyright (C) 2019-2019 Johannes Bauer
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

import os
import unittest
import pycommon
from pycommon.AdvancedColorPalette import AdvancedColorPalette

class AdvancedColorPaletteTests(unittest.TestCase):
	def setUp(self):
		directory = os.path.dirname(pycommon.AdvancedColorPalette.__file__)
		self._json_filename = directory + "/palettes.json"

	def test_doesnt_exists(self):
		with self.assertRaises(KeyError):
			AdvancedColorPalette.load_from_json(self._json_filename, "does_not_exist")

	def test_flatui(self):
		palette = AdvancedColorPalette.load_from_json(self._json_filename, "flatui")

		self.assertEqual(palette[0], (0x1a, 0xbc, 0x9c))
#		self.assertEqual(palette["emerland"], (0x2e, 0xcc, 0x71))
		self.assertEqual(palette[1], (0x7f, 0x8c, 0x8d))
