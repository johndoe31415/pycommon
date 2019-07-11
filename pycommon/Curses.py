#!/usr/bin/python3
#
#	Curses - Very simple ncurses abstraction layer.
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
#	File UUID 9d4357f3-4643-471a-abf7-af0ad79959f8

import curses

class ProgressBar():
	def __init__(self, parent, height, width, y, x, maxval = 100, bgcolor = None, textcolor = None):
		assert(height >= 3)
		assert(width >= 10)
		self._parent = parent
		self._win = parent.subwin(height, width, y, x)
		if bgcolor is not None:
			self._win.bkgd(bgcolor)
		self._win.box()
		self._win.refresh()
		self._value = 0
		self._maxval = maxval
		self._textcolor = textcolor

	def getwidth(self):
		return self._win.getmaxyx()[1]

	def getwin(self):
		return self._win

	def _setctrtext(self, text):
#		print(dir(self._win), file = open("x", "w"))
		pos = round((self.getwidth() / 2) - (len(text) / 2))
		if self._textcolor is None:
			self._win.addstr(1, pos, text)
		else:
			self._win.addstr(1, pos, text, self._textcolor)

	def _getfancymidtext(self):
		width = self.getwidth() - 2
		fltcharsfilled = self._value / self._maxval * width
		fullcharsfilled = int(fltcharsfilled)
		halfcharfilled = fltcharsfilled - fullcharsfilled

		charsempty = width - fullcharsfilled - 1
		if charsempty < 0:
			charsempty = 0
		if fullcharsfilled == width:
			halfchar = ""
		else:
			if halfcharfilled <= (1 / 8):
				halfchar = "▏"
			elif halfcharfilled <= (2 / 8):
				halfchar = "▎"
			elif halfcharfilled <= (3 / 8):
				halfchar = "▍"
			elif halfcharfilled <= (4 / 8):
				halfchar = "▌"
			elif halfcharfilled <= (5 / 8):
				halfchar = "▋"
			elif halfcharfilled <= (6 / 8):
				halfchar = "▊"
			elif halfcharfilled <= (7 / 8):
				halfchar = "▉"
			else:
				halfchar = "█"
		return ("█" * fullcharsfilled) + halfchar + (" " * charsempty)
	
	def _getmidtext(self):
		width = self.getwidth() - 2
		fltcharsfilled = self._value / self._maxval * width
		fullcharsfilled = round(fltcharsfilled)
		charsempty = width - fullcharsfilled
		return ("*" * fullcharsfilled) + (" " * charsempty)

	def setprogress(self, value):
		self._value = value		
		
		# Set bar first
		if self._textcolor is None:
			self._win.addstr(1, 1, self._getmidtext())
		else:
			self._win.addstr(1, 1, self._getmidtext(), self._textcolor)
	
		# Then text over it
		percent = self._value / self._maxval * 100
		if percent < 0:
			percent = 0
		elif percent > 100:
			percent = 100
		text = " %5.1f%% " % (percent)
		self._setctrtext(text)

		self._win.refresh()

class LogWindow():
	def __init__(self, parent, height, width, y, x, color = None):
		self._width = width
		self._height = height
		self._parent = parent
		self._win = parent.subwin(height, width, y, x)
		if color is not None:
			self._win.bkgd(color)
		self._win.box()
		self._win.refresh()

		self._textwin = self._win.subwin(height - 2, width - 2, y + 1, x + 1)
		self._textwin.scrollok(True)

	def msg(self, text, color = None):
		self._textwin.scroll()
		text = text[:self._width - 3]
		if color is not None:
			self._textwin.addstr(self._height - 3, 0, text, color)
		else:
			self._textwin.addstr(self._height - 3, 0, text)
		curses.color_pair(0)
		self._textwin.refresh()

class Curses():
	def __init__(self):
		self._mainscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)
		curses.start_color()
		self._colors = { }
		self._mainscr.refresh()

	def getscr(self):
		return self._mainscr

	def getcolor(self, foreground, background):
		coltuple = (foreground, background)
		if coltuple in self._colors:
			return curses.color_pair(self._colors[coltuple])
		newcol = len(self._colors) + 1
		self._colors[coltuple] = newcol
		curses.init_pair(newcol, foreground, background)
		return curses.color_pair(newcol)

	def getboxedscr(self, color = None):
		if color is not None:
			self._mainscr.bkgd(color)
		self._mainscr.border(0)
		self._mainscr.refresh()
		(height, width) = self._mainscr.getmaxyx()
		subscr = self._mainscr.subwin(height - 2, width - 2, 1, 1)
		subscr.clear()
		return subscr

	def resizeevent(self):
		self._mainscr.nodelay(True)
		char = self._mainscr.getch()
		resize = False
		while char != -1:
			if char == curses.KEY_RESIZE:
				resize = True
			char = self._mainscr.getch()
		return resize

	def close(self):
		curses.endwin()

if __name__ == "__main__":
	import time
	try:
		c = Curses()
		
		scr = c.getboxedscr(c.getcolor(curses.COLOR_WHITE, curses.COLOR_BLUE))
		scr.addstr(0, 1, "Current action:")
		scr.addstr(1, 1, "Started at:")
		scr.addstr(2, 1, "Running for:")
		scr.refresh()

		p = ProgressBar(scr, 3, scr.getmaxyx()[1], 5, 1, 100, c.getcolor(curses.COLOR_WHITE, curses.COLOR_BLUE), c.getcolor(curses.COLOR_GREEN, curses.COLOR_BLUE))
		l = LogWindow(scr, 9, 20, 8, 1, c.getcolor(curses.COLOR_WHITE, curses.COLOR_BLUE))
		for i in range(101):
			p.setprogress(i)
			if (i % 3) == 0:
				l.msg("Normal %d" % (i))
			elif (i % 3) == 1:
				l.msg("Error %d" % (i), c.getcolor(curses.COLOR_RED, curses.COLOR_BLUE))
			else:
				l.msg("OK %d" % (i), c.getcolor(curses.COLOR_GREEN, curses.COLOR_BLUE))
			l.msg("long messassssssssssssssssssssssssssssssssssssssssssssssssssage")

			if c.resizeevent():
				scr = c.getboxedscr(c.getcolor(curses.COLOR_WHITE, curses.COLOR_BLUE))
				scr.clear()
				scr.addstr(0, 1, "Current action:")
				scr.addstr(1, 1, "Started at:")
				scr.addstr(2, 1, "Running for:")
				scr.refresh()
				p = ProgressBar(scr, 3, scr.getmaxyx()[1], 5, 1, 100, c.getcolor(curses.COLOR_WHITE, curses.COLOR_BLUE), c.getcolor(curses.COLOR_GREEN, curses.COLOR_BLUE))
				l = LogWindow(scr, 9, 20, 8, 1, c.getcolor(curses.COLOR_WHITE, curses.COLOR_BLUE))

			time.sleep(0.1)

		scr.addstr(25, 2, "Press key")
		scr.refresh()
		c.getscr().getch()
		c.close()
	except:
		curses.endwin()
		raise

