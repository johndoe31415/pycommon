#!/usr/bin/python3
#
#       DebugConsole - Simple interactive Python console
#       Copyright (C) 2011-2012 Johannes Bauer
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
#
#       File UUID 30888f5e-4b2e-4e24-ba80-2b3a1b26f76d

import code
import readline
import atexit
import os

class DebugConsole(code.InteractiveConsole):
	def __init__(self, localvars = None, histfile = os.path.expanduser("~/.dbgconsole-history")):
		code.InteractiveConsole.__init__(self, localvars)
		self.init_history(histfile)

	def init_history(self, histfile):
		readline.parse_and_bind("tab: complete")
		if hasattr(readline, "read_history_file"):
			try:
				readline.read_history_file(histfile)
			except IOError:
				pass
			atexit.register(self.save_history, histfile)

	def save_history(self, histfile):
		readline.write_history_file(histfile)

