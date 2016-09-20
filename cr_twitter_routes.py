from copy import deepcopy
from config import Mongo, haversine
from datetime import datetime
import json,csv
import traceback
from random import randint
import sys
import lib_route as lb

db = Mongo()
choose_subroute_d = False

def date_filter(posts,d):
    """
    This is for Instagram
    return [x for x in posts if (int(x["created_time"]) >= d and \
    (int(x["created_time"]) <= (d+86400)))]
    for time in t:
            posts2=db.clean_tweets4.find({"user_id": uid,"timestamp_ms": {"$gt": t_start,"$lt":t_end}},{})
            #print posts2
            if(posts2.count()>=4):
                print "more than 4"
    """
    return [x for x in posts if (int(x["timestamp_ms"]))>= d and (int(x["timestamp_ms"]) <= (d+86400))]


def main():

    t_start = datetime.now()
    # get unique twitter user ids
    twitter_user_ids = db.mapped_twitter_ids.distinct("user_id")
    num_twitter_ids = str(len(twitter_user_ids))
    print "There are %s distinct Twitter users" % num_twitter_ids

    user_count = 1
    routes_count = 0
    user_count_mass = 0
    user_routes = {}
    for uid in twitter_user_ids:
        if(user_count%1000==0):
            print user_count
#           break
	user_count+=1
#       print "processing user "+ str(uid) + " : " + str(user_count) + " of " + num_twitter_ids
        # get all posts
	
        posts_cursor = db.clean_tweets4.find({"user_id": uid})
#	print posts.count()
	uid_routes = []
	if posts_cursor.count()>4:
#		if uid ==883159742:
#			print "Posts for 883159742: %s" %posts_cursor.count()
		user_count_mass +=1
#		print "Hello: %s"% user_count_mass
		posts_list =[]
		
		for i in posts_cursor:
			posts_list.append(i)

			
#        	print "Posts Count: %s"% len(posts_list)

		posts_day = []
		i=0
		while i< (len(posts_list)-3):
			curr_post = posts_list[i]
 #          		print "New Route Timestamp: %s" % curr_post['timestamp_ms']
			t_start_route = curr_post['timestamp_ms']
			t_step = 86400 #seconds in a day.
			t_end_route = t_start_route + t_step
			posts_day[:]=[]
			posts_day = [curr_post] #How many points in the day?
			t_temp = posts_list[i+1]['timestamp_ms']
			next_post = posts_list[i+1]
			j=i+2
			
			while (t_temp < t_end_route and j<(len(posts_list)-2)):
				# We can add more posts to the route
				posts_day.append(next_post)
				next_post = posts_list[j]
				t_temp = next_post['timestamp_ms']
				j+=1
			if (len(posts_day)>=5):
#				print "\n\nNEW ROUTE ADDED\n\n!"
				
				db.routes_tw2.insert({"user_id":uid,"numb_user_posts":len(posts_list),"route":[deepcopy(posts_day)]})
				#uid_routes.append(deepcopy(posts_day))
#				print uid_routes
				routes_count+=1
				i=j
			else:
				i+=1
#			print "I'm stuck"
#			print "i: %s" % i
#		print "User %s | Routes: %s Posts: %s" % (curr_post['user_id'],"len(uid_routes)","len(posts_list)")
		#		
#	        print "\n\n\nNEWUSER\n\n"    
#	if len(uid_routes)>0:    	
#		user_routes[uid]=uid_routes
	count = 0
#	for i in user_routes:
#		count += len(user_routes[i])
#	if user_count == 50:
#	print "\n\n\n\completed 500 users\n\n\n"
#		for i in user_routes:
#			get_size_of_routes = []
#			for j in range(len(user_routes[i])):
			
#				get_size_of_routes.append(len(user_routes[i][j]))
#			print "User %s | Routes: %s %s" % (i,len(user_routes[i]),get_size_of_routes)
#		break
main()
