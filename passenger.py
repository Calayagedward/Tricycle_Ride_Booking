import requests

# Change this URL if your API is hosted on another computer/server.
BASE_URL = "http://127.0.0.1:5000"

# Example booking data.
new_booking = {
    "passenger_name": "Juan Dela Cruz",
    "pickup_location": "Mabalacat City College",
    "destination": "Dau Terminal",
    "passengers": 2
}


def show_result(title, response):
    print(f"\n--- {title} ---")
    print("Status code:", response.status_code)

    try:
        print("Response:", response.json())
    except ValueError:
        print("The server did not return JSON.")


def main():
    try:
        #Create a booking.
        response = requests.post(
            f"{BASE_URL}/rides",
            json=new_booking,
            timeout=5
        )
        show_result("CREATE RIDE", response)

        if response.status_code != 201:
            print("Booking was not created. Stopping the test.")
            return

        ride_id = response.json()["ride"]["ride_id"]

        #Retrieve all bookings.
        response = requests.get(f"{BASE_URL}/rides", timeout=5)
        show_result("GET ALL RIDES", response)

        #Retrieve one booking.
        response = requests.get(
            f"{BASE_URL}/rides/{ride_id}",
            timeout=5
        )
        show_result("GET ONE RIDE", response)

        #Update the booking.
        updated_booking = {
            "passenger_name": "Juan Dela Cruz",
            "pickup_location": "Mabalacat City College",
            "destination": "SM City Clark",
            "passengers": 3
        }
        response = requests.put(
            f"{BASE_URL}/rides/{ride_id}",
            json=updated_booking,
            timeout=5
        )
        show_result("UPDATE RIDE", response)

        #Update its status.
        response = requests.patch(
            f"{BASE_URL}/rides/{ride_id}/status",
            json={"status": "accepted"},
            timeout=5
        )
        show_result("UPDATE RIDE STATUS", response)

        #Demonstrate handling an error response (booking ID does not exist).
        response = requests.get(
            f"{BASE_URL}/rides/99999",
            timeout=5
        )
        show_result("ERROR HANDLING TEST", response)

        if response.status_code == 404:
            print("Handled expected error: ride booking was not found.")
        else:
            print("Unexpected response for the error-handling test.")

        print("\nSummary: The consumer attempted all five API endpoints.")

    except requests.exceptions.ConnectionError:
        print("Connection error: Make sure the Flask API is running.")

    except requests.exceptions.Timeout:
        print("Request timed out. Try again.")

    except requests.exceptions.RequestException as error:
        print("Request error:", error)


if __name__ == "__main__":
    main()
