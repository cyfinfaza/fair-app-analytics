from json import load
from flask import Flask, request, Response
import pymongo
from dotenv import load_dotenv
import os
import json
import certifi
from countUniqueUsersPvt import countUniqueUsers
from countPlatformsPvt import countPlatforms

load_dotenv()
app = Flask(__name__)

MONGODB_CONN_STR = os.environ["MONGODB_CONN_STR"]

client = pymongo.MongoClient(MONGODB_CONN_STR, tlsCAFile=certifi.where())
db = client["analytics"]


def success_json(data):
    return Response(json.dumps({"type": "success", "data": data}), mimetype="application/json")


@app.route('/')
def index():
    return "hi"


@app.route('/api/uniqueUsersPvt')
def uniqueUsersPvt():
    try:
        sinceHoursAgo = int(request.args.get("sinceHoursAgo"))
    except:
        sinceHoursAgo = None
    return success_json(str(countUniqueUsers(db["requests"], sinceHoursAgo)))


@app.route("/api/platformsPvt")
def platformsPvt():
    return success_json(countPlatforms(db["sessions"]))


if __name__ == "__main__":
    app.run(debug=True)
