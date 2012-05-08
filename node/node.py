#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  node.py
#
#  Copyright 2012 Delin <delin@eridan.la>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.


from flask import Flask
from time import sleep, ctime, time
from os import uname, getloadavg
from psutil import phymem_usage, cached_phymem, virtmem_usage, cpu_percent, disk_usage, get_pid_list
from pycpuid import brand_string as cpu_brand_name
import json, threading, socket, select, sys


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DEV-SERVER-NODE_SETTINGS', silent = True)
app.secret_key = 'B*%^F56k(OAwcc. 0 ¤'
DEBUG = True

start_time = time()
services_run = 0

class server_handler (threading.Thread):
	def __init__ (self, host = "0.0.0.0", port = 9910):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.backlog = 16
		self.server = None

	def run (self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server.bind((self.host, self.port))
			self.server.listen(self.backlog)
		except socket.error, (value,message):
			if self.server:
				self.server.close()
			print "Could not open socket: " + message
			return False

		print "Server started."

		while True:
			self.client, self.address = self.server.accept()
			if not self.client:
				break

			self.engine()
			self.client.close()

		self.shutdown()

	def shutdown (self):
		self.server.close()

	def msg_send (self, data):
		if not data:
			return False

		return self.client.send(json.dumps(data) + '\n')

	def msg_recv (self):
		buf = ''
		msg = ''

		while buf != '\n':
			msg = msg + buf
			buf = self.client.recv(1)
			if len(buf) <= 0:
				return ''

		#~ print "<--", msg
		return json.loads(msg)

	def engine (self):
		# Auth
		self.msg_send(node_stat())

def get_uptime (unix_time = None):
	if not unix_time:
		try:
			f = open( "/proc/uptime" )
			contents = f.read().split()
			f.close()
		except Exception, ex:
			print "Cannot open get_uptime file: /proc/get_uptime", ex
			return False

		total_seconds = float(contents[0])
	else:
		total_seconds = unix_time

	# Helper vars:
	MINUTE	= 60
	HOUR	= MINUTE * 60
	DAY	= HOUR * 24

	# Get the days, hours, etc:
	days	= int( total_seconds / DAY )
	hours	= int( ( total_seconds % DAY ) / HOUR )
	minutes = int( ( total_seconds % HOUR ) / MINUTE )
	seconds = int( total_seconds % MINUTE )

	# Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
	string = ""
	if days > 0:
		string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
	if len(string) > 0 or hours > 0:
		string += (hours < 10 and "0" + str(hours) or str(hours)) + ":"
	if len(string) > 0 or minutes > 0:
		string += (minutes < 10 and "0" + str(minutes) or str(minutes)) + ":"

	string += (seconds < 10 and "0" + str(seconds) or str(seconds))

	return string


@app.route('/')
def page_index ():
	""" Function doc """
	return "Helo"

def node_stat():
	stat_phymem_usage = phymem_usage()
	stat_virtmem_usage = virtmem_usage()

	sys_stats = dict(
		srv_uptime	= int(time() - start_time),
		services	= services_run,

		load_avarage	= getloadavg(),
		date		= ctime(),
		uptime		= get_uptime(),
		cpu_percent	= int(cpu_percent(interval = 0)),
		mem_percent	= int(stat_phymem_usage.percent),
		mem_usage	= (stat_phymem_usage.used - cached_phymem()) / 1024 / 1024,
		mem_total	= stat_phymem_usage.total / 1024 / 1024,
		swap_percent	= int(stat_virtmem_usage.percent),
		swap_usage	= stat_virtmem_usage.used / 1024 / 1024,
		swap_total	= stat_virtmem_usage.total / 1024 / 1024,
		disk_percent	= int(disk_usage('/home').percent),
		disk_usage	= disk_usage('/home').used / 1024 / 1024 / 1024,
		disk_total	= disk_usage('/home').total / 1024 / 1024 / 1024,
		procs_total	= len(get_pid_list())
	)

	return sys_stats


if __name__ == "__main__":
	srv = server_handler('0.0.0.0', 9910)			# handle the server socket
	srv.start()

	#~ app.run(host = '0.0.0.0', port = 9900, debug = DEBUG)
