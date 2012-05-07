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
from time import sleep, ctime
from os import uname, getloadavg
from psutil import phymem_usage, cached_phymem, virtmem_usage, cpu_percent, disk_usage, get_pid_list
from pycpuid import brand_string as cpu_brand_name


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DEV-SERVER_SETTINGS', silent = True)
app.secret_key = 'bb5d 580;$ 2 b8cfc6a2 …'
DEBUG = True

def system_uptime():
	try:
		f = open( "/proc/uptime" )
		contents = f.read().split()
		f.close()
	except Exception, ex:
		print "Cannot open uptime file: /proc/uptime", ex
		return False

	total_seconds = float(contents[0])

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
def ajax_stat():
	stat_phymem_usage = phymem_usage()
	stat_virtmem_usage = virtmem_usage()

	sys_stats = dict(
		load_avarage	= getloadavg(),
		date		= ctime(),
		uptime		= system_uptime(),
		cpu_percent	= cpu_percent(interval = 0),
		mem_percent	= stat_phymem_usage.percent,
		mem_usage	= (stat_phymem_usage.used - cached_phymem()) / 1024 / 1024,
		mem_total	= stat_phymem_usage.total / 1024 / 1024,
		swap_percent	= stat_virtmem_usage.percent,
		swap_usage	= stat_virtmem_usage.used / 1024 / 1024,
		swap_total	= stat_virtmem_usage.total / 1024 / 1024,
		disk_percent	= disk_usage('/home').percent,
		disk_usage	= disk_usage('/home').used / 1024 / 1024 / 1024,
		disk_total	= disk_usage('/home').total / 1024 / 1024 / 1024,
		procs_total	= len(get_pid_list())
	)

	return jsonify(sys_stats = sys_stats)

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
