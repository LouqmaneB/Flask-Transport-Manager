import os
import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-default')

def convert_obj(obj):
  if isinstance(obj, list):
    return [convert_obj(item) for item in obj]
  elif isinstance(obj, dict):
    return {k: convert_obj(v) for k, v in obj.items()}
  elif isinstance(obj, ObjectId):
    return str(obj)
  elif isinstance(obj, datetime.datetime):
    return obj.isoformat()
  return obj

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'transport-manager')

try:
  client = MongoClient(MONGO_URI)
  db = client[MONGO_DB_NAME]
  routes_collection = db["routes"]
  stops_collection = db["stops"]
  print("MongoDB connected successfully!")
except Exception as e:
  print(f"MongoDB connection failed: {e}")
  raise e

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/save_route", methods=["POST"])
def save_route():
  data = request.json
  route_name = data.get("name")
  points = data.get("points")

  if route_name and points:
    try:
      formatted_stops = [
        {
          "stop_id": ObjectId(stop["stop_id"]),
          "order": stop["order"]
        }
        for stop in points
      ]

      routes_collection.insert_one({
        "route_name": route_name,
        "short_name": data.get("short_name", ""),
        "description": data.get("description", ""),
        "route_color": data.get("route_color", "#10b981"),
        "frequency_minutes": data.get("frequency_minutes", 30),
        "first_departure": data.get("first_departure", "06:00 AM"),
        "last_departure": data.get("last_departure", "10:00 PM"),
        "points": formatted_stops,
        "created_at": datetime.datetime.utcnow(),
      })

      return jsonify({"message": "Route saved"}), 200
    except Exception as e:
      return jsonify({"error": str(e)}), 500
  return jsonify({"error": "Missing data"}), 400

@app.route('/get_routes')
def get_routes():
  routes = list(db.routes.find())
  
  for route in routes:
    for point in route.get("points", []):
      stop = db.stops.find_one({"_id": point["stop_id"]})
      if stop:
        point["stop_details"] = {
          "stop_name": stop.get("stop_name", ""),
          "location": stop.get("location", {}),
          "description": stop.get("description", ""),
          "facilities": stop.get("facilities", {}),
        }
      point["stop_id"] = str(point["stop_id"])        
    route["_id"] = str(route["_id"])
  
  return jsonify(routes)

@app.route("/get_route/<route_id>")
def get_route(route_id):
  route = routes_collection.find_one({"_id": ObjectId(route_id)})
  if not route:
    return jsonify({"error": "Route not found"}), 404

  route["_id"] = str(route["_id"])
  for point in route.get("points", []):
    stop = stops_collection.find_one({"_id": point["stop_id"]})
    if stop:
      point["stop_details"] = {
        "stop_name": stop.get("stop_name", ""),
        "location": stop.get("location", {}),
        "description": stop.get("description", ""),
        "facilities": stop.get("facilities", {}),
      }
    point["stop_id"] = str(point["stop_id"])

  return jsonify(route), 200

@app.route("/update_route/<route_id>", methods=["POST"])
def update_route(route_id):
  data = request.json
  points = data.get("points")
  if points:
    routes_collection.update_one({"_id": ObjectId(route_id)}, {"$set": {"points": points}})
    return jsonify({"status": "updated"}), 200
  return jsonify({"status": "error"}), 400

@app.route("/delete_route/<route_id>", methods=["DELETE"])
def delete_route(route_id):
  routes_collection.delete_one({"_id": ObjectId(route_id)})
  return jsonify({"status": "deleted"}), 200

@app.route("/stops")
def stop_manager():
  return render_template("stops.html")

@app.route("/add_stop", methods=["POST"])
def add_stop():
  data = request.json
  name = data.get("name")
  location = data.get("location")
  if name and location:
    stops_collection.insert_one({
      "stop_name": name,
      "stop_code": data.get("stop_code", ""),
      "location": {
        "type": "Point",
        "coordinates": location
      },
      "address": data.get("address", ""),
      "description": data.get("description", ""),
      "facilities": {
        "shelter": data.get("shelter", False),
        "bench": data.get("bench", False),
        "lighting": data.get("lighting", False),
        "wheelchair_accessible": data.get("wheelchair_accessible", False),
        "real_time_display": data.get("real_time_display", False)
      },
      "stop_code": data.get("stop_code", ""),
      "created_at": datetime.datetime.now()
    })
    return jsonify({"status": "success"}), 200
  return jsonify({"status": "error"}), 400

@app.route("/get_stops", methods=["GET"])
def get_stops():
  stops = list(stops_collection.find().limit(500))
  for stop in stops:
    stop["_id"] = str(stop["_id"])
  return jsonify(stops), 200

@app.route("/update_stop/<stop_id>", methods=["POST"])
def update_stop(stop_id):
  data = request.json
  name = data.get("stop_name")
  location = data.get("location")
  if name and location:
    stops_collection.update_one({"_id": ObjectId(stop_id)}, {"$set": {"stop_name": name, "location": location}})
    return jsonify({"status": "updated"}), 200
  return jsonify({"status": "error"}), 400

@app.route("/delete_stop/<stop_id>", methods=["DELETE"])
def delete_stop(stop_id):
  stops_collection.delete_one({"_id": ObjectId(stop_id)})
  return jsonify({"status": "deleted"}), 200

if __name__ == "__main__":
  debug_mode = os.getenv('FLASK_ENV') == 'development'
  
  app.run(
    debug=debug_mode,
    host=os.getenv('FLASK_HOST', '127.0.0.1'),
    port=int(os.getenv('FLASK_PORT', 5000))
  )