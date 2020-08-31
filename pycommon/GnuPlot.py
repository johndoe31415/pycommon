#!/usr/bin/python3
#
#	GnuPlot - Simple abstraction on top of GnuPlot
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
#	File UUID ca1d0fde-959d-4250-857b-1fa64ea1c54d

import subprocess

def _escape(text):
	return text

class GnuPlotDataset():
	def __init__(self, xydata, title = "Graph", plotstyle = "lines", line_width = None, point_size = None, color = None, smooth = None, normalize_y = False, scale_y = 1):
		assert((color is None) or (isinstance(color, str) and (len(color) == 6)))
		assert(plotstyle in [ "lines", "dots", "points", "steps" ])
		assert((smooth is None) or (smooth in [ "cspline", "bezier" ]))
		if isinstance(xydata, dict):
			self._xydata = sorted(xydata.items())
		else:
			self._xydata = xydata
		if normalize_y:
			self._xydata = list(self._normalize(self._xydata))
		self._title = title
		self._plotstyle = plotstyle
		self._line_width = line_width
		self._point_size = point_size
		self._color = color
		self._smooth = smooth
		self._scale_y = scale_y

	@staticmethod
	def _normalize(xydata):
		ysum = 0
		for (x, y) in xydata:
			ysum += y
		if ysum > 0:
			for (x, y) in xydata:
				yield (x, y / ysum)

	@property
	def plot_cmd(self):
		cmd = [ "\"-\" using 1:(%.6e*$2)" % (self._scale_y) ]
		if self._plotstyle is not None:
			cmd += [ "with", self._plotstyle ]
		if self._title is not None:
			cmd += [ "title", "\"%s\"" % (_escape(self._title)) ]
		if self._line_width is not None:
			cmd += [ "linewidth", "%.2f" % (self._line_width) ]
		if self._point_size is not None:
			cmd += [ "pointsize", "%.2f" % (self._point_size) ]
		if self._color is not None:
			cmd += [ "linetype", "rgb", "\"#%s\"" % (self._color) ]
		if self._smooth is not None:
			cmd += [ "smooth", self._smooth ]
		return " ".join(cmd)

	def __iter__(self):
		return iter(self._xydata)

class GnuPlotDiagram():
	def __init__(self, terminal = "pngcairo", default_width = 1920, default_height = 1080, title = None, xtitle = None, ytitle = None):
		self._terminal = terminal
		self._default_width = default_width
		self._default_height = default_height
		self._title = title
		self._xtitle = xtitle
		self._ytitle = ytitle
		self._datasets = [ ]
		self._x_timelabel = None

	def make_timeplot(self, xlabel = "%H:%M:%S"):
		self._x_timelabel = xlabel
		return self

	def add_dataset(self, dataset):
		assert(isinstance(dataset, GnuPlotDataset))
		self._datasets.append(dataset)
		return self

	def gnuplot_source(self):
		yield "set terminal %s size %d,%d" % (self._terminal, self._default_width, self._default_height)
		if self._title is not None:
			yield "set title \"%s\"" % (_escape(self._title))
		if self._xtitle is not None:
			yield "set xlabel \"%s\"" % (_escape(self._xtitle))
		if self._ytitle is not None:
			yield "set ylabel \"%s\"" % (_escape(self._ytitle))
		if self._x_timelabel is not None:
			yield "set xdata time"
			yield "set timefmt \"%s\""
			yield "set format x \"%s\"" % (self._x_timelabel)

		yield "plot %s" % (", ".join(dataset.plot_cmd for dataset in self._datasets))
		yield ""
		for dataset in self._datasets:
			for (x, y) in dataset:
				if self._x_timelabel is None:
					yield "%.6e %.6e" % (x, y)
				else:
					yield "%.6f %.6e" % (x, y)
			yield "e"
			yield ""

	def gnuplot_render(self):
		source = "\n".join(line for line in self.gnuplot_source()) + "\n"
		rendered_doc = subprocess.check_output([ "gnuplot" ], input = source.encode())
		return rendered_doc

	def write_rendered(self, filename):
		with open(filename, "wb") as f:
			f.write(self.gnuplot_render())

if __name__ == "__main__":
	gpd = GnuPlotDiagram(title = "footitle", xtitle = "X axis", ytitle = "Y axis").add_dataset(GnuPlotDataset([ (0, 0), (1, 10), (2, 25), (3, 15), (4, 14) ], line_width = 3, color = "ff0000", plotstyle = "steps", smooth = "cspline"))
	gpd.write_rendered("graph.png")
