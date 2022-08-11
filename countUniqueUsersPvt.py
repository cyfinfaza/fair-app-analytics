import pymongo
import time
import datetime


def countUniqueUsers(collection, since):
    # fetch documents from past 24 hours
    if not since == None:
        documents = collection.find({"t": {"$gte": since}})
    else:
        documents = collection.find()

    ids = set()

    for document in documents:
        ids.add(document["track_id"])
    return len(ids)


if __name__ == "__main__":
    conn_str = input("MongoDB connection string: ")

    client = pymongo.MongoClient(conn_str)

    db = client["analytics"]

    print(countUniqueUsers(db["requests"]), "unique users")
