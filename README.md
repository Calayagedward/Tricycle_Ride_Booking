TRICYCLE RIDE BOOKING API

Files:
- app.py: Flask provider API with five endpoints.
- consumer.py: Example Python requests consumer for testing this API.
- sample_requests.json: Example JSON request bodies.
- requirements.txt: Required Python packages.

Setup:
1. Open a terminal in this folder.
2. Install dependencies: pip install -r requirements.txt
3. Start the API: python app.py
4. Open another terminal in this folder.
5. Run the consumer: python consumer.py

API base URL: http://127.0.0.1:5000

Endpoints:
POST   /rides
GET    /rides
GET    /rides/<ride_id>
PUT    /rides/<ride_id>
PATCH  /rides/<ride_id>/status

Note:
Data is stored in memory using a Python list. It resets whenever the
Flask application restarts. The consumer.py file is a local testing
example; for the class deliverable, adjust it to call your partner
group's approved API specification.
