import pymongo
from pymongo.collection import Collection

# todo: update for 2024
codes = [
	"ka1ho9h0",
	"qjdjfjbd",
	"brjx21ms",
	"i38sbr6x",
	"6k9yggkf",
	"ro1khj99",
	"d35eb1af",
	"sip1mvmn",
	"dtijjfy0",
	"f1vrzfhx",
	"e0oalvvq",
	"5f9lnsp9",
	"qsnqda7b",
	"6i936v1s",
	"zakfvnsm",
	"zd1wjidv",
	"7xwm9rm9",
	"l9rgq8li",
	"52twfi84",
	"k9i8e6sd",
	"f1vytlmj",
]
codeMetaKey = "sh_2024_code"

def getScavengerHuntProgress(collection: Collection, since=None):
	filter = {f"meta.{codeMetaKey}": {"$exists": True}}
	if not since == None:
		filter["t"] = {"$gte": since}
	documents = collection.find(filter, projection={"_id": False, "track_id": True, f"meta.{codeMetaKey}": True}).sort("t")

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