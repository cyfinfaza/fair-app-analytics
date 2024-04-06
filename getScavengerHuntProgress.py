import pymongo
from pymongo.collection import Collection

# todo: update for 2024
codes = [
	"om3p5j2t",
	"5bb6wme7",
	"2yg2u65x",
	"90y23932",
	"qhpz6ok3",
	"j18pw7ro",
	"60gj3ve5",
	"y09vkc8f",
	"w4rwdh9y",
	"7joqi24d",
	"kxnib0c3",
	"4nwt0k6y",
	"zzx3q0ry",
	"25tu9o28",
	"5o5w7mpg",
	"2qj7zma6"
]
codeMetaKey = "sh_2023_code"

def getScavengerHuntProgress(collection: Collection, since=None):
	filter = {"meta": {codeMetaKey: {"$exists": True}}}
	if not since == None:
		filter["t"] = {"$gte": since}
	documents = collection.find(filter).sort("t")

	shIndexOfClients: dict[str, int] = {}

	# from the start of the day (the "since" period), iterate over every log and keep updating each tracker's status
	for document in documents:
		if 'meta' in document and codeMetaKey in document['meta'] and document['meta'][codeMetaKey] in codes:
			index = codes.index(document['meta'][codeMetaKey])
			if document['track_id'] not in shIndexOfClients and index == (len(codes) - 1):
				# first appearance during the day period and already at the end
				# so don't include them anymore
				continue
			shIndexOfClients[document['track_id']] = index

	# turn each tracker status into the format for the ui
	clientsAtEachIndex: list[list[str]] = [[] for _ in codes]
	for client in shIndexOfClients:
		clientsAtEachIndex[shIndexOfClients[client]].append(client)

	return clientsAtEachIndex