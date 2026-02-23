#	kartfire - Test framework to consistently run submission files
#	Copyright (C) 2023-2026 Johannes Bauer
#
#	This file is part of kartfire.
#
#	kartfire is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	kartfire is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with kartfire; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import enum
import collections
import dataclasses

class CellFormatter():
	_BASIC = { }

	class Alignment(enum.IntEnum):
		Left = enum.auto()
		Center = enum.auto()
		Right = enum.auto()

	class Color(enum.Enum):
		Default = ("", "")
		Red = ("\x1b[31m", "\x1b[0m")
		Green = ("\x1b[32m", "\x1b[0m")
		Yellow = ("\x1b[33m", "\x1b[0m")
		Blue = ("\x1b[34m", "\x1b[0m")
		Purple = ("\x1b[35m", "\x1b[0m")
		Cyan = ("\x1b[36m", "\x1b[0m")

	class Keep():
		pass

	def __init__(self, content_to_str_fnc: callable = str, align: Alignment = Alignment.Left, min_length: int | None = None, max_length: int | None = None, abbreviation_str: str = "…", color: Color = Color.Default):
		self._content_to_str_fnc = content_to_str_fnc
		self._align = align
		self._min_length = min_length
		self._max_length = max_length
		self._abbreviation_str = abbreviation_str
		self._color = color

	def override(self, content_to_str_fnc = Keep, align = Keep, min_length = Keep, max_length = Keep, abbreviation_str = Keep, color = Keep):
		return CellFormatter(
			content_to_str_fnc = self._content_to_str_fnc if (content_to_str_fnc is self.Keep) else content_to_str_fnc,
			align = self._align if (align is self.Keep) else align,
			min_length = self._min_length if (min_length is self.Keep) else min_length,
			max_length = self._max_length if (max_length is self.Keep) else max_length,
			abbreviation_str = self._abbreviation_str if (abbreviation_str is self.Keep) else abbreviation_str,
			color = self._color if (color is self.Keep) else color,
		)

	def string_width(self, string: str) -> int:
		width = len(string)
		char_count = collections.Counter(string)
		width -= char_count["\u0305"]	# Overline sequences do not count as width
		return width

	def width_of(self, content: any):
		length = self.string_width(self._content_to_str_fnc(content))
		if self._min_length is not None:
			length = max(self._min_length, length)
		if self._max_length is not None:
			length = min(self._max_length, length)
		return length

	def __call__(self, content: any, length: int):
		value = self._content_to_str_fnc(content)
		assert(isinstance(value, str))
		width = self.string_width(value)
		if width > length:
			# Value too long, truncate
			value = value[ : length - len(self._abbreviation_str)] + self._abbreviation_str
		elif width < length:
			# Value too short, align
			match self._align:
				case self.Alignment.Left:
					lpad = 0
					rpad = length - width

				case self.Alignment.Center:
					lpad = (length - width) // 2
					rpad = (length - width) - lpad

				case self.Alignment.Right:
					lpad = length - width
					rpad = 0
			value = (" " * lpad) + value + (" " * rpad)
		(prefix, suffix) = self._color.value
		return prefix + value + suffix

	@classmethod
	def basic_lalign(cls):
		if "lalign" not in cls._BASIC:
			cls._BASIC["lalign"] = CellFormatter()
		return cls._BASIC["lalign"]

	@classmethod
	def basic_ralign(cls):
		if "ralign" not in cls._BASIC:
			cls._BASIC["ralign"] = CellFormatter(align = cls.Alignment.Right)
		return cls._BASIC["ralign"]

	@classmethod
	def basic_center(cls):
		if "center" not in cls._BASIC:
			cls._BASIC["center"] = CellFormatter(align = cls.Alignment.Center)
		return cls._BASIC["center"]

