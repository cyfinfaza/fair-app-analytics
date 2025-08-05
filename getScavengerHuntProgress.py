from pymongo.collection import Collection

# todo: make dynamic yearly (with centralized codes)
codes = [
	"e0oalvvq",	
	"qjdjfjbd",	
	"k9i8e6sd",	
	"d35eb1af",	
	"0rxlk3z1",	
	"1gaeqwkv",	
	"f1vytlmj",	
	"zakfvnsm",	
	"6k9yggkf",	
	"ozy1huwg",	
	"z20b80td",	
	"ro1khj99",	
	"2try64a7",	
	"7xwm9rm9",	
	"ka1ho9h0"
]
codeMetaKey = "sh_2025_code"

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