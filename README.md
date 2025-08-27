# FastAPI Face Recognition Service

A robust microservice for face recognition and verification built with FastAPI, featuring event-based user management and Cloudinary cloud storage integration.

## Features

- **Face Registration**: Add users with their face images to specific events
- **Face Verification**: Verify user identity against registered faces in events
- **Event Management**: Create, manage, and delete events with associated users
- **User Management**: Get and delete users within events
- **Cloud Storage**: Cloudinary integration for persistent data storage
- **Comprehensive Logging**: Detailed logging for monitoring and debugging
- **RESTful API**: Clean, documented API endpoints with CORS support

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **face-recognition**: Python library for face recognition using dlib
- **Cloudinary**: Cloud-based storage for face embeddings
- **NumPy**: Numerical computing for face embeddings
- **Pillow**: Image processing library
- **Uvicorn**: ASGI server for running the application

## Project Structure

```
fastapi-face-recognition/
├── app/
│   ├── api/
│   │   ├── events.py                    # Event management endpoints
│   │   ├── routes_add.py               # User registration endpoints
│   │   ├── routes_verify.py            # Face verification endpoints
│   │   ├── get_transaction_details.py  # Transaction details (placeholder)
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py                   # Configuration management
│   │   ├── logging_config.py           # Logging setup
│   │   └── utils.py                    # Utility functions
│   ├── services/
│   │   ├── cloud_storage.py            # Cloudinary integration
│   │   ├── event_service.py            # Event management logic
│   │   ├── face_service.py             # Face recognition logic
│   │   └── storage.py                  # Data storage utilities
│   ├── models/                         # Data models
│   └── main.py                         # FastAPI application entry point
├── logs/                               # Application logs
├── tests/                              # Test files
├── .env                                # Environment variables
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Cloudinary account (for cloud storage)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-face-recognition
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

## Usage

### Starting the Server

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### User Registration

**POST** `/addUser/`

Register a new user with their face image to an event.

**Parameters:**
- `event_name` (form): Name of the event
- `username` (form): Username for the person
- `file` (file): Image file containing the person's face

**Response:**
```json
{
  "status": "success",
  "message": "User 'john_doe' successfully added to event 'conference_2024'",
  "embedding_count": 1
}
```

### Face Verification

**POST** `/verify/`

Verify if a face image matches any registered user in an event.

**Parameters:**
- `event_name` (form): Name of the event to verify against
- `file` (file): Image file to verify

**Response:**
```json
{
  "verified": true,
  "username": "john_doe",
  "message": "Face verified successfully for user 'john_doe' in event 'conference_2024'",
  "confidence": 85.67
}
```

### Event Management

**GET** `/api/events`

Get all events with user counts.

**Response:**
```json
{
  "events": [
    {
      "event_name": "conference_2024",
      "user_count": 15
    }
  ]
}
```

**DELETE** `/api/events/{event_name}`

Delete an event and all associated user data.

**Response:**
```json
{
  "status": "success",
  "message": "Event 'conference_2024' deleted"
}
```

### User Management

**GET** `/api/all_user?event_name={event_name}`

Get all users in a specific event.

**Response:**
```json
{
  "users": ["john_doe", "jane_smith", "bob_wilson"]
}
```

**GET** `/api/delete_user?event_name={event_name}&user_id={user_id}`

Delete a specific user from an event.

**Response:**
```json
{
  "status": "success",
  "message": "User 'john_doe' deleted from event 'conference_2024'"
}
```

### Debug Endpoints

**GET** `/api/debug/cloudinary-data`

View raw Cloudinary data for debugging purposes.

**GET** `/get_transaction_details/`

Placeholder endpoint for transaction details (not implemented).

## Configuration

### Face Recognition Settings

- **Threshold**: `0.6` (adjustable in `face_service.py`)
  - Lower values = stricter matching
  - Higher values = more lenient matching
- **Distance Calculation**: Euclidean distance between face embeddings
- **Confidence Score**: Calculated as `(1 - distance) * 100`

### Cloud Storage

- Face embeddings are stored as JSON in Cloudinary
- Automatic retry mechanism for network failures
- Cache-busting for real-time data updates

## Error Handling

The API provides comprehensive error handling with detailed responses:

**Common Error Responses:**

```json
{
  "status": "error",
  "message": "No face detected in image"
}
```

```json
{
  "verified": false,
  "username": null,
  "message": "Event 'nonexistent_event' not found or has no registered users"
}
```

**HTTP Status Codes:**
- **200**: Success
- **400**: Bad Request (invalid parameters)
- **404**: Not Found (event/user not found)
- **500**: Internal Server Error

## Security Considerations

- Face embeddings are stored as numerical vectors (not actual images)
- Cloudinary provides secure cloud storage with API authentication
- Environment variables protect sensitive credentials
- Input validation prevents malicious uploads
- CORS enabled for cross-origin requests

## Performance

- Face encoding: ~100-500ms per image
- Verification against 100 users: ~50-100ms
- Cloudinary CDN ensures fast global data access
- Retry mechanism for network reliability

## Troubleshooting

### Common Issues

1. **No face detected**
   - Ensure image has clear, front-facing face
   - Check image quality and lighting
   - Verify image format (JPEG, PNG supported)

2. **Cloudinary connection errors**
   - Verify environment variables in `.env`
   - Check internet connectivity
   - Review Cloudinary account status

3. **Import/dependency errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Activate virtual environment
   - Check Python version compatibility

### Logging

- Logs are automatically generated in `logs/app.log`
- Log levels: INFO, WARNING, ERROR
- Detailed request/response logging for debugging

## Development

### Adding New Features

1. Create new route files in `app/api/`
2. Add business logic in `app/services/`
3. Update `main.py` to include new routers
4. Add appropriate logging and error handling

### Testing

Run tests using:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the logs in `logs/app.log`
2. Review the API documentation at `/docs`
3. Create an issue in the repository

---

**Note**: This service requires proper lighting and clear face images for optimal performance. Ensure users are facing the camera directly during registration and verification.