import pymongo

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

def getScavengerHuntProgress(collection, since=None):
	if not since == None:
		documents = collection.find({"t": {"$gte": since}})
	else:
		documents = collection.find()

	documents.sort("t")

	shIndexOfClients = dict()

	for document in documents:
		if 'meta' in document and 'sh_2023_code' in document['meta']:
			if document['meta']['sh_2023_code'] in codes:
				index = codes.index(document['meta']['sh_2023_code'])
				if document['track_id'] not in shIndexOfClients and index == (len(codes) -1):
					continue # if they completed the scavenger hunt before the specified "since" period, we do not want to include them in the report
				shIndexOfClients[document['track_id']] = index

	return {
		"shIndexOfClients": shIndexOfClients,
		"totalClues": len(codes),
	}


if __name__ == "__main__":
	conn_str = input("MongoDB connection string: ")

	client = pymongo.MongoClient(conn_str)

	db = client["analytics"]

	print(getScavengerHuntProgress(db["requests"]))
