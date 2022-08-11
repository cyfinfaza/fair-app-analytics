import pymongo
from user_agents import parse

conn_str = input("MongoDB connection string: ")

client = pymongo.MongoClient(conn_str)

db = client["analytics"]
collection = db["sessions"]

agents = {}

documents = collection.find()
for document in documents:
    if document["agent"] in agents:
        agents[document["agent"]] += 1
    else:
        agents[document["agent"]] = 1

platforms = {}

for agent in agents:
    platform = parse(agent).os.family
    if platform in platforms:
        platforms[platform] += agents[agent]
    else:
        platforms[platform] = agents[agent]

print(platforms)
