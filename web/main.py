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


from flask import Flask, url_for, render_template


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DEV-SERVER_SETTINGS', silent = True)
app.secret_key = 'bb5d 580;$ 2 b8cfc6a2 …'
DEBUG = True


@app.route("/")
def page_index():
	url_for('static', filename = 'css/*.css')
	url_for('static', filename = 'img/*.png')
	url_for('static', filename = 'js/*.js')

	return render_template('pages/index.html')

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 8081, debug = DEBUG)
