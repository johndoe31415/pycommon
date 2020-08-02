#!/usr/bin/python3
#
#	MailSender - Simple interface for SMTP email delivery
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
#	File UUID 03a68838-3bed-473c-a13c-d5bd0fd48271

import smtplib
import urllib.parse
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailSender():
	_DEFAULT_PORTS = {
		"smtp":			25,
		"smtps":		465,
		"submission":	587,
	}

	def __init__(self, smtp_uri = "smtp://127.0.0.1", use_starttls = True, auth = None, x_mailer = "https://github.com/johndoe31415/pycommon MailSender"):
		self._uri = urllib.parse.urlparse(smtp_uri)
		assert(self._uri.scheme.lower() in self._DEFAULT_PORTS)
		hostname_port = self._uri.netloc.split(":", maxsplit = 1)
		if len(hostname_port) == 2:
			(self._hostname, self._port) = (hostname_port[0], int(hostname_port[1]))
		else:
			self._hostname = hostname_port[0]
			self._port = self._DEFAULT_PORTS[self._uri.scheme]
		self._starttls = use_starttls
		self._auth = auth
		self._x_mailer = x_mailer

	@staticmethod
	def _format_address(address_input):
		if isinstance(address_input, str):
			return address_input
		else:
			return email.utils.formataddr(address_input)

	def _format_addresses(self, address_input):
		if isinstance(address_input, str):
			return [ self._format_address(address_input) ]
		else:
			return [ self._format_address(address) for address in address_input ]

	def send(self, from_addr, subject, body_text = None, body_html = None, to_addr = None, to_addrs = None, cc_addrs = None, bcc_addrs = None):
		if (to_addr is None) and (to_addrs is None):
			raise ValueError("Either 'to_addr' or 'to_addrs' must be specified.")
		elif (to_addr is not None) and (to_addrs is not None):
			raise ValueError("Either of 'to_addr' or 'to_addrs' must be specified, not both.")
		if (body_text is None) and (body_html is None):
			raise ValueError("At least one of 'body_text' or 'body_html' must be specified.")

		if body_html is None:
			# Text only
			message = MIMEText(body_text, "plain")
		elif body_text is None:
			# HTML only
			message = MIMEText(body_html, "html")
		else:
			# Text and HTML
			message = MIMEMultipart("alternative")
			message.attach(MIMEText(body_text, "plain"))
			message.attach(MIMEText(body_html, "html"))

		from_addr = self._format_address(from_addr)
		if to_addr is not None:
			to_addr = [ self._format_address(to_addr) ]
		else:
			to_addr = self._format_addresses(to_addr)
		message["From"] = from_addr
		message["To"] = ", ".join(to_addr)
		message["Subject"] = subject
		if cc_addrs is not None:
			message["CC"] = ", ".join(self._format_addresses(cc_addrs))
		if bcc_addrs is not None:
			message["BCC"] = ", ".join(self._format_addresses(bcc_addrs))
		message["Date"] = email.utils.formatdate(localtime = True)
		message["MIME-Version"] = "1.0"
		if self._x_mailer is not None:
			message["X-Mailer"] = self._x_mailer
		message = message.as_string()
		print(message)

		if self._uri.scheme.lower() == "smtp":
			conn = smtplib.SMTP(self._hostname, self._port)
		elif self._uri.scheme.lower() == "smtps":
			conn = smtplib.SMTP_SSL(self._hostname, self._port)

		with conn as server:
			if self._starttls and (self._uri.scheme.lower() == "smtp"):
				server.starttls()

			if self._auth is not None:
				server.login(self._auth[0], self._auth[1])

			email_from = email.utils.getaddresses([ from_addr ])[0][1]
			email_to = email.utils.getaddresses([ to_addr[0] ])[0][1]
			server.sendmail(email_from, email_to, message)

if __name__ == "__main__":
	mail = MailSender()
	#mail.send(("Thäng", "thaeng@foo.com") , to_addr = "target@x.de", subject = "Hey there", body_text = "What are you up to?")
	#mail.send(("Thäng", "thaeng@foo.com") , to_addr = "target@x.de", subject = "Hey there", body_html = "<b>What are you up to?</b>")
	mail.send(("Thäng", "thaeng@foo.com") , to_addr = "target@x.de", subject = "Hey there", body_text = "text!", body_html = "<b>What are you up to?</b>")