class Table():
	class RowType(enum.IntEnum):
		Data = enum.auto()
		Separator = enum.auto()

	@dataclasses.dataclass(frozen = True, slots = True)
	class Row():
		row_type: "RowType"
		data: dict[str, any] | None = None
		cell_formatters: dict[str, CellFormatter] | None = None

	def __init__(self, style: dict | None = None, pad: int = 1):
		self._style = style
		self._pad = pad
		self._rows = [ ]
		self._column_formatters = { }
		if self._style is None:
			self._style = {
				"V":	"│",
				"H":	"─",
				"TL":	"┌",
				"ML":	"├",
				"BL":	"└",
				"TR":	"┐",
				"MR":	"┤",
				"BR":	"┘",
				"TM":	"┬",
				"MM":	"┼",
				"BM":	"┴",
			}

	def format_column(self, col_name: str, formatter: CellFormatter):
		self._column_formatters[col_name] = formatter
		return self

	def format_columns(self, column_format: dict[str, CellFormatter]):
		self._column_formatters.update(column_format)
		return self

	def add_separator_row(self):
		self._rows.append(self.Row(row_type = self.RowType.Separator))
		return self

	def add_row(self, row_data: dict, cell_formatters: dict[str, CellFormatter] | None = None):
		self._rows.append(self.Row(row_type = self.RowType.Data, data = row_data, cell_formatters = cell_formatters))
		return self

	def add_fixed_format_row(self, row_data: dict, fixed_format: CellFormatter):
		return self.add_row(row_data = row_data, cell_formatters = { col_name: fixed_format for col_name in row_data })

	def _get_column_formatter(self, col_name: str):
		if col_name not in self._column_formatters:
			self._column_formatters[col_name] = CellFormatter()
		return self._column_formatters[col_name]

	def _get_cell_formatter(self, col_name: str, row: Row):
		if (row.cell_formatters is not None) and (col_name in row.cell_formatters):
			return row.cell_formatters[col_name]
		else:
			return self._get_column_formatter(col_name)

	def _determine_col_width(self, col_name: str):
		max_length = 0
		for row in self._rows:
			if row.row_type != self.RowType.Data:
				continue
			if col_name not in row.data:
				continue

			cell_content = row.data[col_name]
			cell_formatter = self._get_cell_formatter(col_name, row)
			length = cell_formatter.width_of(cell_content)
			max_length = max(max_length, length)
		return max_length

	def _print_row(self, col_widths: collections.OrderedDict[str, int], row: Row):
		match row.row_type:
			case self.RowType.Data:
				line = [ ]
				for (col_name, col_width) in col_widths.items():
					if col_name not in row.data:
						# Empty cell
						line.append(" " * (col_width + 2 * self._pad))
					else:
						cell_content = row.data[col_name]
						cell_formatter = self._get_cell_formatter(col_name, row)
						line.append((" " * self._pad) + cell_formatter(cell_content, col_width) + (" " * self._pad))
				print(self._style["V"] + self._style["V"].join(line) + self._style["V"])

			case self.RowType.Separator:
				print(self._style["ML"] + self._style["MM"].join(self._style["H"] * (col_width + 2 * self._pad) for col_width in col_widths.values()) + self._style["MR"])

	def _print_head_row(self, col_widths: collections.OrderedDict[str, int]):
		print(self._style["TL"] + self._style["TM"].join(self._style["H"] * (col_width + 2 * self._pad) for col_width in col_widths.values()) + self._style["TR"])

	def _print_tail_row(self, col_widths: collections.OrderedDict[str, int]):
		print(self._style["BL"] + self._style["BM"].join(self._style["H"] * (col_width + 2 * self._pad) for col_width in col_widths.values()) + self._style["BR"])

	def print(self, *col_names: tuple[str]):
		col_widths = collections.OrderedDict((col_name, self._determine_col_width(col_name)) for col_name in col_names)
		col_widths = collections.OrderedDict((col_name, col_width) for (col_name, col_width) in col_widths.items() if col_width != 0)
		self._print_head_row(col_widths)
		for row in self._rows:
			self._print_row(col_widths, row)
		self._print_tail_row(col_widths)

	def __getitem__(self, col_name: str):
		return self._column_formatters[col_name]

if __name__ == "__main__":
	table = Table()

	rfloat_format = CellFormatter(align = CellFormatter.Alignment.Right, content_to_str_fnc = lambda content: f"{content:.2f}")
	table.format_columns({
		"count":		CellFormatter.basic_ralign(),
		"description":	CellFormatter(max_length = 20),
		"price":		rfloat_format,
		"sum":			rfloat_format,
	})

	table.add_row({
		"pos":				"Position",
		"count":			"Count",
		"description":		"Description",
		"price":			"Price",
		"sum":				"Sum",
	}, cell_formatters = {
		"price":		table["price"].override(content_to_str_fnc = str),
		"sum":			table["sum"].override(content_to_str_fnc = str),
	})
	table.add_separator_row()
	table.add_row({
		"pos":				1,
		"count":			4,
		"description":		"Ice Cream",
		"price":			4.90,
		"sum":				4 * 4.90,
	})
	table.add_row({
		"pos":				2,
		"count":			12,
		"description":		"Donut",
		"price":			2.00,
		"sum":				12 * 2.00,
	})
	table.add_row({
		"pos":				3,
		"count":			12,
		"description":		"This is a long item description much too long to display",
		"price":			2.00,
		"sum":				12 * 2.00,
	})
	table.add_row({
		"pos":				4,
		"description":		"Sales Tax",
		"price":			"19%",
		"sum":				0.19 * ((12 * 2) + (4 * 4.90)),
	}, cell_formatters = {
		"price": CellFormatter(align = CellFormatter.Alignment.Right, color = CellFormatter.Color.Red),
	})
	table.add_separator_row()
	table.add_row({
		"description":		"Grand Total",
		"sum":				1.19 * ((12 * 2) + (4 * 4.90)),
	}, cell_formatters = {
		"sum": table["sum"].override(color = CellFormatter.Color.Yellow),
	})

	table.print("pos", "count", "description", "price", "sum")
