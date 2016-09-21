from copy import deepcopy
from config import Mongo, haversine
from datetime import datetime
import json,csv
import traceback
from random import randint, sample
import sys
from math import radians, cos, sin, asin, sqrt,atan2,fabs

db = Mongo()
MIN_DISTANCE = 0 # 1 km between points
MAX_DISTANCE = 1 #50 kilometers between points. 
MIN_TIME = 0 # 10 MINUTES IN SECONDS 
MAX_TIME = 3600 #1 DAY IN SECONDS
MIN_ROUTE_UNIQUE_POSTS = 5 

def main():

	print "Hello"
	n = 2 
	#Compute Query Routes given "N"
	
	q_routes = compute_q_routes(n)
	res = []
	i=0
	for iroute in q_routes:
		#does iroute match:
		matches = compute_matches(iroute,[MIN_TIME,MAX_TIME],[MIN_DISTANCE,MAX_DISTANCE])
		res.append([iroute, matches]) 
		print "%s,%" % (i, matches)
		i+=1	

def compute_matches(iroute,t,d):

	counter = 0 #Count # of matches
	routes_cursor = conv_cursor_to_list(db.routes_ig.find())
	
	for a_route in routes_cursor: 
		if does_match(a_route['route'],iroute,t,d):
			counter+=1

	return counter

def does_match(a_route,iroute,t,d):
#	print iroute

	for a_point in iroute:
		if not point_with(a_route,a_point,t,d):
			return False
	return True

def point_with(a_route,a_point,t,d):

	#For each point in route
	for pt in a_route[0]:
		#is j within t and d of a_point
		loc = pt['location']
		a_t = pt['created_time']
		b_loc = a_point['location']
		b_t = a_point['created_time']
		dist = haversine(loc,b_loc)
		delta_t = fabs(a_t-b_t)
		if dist >= min(d) and dist <= max(d) and delta_t >= min(t) and delta_t <= max(t):
			return True
	return False

def compute_q_routes(n):
	q_route_list = []

	routes_cursor = db.routes_ig.find()
	routes_list = conv_cursor_to_list(routes_cursor)
	
	for i in range(0,len(routes_list)):
		
		all_pts = routes_list[i]['route'][0]
		s = sample(all_pts,n)
		#Randomly select n number from list of 0,len(all_points_of_a_route)
				
		q_route_list.append(s)
		
	return q_route_list

def conv_cursor_to_list(routes):
	posts = []
	for i in routes:
		posts.append(i)
	return posts

# This is duplicated. Needs to be removed.
def haversine(coord_1,coord_2):
	
	lat1 = coord_1['latitude']
	lon1 = coord_1['longitude']
	lat2 = coord_2['latitude']
	lon2 = coord_2['longitude']
	# convert decimal degrees to radians
    	lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])

    	# haversine formula
    	dlon = lon2 - lon1
    	dlat = lat2 - lat1
    	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    	c = 2 * atan2(sqrt(a),sqrt(1-a))

    	# 6367 km is the radius of the Earth
    	km = 6367 * c
    	return km


main()

