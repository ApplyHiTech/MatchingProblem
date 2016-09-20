from copy import deepcopy
from config import Mongo, haversine
from datetime import datetime
import json,csv
import traceback
from random import randint
import sys
from math import radians, cos, sin, asin, sqrt,atan2

db = Mongo()
MIN_DISTANCE = .5 # 1 km between points
MAX_DISTANCE = 50 #50 kilometers between points. 
MIN_TIME = 300 # 10 MINUTES IN SECONDS 
MAX_TIME = 86400 #1 DAY IN SECONDS
MIN_ROUTE_UNIQUE_POSTS = 5 

def date_filter(posts,d):
    return [x for x in posts if (int(x["created_time"]))>= d and (int(x["created_time"]) <= (d+86400))]


def main():

    t_start = datetime.now()
    # get unique twitter user ids
    instagram_user_ids = db.mapped_instagram_ids.distinct("user_id")

    num_instgram_ids = str(len(instagram_user_ids))
    print "There are %s distinct Instagram users" % num_instgram_ids
    user_count = 1
    routes_count = 0
    routes_added = 0
    route_err = 0
    route_too_short = 0
    user_count_mass = 0
    user_routes = {}
    for uid in instagram_user_ids:
	if(user_count%2500==0):
            print "Break For Loop users: %s " % user_count
#	    break
	user_count+=1
	posts_cursor = db.clean_instagram_posts.find({"user_id":uid}).sort("created_time")
#	print "The user: %s has %s posts" % (uid,posts_cursor.count())
	uid_routes =[]

	if posts_cursor.count() >= MIN_ROUTE_UNIQUE_POSTS: #There are at leats 5 posts by the user...compute routes
		user_count_mass+=1
		
		#Get Routes
		posts_list =[]
		
		for i in posts_cursor:
			posts_list.append(i)


		
		posts_day = []
		i=0 
		# ARE THERE ENOUGH POSSIBLE POSTS FOR A ROUTE? 
		while i < (len(posts_list)-MIN_ROUTE_UNIQUE_POSTS+1):
			curr_post = posts_list[i]
			
			t_start_route=curr_post['created_time']
			t_step = 86400
			t_end_route = t_start_route+t_step
			posts_day[:]=[]
			posts_day=[curr_post]
			
			nextPost = posts_list[i+1]
			j=i+2 #counter for potential posts to add to route.
			prev_post = curr_post
			n_posts_route = 1
			lastTime = prev_post['created_time']
			lastLocation = prev_post['location']

			



			while ( nextPost['created_time'] < t_end_route and j< (len(posts_list)-2)):
				#If post time difference > some min_time add post to route. 
				if isEligiblePost(nextPost,lastTime,lastLocation):
					#addPost to list
					posts_day.append(nextPost)
					lastTime = nextPost['created_time']
					lastLocation = nextPost['location']
					n_posts_route += 1

				nextPost = posts_list[j]

				j+=1

				#Get's all posts on a day. 

			if (len(posts_day)>=5):
				#insert the valid Route
				
				routes_count+=1								
				#Compute Features.
				
				try:
					route_features = compute_features(deepcopy(posts_day))
					db.routes_ig.insert({"user_id":uid,"numb_user_posts":len(posts_list),"route":[deepcopy(posts_day)],"route_features":route_features})
					
					routes_added+=1
					if route_features['route_distance']== -1:
						route_err+=1					
				except: 
					route_err+=1 
				
				i=j
			else:
				i+=1 # We try to compute a route. 

    print "the number of eligible users: %s " % user_count_mass
    print "Routes %s\n Routes with Featurs: %s Error: %s\n Too short: %s " % (routes_count,routes_added,route_err,route_too_short)		

def isEligiblePost(nextPost,lastTime,lastLocation):
	# time between nextpost and last post is 3600 < t < 86400 seconds
	if nextPost['created_time']-lastTime < MIN_TIME:
		return False
	# distance between nextPost and last post 1 km < d < 50 km 
	try:
		dist_km = haversine(nextPost['location'],lastLocation)
#		print "lat1 %s, lon1: %s\nlat2 %s lon2: %s haves: %s\n" % (lastLocation['latitude'],lastLocation['longitude'],nextPost['location']['latitude'],nextPost['location']['longitude'],dist_km)
	except:
		return False
	if dist_km < MIN_DISTANCE or dist_km > MAX_DISTANCE:
		return False
	return True

def compute_features(route):
#	print "Yes. It works"
	time = compute_time(route)
	try:
		distance = compute_distance(route)
	except:
		distance = -1
	
	return {"Length_time": time, "route_distance": distance}

def compute_time(route):
	# get list of all start times
	list_times = []
	for x in route:
		list_times.append(x['created_time'])
	return {"min":  min(list_times), "max": max(list_times), "length": max(list_times)-min(list_times)}
	
	
def compute_distance(route):
	list_distances = []

	for x in range(0,len(route)-1):
		
		coord_1 = route[x]['location']
		coord_2 = route[x+1]['location']

		diff = haversine(coord_1,coord_2)
		if diff > 50: # more than 50 km between the two points
			print "error -- too much distance"
			return -1
		list_distances.append(diff)
					
	return list_distances

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
