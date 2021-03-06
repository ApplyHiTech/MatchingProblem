# The following script computes the
# a. Number of routes in the Twitter database.
# b. Number of Routes per user
# c. a Historgram of the Number of users with N number of routes per user. 
# d. The script saves the histogram data in csv format. 



from config import Mongo
import csv
import pandas as pd

db=Mongo()

n= db.instas.count()

def main():
	twitter_route_analysis()

def twitter_route_analysis():
	#compute the number of routes in the twitter database.
	x = db.routes_tw2.find().count()
	
	print "There are %s number of Twitter Routes" % x
	
	#Routes per User Data
	x1 = db.routes_tw2.aggregate(
		[
			{"$group": {"_id":"$user_id", "count": {"$sum":1}}},
			{"$sort": {"count":1}}

		]
	)
	print "Number of users: %s" % len(x1['result'])
	
	#Histogram
	x2 = db.routes_tw2.aggregate(
		[
			{"$group": {"_id":"$user_id", "count":{"$sum":1}}},
			{"$group": {"_id": "$count","User_count":{"$sum":1}}},
			{"$sort": {"User_count":1}}
		]
	)
	x3 = x2['result']	
	print type(x3),type(x3[0])
	print pd.DataFrame(x3)

	pd.DataFrame(x3).to_csv("twitter_route_histogram.csv",index_label=False)
main()

