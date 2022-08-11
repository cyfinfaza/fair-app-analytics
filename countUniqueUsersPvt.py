import pymongo
import time
import datetime

conn_str = input("MongoDB connection string: ")

client = pymongo.MongoClient(conn_str)

db = client["analytics"]
collection = db["requests"]

# fetch documents from past 24 hours
start = datetime.datetime.utcnow() - datetime.timedelta(days=1)
end = datetime.datetime.utcnow()
documents = collection.find({"t": {"$gte": start, "$lt": end}})

ids = set()

for document in documents:
    ids.add(document["track_id"])

print(len(ids), "unique users")
