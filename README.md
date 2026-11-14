# Tricycle Ride Booking REST API (IT31DEVNET)

Mabalacat City College — Institute of Computing Studies (1st Semester, A.Y. 2026-2027)

## Project Files
- `app.py` — Flask REST API Provider (5 endpoints for `/rides`)
- `consumer.py` — Python `requests` Consumer Script with error handling & summary report
- `requirements.txt` — Required Python packages (`flask`, `requests`)

## API Specification

| HTTP Method | Path | Description | Success Code | Failure Code | Sample JSON Response (Success) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GET** | `/rides` | Retrieve a list of all tricycle ride bookings | `200 OK` | `500 Internal Server Error` | `[{"ride_id": 1, "pickup": "McArthur Highway", "dropoff": "Mabalacat City College", "status": "completed"}]` |
| **GET** | `/rides/<int:ride_id>` | Retrieve details of a specific ride by ID | `200 OK` | `404 Not Found` | `{"ride_id": 3, "pickup": "Barangay Hall", "dropoff": "Public Market", "status": "on the way"}` |
| **POST** | `/rides` | Book a new tricycle ride | `201 Created` | `400 Bad Request` | `{"ride_id": 4, "pickup": "7-Eleven Dau", "dropoff": "Bamban Town Plaza", "status": "pending"}` |
| **PUT** | `/rides/<int:ride_id>` | Update the status or details of an existing ride | `200 OK` | `404 Not Found` / `400 Bad Request` | `{"ride_id": 3, "pickup": "Barangay Hall", "dropoff": "Public Market", "status": "completed"}` |
| **DELETE** | `/rides/<int:ride_id>` | Cancel and remove a ride booking by ID | `200 OK` | `404 Not Found` | `{"message": "Ride 3 cancelled successfully"}` |

## How to Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Flask API server (Terminal 1):**
   ```bash
   python app.py
   ```
   The API will run at `http://127.0.0.1:5000`.

3. **Run the Consumer Script (Terminal 2):**
   ```bash
   python consumer.py
   ```
