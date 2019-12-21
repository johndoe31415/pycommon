#!/usr/bin/python3
#
#	JobServer - Schedule multiple jobs in a parallelized fashion.
#	Copyright (C) 2016-2019 Johannes Bauer
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
#	File UUID b9be1e6c-c465-4930-8ac0-f4456d344d9e

import threading
import os
import enum
import time
import subprocess

class JobStatus(enum.IntEnum):
	idle = 0
	running = 1
	finished = 2
	closed = 3

class Job():
	def __init__(self):
		self._jobserver = None
		self._status = JobStatus.idle
		self._successful = None
		self._depends = [ ]

	@property
	def jobserver(self):
		return self._jobserver

	@jobserver.setter
	def jobserver(self, value):
		assert(self._jobserver is None)
		self._jobserver = value

	@property
	def status(self):
		return self._status

	@status.setter
	def status(self, value):
		assert(isinstance(value, JobStatus))
		self._status = value

	@property
	def successful(self):
		return self._successful

	@successful.setter
	def successful(self, value):
		assert(self._successful is None)
		self._successful = value

	def add_dependency(self, job):
		self._depends.append(job)
		return self

	def register(self, jobserver):
		assert(self._jobserver is None)
		self._jobserver = jobserver

	def execute(self):
		raise Exception(NotImplemented)

	@property
	def should_start(self):
		"""Returns if the job is stuck in idle state and has all its
		prerequisites satisfied."""
		return (self.status == JobStatus.idle) and all((job.status == JobStatus.closed) and (job.successful is True) for job in self._depends)

	@property
	def can_never_start(self):
		"""Returns if the job is stuck in idle state and can never be started because dependencies failed."""
		return (self.status == JobStatus.idle) and any((job.status == JobStatus.closed) and (job.successful is False) for job in self._depends)

	def chain(self, job):
		job.add_dependency(self)
		self.jobserver.add(job)
		return job

class ExecuteCommandJob(Job):
	def __init__(self, command, success_errcodes = None):
		Job.__init__(self)
		self._command = command
		if success_errcodes is None:
			self._success_errcodes = [ 0 ]
		else:
			self._success_errcodes = success_errcodes
		self._proc = None

	def execute(self):
		self.status = JobStatus.running
		self._proc = subprocess.Popen(self._command)
		returncode = self._proc.wait()
		self.successful = returncode in self._success_errcodes
		self.status = JobStatus.finished

	def __str__(self):
		return "[%s] ExecuteJob<%s>" % (self.status, " ".join(self._command))

class RemoveFileJob(Job):
	def __init__(self, filename):
		Job.__init__(self)
		self._filename = filename

	def execute(self):
		self.status = JobStatus.running
		try:
			os.unlink(self._filename)
			self.successful = True
		except Exception as e:
			print("Unlink failed", e)
			self.successful = False
		self.status = JobStatus.finished

	def __str__(self):
		return "[%s] RemoveFileJob<%s>" % (self.status, self._filename)

class _JobExecutionWorker(threading.Thread):
	def __init__(self, job):
		threading.Thread.__init__(self)
		self._job = job

	def run(self):
		#print(self._job)
		self._job.execute()
		self._job.jobserver.notify()

class _TimingThread(threading.Thread):
	def __init__(self, interval, callback):
		threading.Thread.__init__(self)
		self._quit = False
		self._interval = interval
		self._callback = callback
		self._cond = threading.Condition()

	def quit(self):
		self._quit = True

	def notify(self):
		with self._cond:
			self._cond.notify_all()

	def run(self):
		while not self._quit:
			self._callback()
			with self._cond:
				self._cond.wait(timeout = self._interval)


class JobServer():
	def __init__(self, concurrent_job_count, verbose = True):
		self._concurrent_cnt = concurrent_job_count
		self._lock = threading.Lock()
		self._run_cnt = 0
		self._jobs = [ ]
		self._verbose = verbose
		self._timer = _TimingThread(0.1, self._callback)
		self._timer.start()

	def notify(self):
		self._timer.notify()

	def _callback(self):
		with self._lock:
#			print("List:")
#			for job in self._jobs:
#				print(job)
#			print()

			# Collect finished jobs first
			for job in self._jobs:
				if job.status == JobStatus.finished:
					# Close job
					self._run_cnt -= 1
					job.status = JobStatus.closed
#					print("> Closed finished %s Success = %s" % (job, job.successful))
				elif job.can_never_start:
					# Mark as failed as well
					job.successful = False
					job.status = JobStatus.closed
#					print("> Failed propagation", job, job.successful)

			# Walk through and possibly start new jobs
			for job in self._jobs:
				# Could we start new jobs?
				if self._run_cnt >= self._concurrent_cnt:
#					print("Can't start any new")
					# Nope.
					break

				if job.should_start:
					if self._verbose:
						print("Starting: %s" % (str(job)))
					_JobExecutionWorker(job).start()
					self._run_cnt += 1

	def add(self, job, after_list = None):
		with self._lock:
			job.jobserver = self
			if after_list is not None:
				for after_job in after_list:
					job.add_dependency(after_job)
			self._jobs.append(job)
		return job

	def shutdown(self):
		while True:
			with self._lock:
				all_done = all(job.status == JobStatus.closed for job in self._jobs)
				if all_done:
					self._timer.quit()
					return all(job.successful for job in self._jobs)
			time.sleep(0.1)


if __name__ == "__main__":
	js = JobServer(8)
	for i in range(100):
		job = js.add(ExecuteCommandJob([  "convert", "-size", "1000x1000", "xc:white", "canvas%03d.png" % (i) ]))
		job = job.chain(ExecuteCommandJob([ "convert", "canvas%03d.png" % (i), "canvas%03d.jpg" % (i) ]))
		job = job.chain(RemoveFileJob("canvas%03d.png" % (i)))
		job = job.chain(ExecuteCommandJob([ "convert", "canvas%03d.jpg" % (i), "canvas%03d.pnm" % (i) ]))
		job = job.chain(RemoveFileJob("canvas%03d.jpg" % (i)))
#	job = job.chain(RemoveFileJob("error"))
	success = js.shutdown()
	print("Finished!", success)

