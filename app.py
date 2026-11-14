from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
rides = [
    {"ride_id": 1, "pickup": "McArthur Highway", "dropoff": "Mabalacat City College", "status": "completed"},
    {"ride_id": 2, "pickup": "Dau Bus Terminal", "dropoff": "Xevera Mabalacat", "status": "pending"},
    {"ride_id": 3, "pickup": "Barangay Hall", "dropoff": "Public Market", "status": "on the way"}
]

# 0. Home route (so visiting the base URL doesn't give a 404 anymore!)
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Tricycle Ride Booking API!",
        "available_endpoints": [
            "GET /rides",
            "GET /rides/<ride_id>",
            "POST /rides",
            "PUT /rides/<ride_id>",
            "DELETE /rides/<ride_id>"
        ]
    }), 200

# 1. GET all rides
@app.route("/rides", methods=["GET"])
def get_all_rides():
    return jsonify(rides), 200

# 2. GET a single ride by ID
@app.route("/rides/<int:ride_id>", methods=["GET"])
def get_ride(ride_id):
    ride = next((r for r in rides if r["ride_id"] == ride_id), None)
    if not ride:
        return jsonify({"error": f"Ride {ride_id} not found"}), 404
    return jsonify(ride), 200

# 3. POST a new ride booking
@app.route("/rides", methods=["POST"])
def create_ride():
    data = request.get_json()
    if not data or "pickup" not in data or "dropoff" not in data:
        return jsonify({"error": "Both 'pickup' and 'dropoff' fields are required"}), 400

    new_id = max((r["ride_id"] for r in rides), default=0) + 1
    new_ride = {
        "ride_id": new_id,
        "pickup": data["pickup"],
        "dropoff": data["dropoff"],
        "status": data.get("status", "pending")
    }
    rides.append(new_ride)
    return jsonify(new_ride), 201

# 4. PUT (update) a ride's status or details
@app.route("/rides/<int:ride_id>", methods=["PUT"])
def update_ride(ride_id):
    ride = next((r for r in rides if r["ride_id"] == ride_id), None)
    if not ride:
        return jsonify({"error": f"Ride {ride_id} not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    if "pickup" in data:
        ride["pickup"] = data["pickup"]
    if "dropoff" in data:
        ride["dropoff"] = data["dropoff"]
    if "status" in data:
        ride["status"] = data["status"]

    return jsonify(ride), 200

# 5. DELETE (cancel) a ride
@app.route("/rides/<int:ride_id>", methods=["DELETE"])
def delete_ride(ride_id):
    global rides
    ride = next((r for r in rides if r["ride_id"] == ride_id), None)
    if not ride:
        return jsonify({"error": f"Ride {ride_id} not found"}), 404

    rides = [r for r in rides if r["ride_id"] != ride_id]
    return jsonify({"message": f"Ride {ride_id} cancelled successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)