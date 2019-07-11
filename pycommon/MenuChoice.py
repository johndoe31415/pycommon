#!/usr/bin/python3
#
#	MenuChoice - Ask one of more options on the command line.
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
#	File UUID 3e2873bd-7c6b-4a0f-992d-87693e0c151d

import collections

_MenuChoice = collections.namedtuple("MenuChoice", [ "itemname", "inputs", "text" ])

class MenuChoice(object):
	def __init__(self, case_sensitive = False):
		self._case_sensitive = case_sensitive
		self._choices = [ ]

	def add(self, itemname, inputs, text):
		if not self._case_sensitive:
			inputs = [ inputvalue.lower() for inputvalue in inputs ]
		self._choices.append(_MenuChoice(itemname = itemname, inputs = tuple(inputs), text = text))
		return self
	
	def question(self, prompt = "Your choice: "):
		for choice in self._choices:
			print(choice.text)
		while True:			
			result = input(prompt)
			if not self._case_sensitive:
				result = result.lower()
		
			for choice in self._choices:
				for inputvalue in choice.inputs:
					if inputvalue == result:
						return choice.itemname

		print(result)

if __name__ == "__main__":
	menu = MenuChoice()
	menu.add("yes", [ "Y" ], "Yes")
	menu.add("no", [ "n" ], "No")
	print(menu.question())
