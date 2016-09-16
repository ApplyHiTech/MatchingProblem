# Collects Instagram Data 
# Written by Rohit Jain

from math import radians, cos, sin, asin, sqrt
from instagram.client import InstagramAPI
import sys, csv, datetime, time
from config import Mongo

def insert(item,db_name):
    try:
        db_name.insert(item)
    except Exception as inst:
        print "========EXCEPTION============"
        print inst
        pass

def write_csv(stmt):
    f = open("tracked_users.csv","a")
    stmt = str(stmt) + ","
    f.write(stmt)
    f.close()

def search(api, dist, start_lat, start_lng, mint, maxt, store):
    time.sleep(0.2)
    db = Mongo()
    last_time = 0
    n_responses=0
    print "Searching"
    for mention in api.media_search(distance=dist,return_json=True,lat=start_lat,lng=start_lng, min_timestamp=mint, max_timestamp=maxt,count=200):
        n_responses+=1
        user = mention["user"]
        last_time = mention["created_time"]
        username = mention["user"]["username"]
        write_csv(mention["user"]["id"])
        insert(user,db.insta_users)
        insert(mention,db.instas)
    print n_responses
    return last_time

def main():
    #writer = csv.writer(file(sys.argv[1], 'wb'), delimiter = '\t')
    trip_start_time  = 1456012800 #02-21-2016 00:00:00
    trip_stop_time = 1460246400 #04-10-2016 00:00:00
    region1_lat = 40.745280
    region1_lon = -73.987071
    cid = ["bd255b8336d64b3181df031968e0a81f","7862b38e6f5b469683ae50ea330db922","a4087ec4b5714b55ad71812572abc522","1ebf920d77ba40aa930736472cad382b","082accf5aa1e4653bde2c595b57f38c0"]
    api = InstagramAPI(client_id = cid[0])
    store = {}
    last_time = trip_stop_time
    print "starting"
    search_count=0
    i=0
    while trip_start_time < trip_stop_time:
        try:
            temp_trip_stop_time = search(api, 7000, region1_lat, region1_lon, trip_start_time, trip_stop_time, store)
            search_count+=1
            if(search_count%50 == 0):
                i= (i+1)%5
                api = InstagramAPI(client_id = cid[i])
                print "switched"
            print "search " + str(search_count)
            print "Time returned from search"
            print datetime.datetime.utcfromtimestamp(int(temp_trip_stop_time))
            print "Time sent to api"
            print datetime.datetime.utcfromtimestamp(int(trip_stop_time))
            temp_trip_stop_time = int(temp_trip_stop_time)
            trip_stop_time = int(trip_stop_time)
            #print int(temp_trip_stop_time) >= int(trip_stop_time)
            if temp_trip_stop_time >= trip_stop_time:
                trip_stop_time = int(trip_stop_time) - 1
                print "change time"
                print datetime.datetime.utcfromtimestamp(int(trip_stop_time))
            else:
                trip_stop_time = temp_trip_stop_time
        except Exception as e:
            print "Exception"
            print e
            #break

main()
