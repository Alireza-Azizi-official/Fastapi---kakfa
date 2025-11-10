**FastAPI Kafka Microservice**

A FastAPI-based microservice integrating Kafka, MongoDB, and aiokafka for real-time event streaming, with JWT authentication and CRUD operations for cameras.

## Features

FastAPI for building REST APIs.

MongoDB as the main database for users and cameras.

Pydantic models for request validation and data serialization.

Kafka message broker for event streaming (camera_created and camera_deleted events).

aiokafka for asynchronous Kafka producer and consumer.

JWT-based authentication for secure API access.

Asynchronous consumer running alongside the FastAPI app.

## Project Structure
```
Fastapi---kakfa/
│
├─ app/
│   ├─ __init__.py
│   ├─ main.py              # FastAPI app entrypoint
│   ├─ api.py               # REST API routes
│   ├─ kafka_manager.py     # Kafka producer & consumer
│   ├─ config.py            # Project settings (MongoDB URI, Kafka bootstrap, JWT secret)
│   ├─ db.py                # MongoDB connection helper
│   └─ models.py            # Pydantic models for User & Camera
│
├─ myenv/                   # Python virtual environment
├─ requirements.txt         # Python dependencies
└─ README.md
```

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/fastapi-kafka.git
cd fastapi-kafka
```

## Create a virtual environment and activate it:
```bash
python -m venv myenv
source myenv/bin/activate    # Linux/macOS
myenv\Scripts\activate       # Windows
```

## Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

**Make sure Kafka and MongoDB are running.**

Start the FastAPI app:
```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000
 to access the API.

The Kafka consumer runs automatically alongside the FastAPI app.

## **API Endpoints**
Root

GET /
Test if the service is running.

{
  "message": "fastapi + kafka + mongodb is running successfully"
}

## **Authentication**

POST /register → register a new user

POST /login → login and get JWT token

## **Cameras**

POST /cameras → create a camera (sends a Kafka camera_created event)

GET /list_cameras → list cameras for the logged-in user

DELETE /cameras/{camera_id} → delete a camera (sends a Kafka camera_deleted event)

**All camera endpoints require a valid JWT token in X-Access-Token header.**

## Kafka Event Flow

Producer: aiokafka.AIOKafkaProducer sends JSON messages to camera_events topic.

Consumer: aiokafka.AIOKafkaConsumer prints received messages asynchronously.

Example events:

// camera_created
{
  "event": "camera_created",
  "data": { "id": "abc123", "name": "Front Door", "location": "Lobby", "owner": "user1" }
}

// camera_deleted
{
  "event": "camera_deleted",
  "data": { "id": "abc123" }
}



**Notes**

Kafka consumer runs asynchronously in the FastAPI lifespan context.

You do not need to call the consumer in the API routes; it automatically listens to events.

Make sure Kafka broker and MongoDB are running before starting the app.

JWT authentication is simple; in production, consider hashing passwords.