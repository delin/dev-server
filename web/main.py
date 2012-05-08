#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  main.py
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


from flask import Flask, url_for, render_template, jsonify
from time import sleep, ctime, time
from os import uname, getloadavg
from psutil import phymem_usage, cached_phymem, virtmem_usage, cpu_percent, disk_usage, get_pid_list
from pycpuid import brand_string as cpu_brand_name
from socket import socket, AF_INET, SOCK_STREAM
import json

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DEV-SERVER_SETTINGS', silent = True)
app.secret_key = 'bb5d 580;$ 2 b8cfc6a2 …'
DEBUG = True

start_time = time()
status_last_update = None
status = None
nodes_last_update = None
nodes = None


class ClientSocket ():
	def __init__(self, host, port):
		self.host = host
		self.port = port

		self.sock = socket(AF_INET, SOCK_STREAM)
		self.connect()

	def connect(self):
		self.sock.connect((self.host, self.port))

	def send(self, msg):
		sent = self.sock.send(msg)
		print "-->", msg

	def recv(self):
		buf = ''
		msg = ''

		while True:
			buf = self.sock.recv(1)

			if buf == '\n':
				break
			else:
				msg += buf

		print "<--", msg
		return msg

	def disconnect(self):
		self.sock.close()

def get_nodes_status ():
	global nodes_last_update
	global nodes

	if nodes and nodes_last_update + 1 >= time():
		return nodes

	nodes_list = []

	nodes_list.append (
		dict (
			hostname = "lilu",
			host = "192.168.1.20",
			port = 9910
		)
	)
	nodes_list.append (
		dict (
			hostname = "kiti",
			host = "192.168.1.100",
			port = 9910
		)
	)
	nodes_list.append (
		dict (
			hostname = "pyweb",
			host = "pyweb.dehome",
			port = 9910
		)
	)

	nodesl = {}
	for node in nodes_list:
		cl = ClientSocket(node['host'], node['port'])
		nodesl[node['hostname']] = json.loads(cl.recv())

	qnodes = jsonify(nodesl)
	nodes_last_update = time()

	return qnodes

def get_status ():
	global status_last_update
	global status

	if status and status_last_update + 1 >= time():
		return status

	stat_phymem_usage = phymem_usage()
	stat_virtmem_usage = virtmem_usage()

	dev_stats = dict(
		uptime = get_uptime(time() - start_time)
	)

	sys_stats = dict(
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

	status = jsonify(sys_stats = sys_stats, dev_stats = dev_stats)
	status_last_update = time()

	return status

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

@app.route('/ajax/sys_stat.json')
def json_stat():
	return get_status()

@app.route('/ajax/nodes_stat.json')
def json_nodes_stat():
	return get_nodes_status()

@app.route("/nodes")
def page_nodes():
	u = uname()
	sys_stats = dict(
		hostname = u[1],
		kernel_name = u[0] + "-" + u[2] + "-" + u[4] +": ",
		cpu_brand = cpu_brand_name()
	)

	return render_template('pages/nodes.html', sys_stats = sys_stats)

@app.route("/")
def page_index():
	url_for('static', filename = 'css/*.css')
	url_for('static', filename = 'img/*.png')
	url_for('static', filename = 'js/*.js')

	u = uname()
	sys_stats = dict(
		hostname = u[1],
		kernel_name = u[0] + "-" + u[2] + "-" + u[4] +": ",
		cpu_brand = cpu_brand_name()
	)

	return render_template('pages/index.html', sys_stats = sys_stats)

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 8081, debug = DEBUG)
