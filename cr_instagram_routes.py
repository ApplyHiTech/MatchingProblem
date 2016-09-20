from copy import deepcopy
from config import Mongo, haversine
from datetime import datetime
import json,csv
import traceback
from random import randint
import sys
db = Mongo()

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
    user_count_mass = 0
    user_routes = {}
    for uid in instagram_user_ids:
        if(user_count%1000==0):
            print "Break For Loop users: %s " % user_count
	    
	user_count+=1
	posts_cursor = db.clean_instagram_posts.find({"user_id":uid}).sort("created_time")
#	print "The user: %s has %s posts" % (uid,posts_cursor.count())

	uid_routes =[]

	if posts_cursor.count()>=5: #There are at leats 5 posts by the user...compute routes
		user_count_mass+=1
		
		#Get Routes
		posts_list =[]
		
		for i in posts_cursor:
			posts_list.append(i)
		
		posts_day = []
		i=0 
		while i < (len(posts_list)-3):
			curr_post = posts_list[i]
			t_start_route=curr_post['created_time']
			t_step = 86400
			t_end_route = t_start_route+t_step
			posts_day[:]=[]
			posts_day=[curr_post]
			t_temp = posts_list[i+1]['created_time']
			next_post = posts_list[i+1]
			j=i+2
			
			while ( t_temp < t_end_route and j<(len(posts_list)-2)):
				posts_day.append(next_post)
				next_post = posts_list[j]
				t_temp = next_post['created_time']
				j+=1
			if (len(posts_day)>=5):
#				print "new route"
				
				route_features = compute_features(deepcopy(posts_day))
#				print "Works %s" % route_features
#				db.routes_ig.insert({"user_id":uid,"numb_user_posts":len(posts_list),"route":[deepcopy(posts_day)]})

				routes_count+=1
				i=j
			else:
				i+=1

    print "the number of eligible users: %s " % user_count_mass
    print "there are %s routes" % routes_count		

def compute_features(route):
#	print "Yes. It works"
	time = compute_time(route)
	distance = compute_distance(route)
	return {"Length_time": time, "Length Distance": distance}

def compute_time(route):
	list_times = []
	for x in route:
		temp_time = x['created_time']
		list_times.append(temp_time)
	
	start = min(list_times)

	end = max(list_times)
	length = end-start
	if length > 86400:
		print "error --- more than a day"

	return {"length": length, "start": start, "end": end}

def compute_distance(route):
	return 1.5
	

main()
