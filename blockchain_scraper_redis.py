
import requests
from bs4 import BeautifulSoup
import pymongo as mongo
import redis
import json
import time


def clean_data(rawdata):
    rawdata = rawdata.replace("Hash","")
    rawdata = rawdata.replace("Time"," ")
    rawdata = rawdata.replace("Amount","")
    rawdata = rawdata.replace("(BTC)","")
    rawdata = rawdata.replace("BTC","")
    rawdata = rawdata.replace(" (USD)","")
       
    return rawdata

myclient = mongo.MongoClient("mongodb://localhost:27017")
hash_db = myclient["hashes"]
col_hashes = hash_db["hashes"]
url = "https://www.blockchain.com/btc/unconfirmed-transactions"

lijst = []
highest = 0
tijd= ""
highest_btc = 0

r = redis.Redis ()
r.flushall() 

while True:
    request = requests.get(url)
    soupbs = BeautifulSoup(request.text, "html.parser")
    texts = soupbs.find_all("div", {"class" : "sc-1g6z4xm-0 hXyplo"})

    for t in texts:
        text = t.get_text()
        text = clean_data(text)
        text = text.split(" ")
        lijst.append(text)
        
    lijst.reverse()

    if len(tijd) == 0:
            tijd = text[1]  
    for l in lijst:    
        if l[1] == tijd:  
            x = {"Hash": l[0], "Time": l[1], "BTC_value" : float(l[2]), "USD_value": l[3]}
            
            if float(x["BTC_value"]) > float(highest_btc):
                res = r.lpush("time",str(x))
                highest_btc = x["BTC_value"]
            elif float(x["BTC_value"]) < float(highest_btc):
                res = r.rpush("time",str(x))       
                 
        if l[1] > tijd: 
            first = (r.lindex("time",0).decode('utf-8')).replace("\'","\"")
            r.flushall()
            di = json.loads(first)
            myhash = di
            x = col_hashes.insert_one(myhash)
            print(x.inserted_id)
            tijd = l[1]
            lijst = []
            myhash = {}
            highest_btc = 0 
            
            
                    







 


