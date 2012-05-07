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


from flask import Flask, jsonify
from time import sleep, ctime, time
from os import uname, getloadavg
from psutil import phymem_usage, cached_phymem, virtmem_usage, cpu_percent, disk_usage, get_pid_list
from pycpuid import brand_string as cpu_brand_name


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DEV-SERVER-NODE_SETTINGS', silent = True)
app.secret_key = 'B*%^F56k(OAwcc. 0 ¤'
DEBUG = True

start_time = time()


def get_uptime ():
	""" Function doc """
	try:
		f = open( "/proc/uptime" )
		contents = f.read().split()
		f.close()
	except Exception, ex:
		print "Cannot open get_uptime file: /proc/get_uptime", ex
		return False

	return int(float(contents[0]))


@app.route('/node_stats')
def node_stat():
	stat_phymem_usage = phymem_usage()
	stat_virtmem_usage = virtmem_usage()

	dev_stats = dict(
		uptime = int(time() - start_time)
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

	return jsonify(sys_stats = sys_stats, dev_stats = dev_stats)


if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 9900, debug = DEBUG)
