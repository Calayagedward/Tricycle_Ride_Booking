from flask import Flask, request, jsonify

app = Flask(__name__)

rides = []
next_ride_id = 1

ALLOWED_STATUSES = ["pending", "accepted", "ongoing", "completed", "cancelled"]


def find_ride(ride_id):
    """Find and return a ride using its ID."""
    for ride in rides:
        if ride["ride_id"] == ride_id:
            return ride
    return None


def validate_ride_data(data):
    """Check whether all required booking details are valid."""
    required_fields = [
        "passenger_name",
        "pickup_location",
        "destination",
        "passengers"
    ]

    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"

    if not isinstance(data["passenger_name"], str) or not data["passenger_name"].strip():
        return "passenger_name must be a non-empty string."

    if not isinstance(data["pickup_location"], str) or not data["pickup_location"].strip():
        return "pickup_location must be a non-empty string."

    if not isinstance(data["destination"], str) or not data["destination"].strip():
        return "destination must be a non-empty string."

    # bool is a subclass of int in Python, so reject it explicitly.
    if isinstance(data["passengers"], bool) or not isinstance(data["passengers"], int):
        return "passengers must be a whole number."

    if data["passengers"] < 1:
        return "passengers must be at least 1."

    return None


#Create a new ride booking.
@app.route("/rides", methods=["POST"])
def create_ride():
    global next_ride_id

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required."}), 400

    error = validate_ride_data(data)
    if error:
        return jsonify({"error": error}), 400

    new_ride = {
        "ride_id": next_ride_id,
        "passenger_name": data["passenger_name"].strip(),
        "pickup_location": data["pickup_location"].strip(),
        "destination": data["destination"].strip(),
        "passengers": data["passengers"],
        "status": "pending"
    }

    rides.append(new_ride)
    next_ride_id += 1

    return jsonify({
        "message": "Ride booking created successfully.",
        "ride": new_ride
    }), 201


#Retrieve all ride bookings.
@app.route("/rides", methods=["GET"])
def get_all_rides():
    return jsonify({"rides": rides}), 200


#Retrieve one ride booking by its ID.
@app.route("/rides/<int:ride_id>", methods=["GET"])
def get_ride(ride_id):
    ride = find_ride(ride_id)

    if ride is None:
        return jsonify({"error": "Ride booking not found."}), 404

    return jsonify(ride), 200


#Update all editable details of an existing booking.
@app.route("/rides/<int:ride_id>", methods=["PUT"])
def update_ride(ride_id):
    ride = find_ride(ride_id)

    if ride is None:
        return jsonify({"error": "Ride booking not found."}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required."}), 400

    error = validate_ride_data(data)
    if error:
        return jsonify({"error": error}), 400

    ride["passenger_name"] = data["passenger_name"].strip()
    ride["pickup_location"] = data["pickup_location"].strip()
    ride["destination"] = data["destination"].strip()
    ride["passengers"] = data["passengers"]

    return jsonify({
        "message": "Ride booking updated successfully.",
        "ride": ride
    }), 200


#Update the status of an existing booking.
@app.route("/rides/<int:ride_id>/status", methods=["PATCH"])
def update_ride_status(ride_id):
    ride = find_ride(ride_id)

    if ride is None:
        return jsonify({"error": "Ride booking not found."}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required."}), 400

    new_status = data.get("status")

    if new_status not in ALLOWED_STATUSES:
        return jsonify({
            "error": "Invalid status.",
            "allowed_statuses": ALLOWED_STATUSES
        }), 400

    ride["status"] = new_status

    return jsonify({
        "message": "Ride status updated successfully.",
        "ride": ride
    }), 200


if __name__ == "__main__":
    # Run the API locally at http://127.0.0.1:5000
    app.run(debug=True)
