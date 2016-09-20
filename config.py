from flask import Flask,request
from bson import json_util
from datetime import tzinfo, timedelta, datetime
from pytz import timezone
from instagram.client import InstagramAPI
import json,urllib2,pymongo,calendar
from math import radians, cos, sin, asin, sqrt

#TAG = 'food'
class Location:
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.radius = 0.0
    def radius_km(self):
        return self.radius/(1000)

#This class refers to #New York City, NY USA
class NYC(Location):
    def __init__(self):
        self.latitude = 40.745280
        self.longitude = -73.987071
        self.radius = 7000

class TimePeriod:
    def __init__(self):
    	start= 1456012800 # 20 feb, 2016
    	end= 1460246400 # 10 april, 2016

class CityBeatMongo:
    def __init__(self):
        self.conn = pymongo.Connection('ec2-23-20-249-108.compute-1.amazonaws.com',27018)
        self.db = self.conn['citybeat_production']
        self.tweets = self.db['tweets']

class Mongo:
  def __init__(self):
        self.conn = pymongo.Connection('ec2-23-20-249-108.compute-1.amazonaws.com',27020)
        self.db = self.conn['sampled_tourist']
	#Instagram posts
        self.instas = self.db['instas']
        #Twitter posts
	self.tweets = self.db['tweets']
        #Instagram users
	self.insta_users = self.db['users']
        
	self.clean_tweets = self.db['clean_tweets'] 
        self.clean_twitter_user_ids = self.db['clean_twitter_user_ids']
        self.clean_instagram_posts = self.db['clean_instagram_posts_2']
        self.clean_insta_users = self.db['clean_insta_user']
        self.user_tweets = self.db['mapped_user_tweets']
        self.clean_tweets2 = self.db['clean_tweets2']
        self.clean_tweets3 = self.db['clean_tweets3'] #This is new sanitized tweets for calculating routes
	self.clean_tweets4 = self.db['clean_tweets4']
        self.mapped_ids = self.db['mapped_ids']
        self.mapped_ids_3 = self.db['mapped_ids_3']
        self.mapped_ids_4 = self.db['mapped_ids_4']
        self.mapped_twitter_ids = self.db['mapped_twitter_ids']
        self.mapped_instagram_ids = self.db['mapped_instagram_ids']
        self.mapped_id_new = self.db['mapped_id_new']
	self.routes_tw = self.db["routes_tw"]
        self.routes_tw2 = self.db["routes_tw2"] #This is for >=5 posts in a route
	self.routes_ig = self.db["routes_ig"] #this is for >=5 posts in a route ig.
	self.routes = self.db["instagram_routes"]
        self.ig_train = self.db["instagram_train_routes"]
        self.ig_test = self.db["instagram_test_routes"]

#Haversine is a distance measure for 2 geolocation.
def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km
