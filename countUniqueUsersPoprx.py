import json

with open(input("jsonl file: ")) as file:
	lines = file.readlines()
	events = [json.loads(line) for line in lines]

users = set()

for event in events:
	if event["type"] == "txinit":
		users.add(event["id"])

print(len(users), "unique users")
