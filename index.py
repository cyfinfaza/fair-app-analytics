from flask import Flask, request, Response, render_template
from flask_cors import CORS
import pymongo
from dotenv import load_dotenv
import os
import json
import certifi
import datetime
from countUniqueUsersPvt import countUniqueUsers
from countPlatformsPvt import countPlatforms

load_dotenv()
app = Flask(__name__)
CORS(app)

MONGODB_CONN_STR = os.environ["MONGODB_CONN_STR"]

client = pymongo.MongoClient(MONGODB_CONN_STR, tlsCAFile=certifi.where())
db = client["analytics"]

def success_json(data):
	return Response(json.dumps({"type": "success", "data": data}, indent="\t"), mimetype="application/json")

@app.route('/')
def index():
	return render_template('index.html', year=datetime.date.today().year)

# ensures since is valid
@app.before_request
def since_middleware():
	since = None
	try:
		if 'since' in request.args:
			since = datetime.datetime.fromisoformat(request.args['since'])
		elif 'sinceHoursAgo' in request.args:
			since = datetime.datetime.utcnow() - datetime.timedelta(hours=float(request.args['sinceHoursAgo']))
	except:
		since = None
	request.environ['since'] = since

@app.route('/api/uniqueUsersPvt')
def uniqueUsersPvt():
	return success_json(countUniqueUsers(db["requests"], request.environ['since']))

@app.route("/api/platformsPvt")
def platformsPvt():
	return success_json(countPlatforms(db["sessions"]))

if __name__ == "__main__":
	app.run(debug=True)
