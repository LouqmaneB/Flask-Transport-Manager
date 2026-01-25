import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, Blueprint, abort
import requests

load_dotenv()

app = Flask(__name__)


from flask import request, abort

def get_admin_token():
  token = request.headers.get("X-Admin-Token")

  if not token:
    token = request.cookies.get("admin_token")

  if not token:
    abort(401, description="Admin token missing")

  return {"Authorization": f"Bearer {token}"}

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-default')
admin_bp = Blueprint("admin", __name__, url_prefix="/admin_api")

@admin_bp.route("/itineraire")
def index():
  return render_template("index.html")

@admin_bp.route("/save_route", methods=["POST"])
def save_route():
  data = request.json
  route_name = data.get("name")
  points = data.get("points") #[{id,order}]

  if route_name and points:
    try:
      response = requests.post(
        f"{os.getenv('EXPRESS_URI')}/api/routes", 
        json={"routeName":route_name, "stops": points},
        headers=get_admin_token()
      )
      response.raise_for_status()
      res = response.json()

    except requests.exceptions.RequestException as e:
      return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify(res), 201
  return jsonify({"status": "error", "message": "route name and (lat, lng) are required"}), 400

@admin_bp.route('/get_routes')
def get_routes():
  try:
    response = requests.get(f"{os.getenv('EXPRESS_URI')}/api/routes")
    response.raise_for_status()
    routes = response.json()
  except requests.exceptions.RequestException as e:
    return jsonify({"status": "error", "message": str(e)}), 500
  return jsonify(routes), 200

@admin_bp.route("/get_route/<route_id>")
def get_route(route_id):
  try:
    response = requests.get(f"{os.getenv('EXPRESS_URI')}/api/routes/{route_id}")
    response.raise_for_status()
    route = response.json()
  except requests.exceptions.RequestException as e:
    return jsonify({"status": "error", "message": str(e)}), 500
  return jsonify(route), 200

@admin_bp.route("/update_route/<route_id>", methods=["POST"])
def update_route(route_id):
  data = request.json
  payload = data.get("stops")
  payload = {
    "stops": payload  # Wrap the array in a 'stops' key
  }
  if payload:
    try:
      response = requests.put(f"{os.getenv('EXPRESS_URI')}/api/routes/{route_id}",json=payload,headers=get_admin_token())
      response.raise_for_status()
      route = response.json()
    except requests.exceptions.RequestException as e:
      return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify(route), 200
  return jsonify({"status": "error", "data": payload}), 400

@admin_bp.route("/delete_route/<route_id>", methods=["DELETE"])
def delete_route(route_id):
  try:
    response = requests.delete(f"{os.getenv('EXPRESS_URI')}/api/routes/{route_id}",headers=get_admin_token())
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    return jsonify({"status": "error", "message": str(e)}), 500
  return jsonify("deleted"), 200


@admin_bp.route("/stops")
def stop_manager():
  return render_template("stops.html")

@admin_bp.route("/add_stop", methods=["POST"])
def add_stop():
  data = request.json
  name = data.get("name")
  location = data.get("location")

  payload = {
  "stop_name": name,
  "latitude": location[1],
  "longitude": location[0]
  }

  try:
    response = requests.post(
      f"{os.getenv('EXPRESS_URI')}/api/stops",
      json=payload,
      headers=get_admin_token(),
      timeout=5
    )
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    return jsonify({"status": "error", "message": str(e)}), 500

  return jsonify(response.json()), 201

@admin_bp.route("/get_stops", methods=["GET"])
def get_stops():
  try:
    response = requests.get(f"{os.getenv('EXPRESS_URI')}/api/stops")
    response.raise_for_status()
    stops = response.json()
    # for stop in stops:
    #   if "id" in stop:
    #     stop["id"] = str(stop["id"])  
  except requests.exceptions.RequestException as e:
    return jsonify({"status": "error", "message": str(e)}), 500
  return jsonify(stops), 200

@admin_bp.route("/update_stop/<stop_id>", methods=["POST"])
def update_stop(stop_id):
  data = request.json
  name = data.get("stop_name")
  location = data.get("location")
  if name and location:
    try:
      response = requests.put(f"{os.getenv('EXPRESS_URI')}/api/stops/{stop_id}",json={"name":name,"location": location},headers=get_admin_token())
      response.raise_for_status()
      data = response.json()
    except requests.exceptions.RequestException as e:
      return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify(data), 200

@admin_bp.route("/delete_stop/<stop_id>", methods=["DELETE"])
def delete_stop(stop_id):
  try:
    response = requests.delete(f"{os.getenv('EXPRESS_URI')}/api/stops/{stop_id}",headers=get_admin_token())
    response.raise_for_status()
    data = response.json()
  except requests.exceptions.RequestException as e:
    return jsonify({"status": "error", "message": str(e)}), 500
  return jsonify(data), 200

app.register_blueprint(admin_bp)

if __name__ == "__main__":
  debug_mode = os.getenv('FLASK_ENV') == 'development'
  
  app.run(
    debug=debug_mode,
    host=os.getenv('FLASK_HOST', '127.0.0.1'),
    port=int(os.getenv('FLASK_PORT', 5000))
  )