# -*- coding: utf-8 -*-

# Copyright (C) 2018 Keith Zubot-Gephart
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Public transport stops and departures from Edmonton Transit (ETS).

http://www.takeets.com
https://data.edmonton.ca

"""

import json
import pan


# There's a bunch of different JSON feeds we need
url_bus_stops = "https://data.edmonton.ca/resource/kgzg-mxv6.json"
url_stop_times = "https://data.edmonton.ca/resource/brqx-qet8.json"
url_bus_routes = "https://data.edmonton.ca/resource/atvz-ppyb.json" # https://data.edmonton.ca/Transit/ETS-Bus-Schedule-GTFS-Data-Feed-Routes/d577-xky7
url_realtime = "https://data.edmonton.ca/download/uzpc-8bnm/application%2Foctet-stream" # https://data.edmonton.ca/Transit/Real-Time-Trip-Updates-GTFS-PB-File-/uzpc-8bnm
url_trips = "https://data.edmonton.ca/resource/qguy-a9de.json" # https://data.edmonton.ca/Transit/ETS-Bus-Schedule-GTFS-Data-Feed-Trips/ctwr-tvrd

routes_raw = pan.http.get_json(url_bus_routes, encoding="utf_8")
routes = {}
for entry in routes_raw:
	routes[entry['route_id']] = {}
	routes[entry['route_id']]['route_long_name'] = entry['route_long_name']
	routes[entry['route_id']]['route_short_name'] = entry['route_short_name']


def find_departures(stops):
	"""Return a list of departures from `stops`."""
	output = []
	#param = "?$where=stop_id in [" + ",".join(stops) + "]"
	#url = url_stop_times + param
	#print("Trying url: " + url)
	#request = pan.http.get_json(url, encoding="utf_8")
	#print(request)
	for stop in stops:
		url = url_stop_times + "?stop_id=" + stop
		print("Trying url: " + url)
		entries = pan.http.get_json(url, encoding="utf_8")
		for entry in entries:
			#print(entry)
			trip = pan.http.get_json((url_trips + "?trip_id=" + entry['trip_id']), encoding="utf_8")
			#print(trip)
			output.append({
				"destination": routes[trip[0]['route_id']]['route_long_name'],
				"line": routes[trip[0]['route_id']]['route_short_name'],
				"realtime": False,
				"scheduled_time": "100",
				"stop": entry['stop_id'],
				"time": "100",
			})
			#print(output)
	return output
