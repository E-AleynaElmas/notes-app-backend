# Notes API Backend

Professional FastAPI backend for notes management with Firebase/Firestore integration.

## 🏗️ Architecture

- **FastAPI**: Modern Python web framework
- **Firebase/Firestore**: Database and authentication
- **Pydantic**: Data validation and serialization
- **JWT**: Token-based authentication verification

## 📁 Project Structure

```
app/
├── api/
│   ├── dependencies.py      # Authentication dependencies
│   └── endpoints/
│       └── notes.py         # Notes CRUD endpoints
├── core/
│   └── security.py          # JWT and security utilities
├── models/
│   └── note.py             # Firestore data models
├── schemas/
│   └── note.py             # Pydantic schemas
├── services/
│   └── firebase_service.py # Firebase/Firestore integration
├── config.py               # Configuration management
└── main.py                 # FastAPI application
```

## 🚀 Quick Start

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Firebase Service Account credentials
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## 📚 API Documentation

- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔌 API Endpoints

### Notes Management

- `GET /api/v1/notes` - List notes with search and pagination
- `POST /api/v1/notes` - Create a new note
- `PUT /api/v1/notes/{id}` - Update a note
- `DELETE /api/v1/notes/{id}` - Delete a note

### System

- `GET /health` - Health check
- `GET /` - API info

## 🔒 Authentication

The API uses Firebase ID tokens for authentication. Include the token in the Authorization header:

```
Authorization: Bearer YOUR_FIREBASE_ID_TOKEN
```

## 🗃️ Database Schema

### Notes Collection
```json
{
  "user_id": "string",
  "title": "string",
  "content": "string",
  "is_pinned": "boolean",
  "tags": ["string"],
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "synced": "boolean"
}
```

## 🛠️ Development

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload

# Run on specific port
uvicorn app.main:app --port 8080
```

## 🐛 Troubleshooting

### Python 3.13 Compatibility
This project is optimized for Python 3.13. If you encounter build issues:

1. Use the exact versions in `requirements.txt`
2. Ensure virtual environment is activated
3. Update pip: `pip install --upgrade pip`

### Common Issues
- **Port already in use**: Use `--port 8001` or kill existing process
- **Import errors**: Ensure virtual environment is activated
- **Firebase errors**: Check `.env` configuration

## 📋 Features

- ✅ CRUD operations for notes
- ✅ Search functionality
- ✅ Pagination support
- ✅ Firebase authentication integration
- ✅ Data validation with Pydantic
- ✅ Proper error handling
- ✅ CORS configuration
- ✅ Comprehensive logging

## 🔧 Configuration

Environment variables are managed through `.env` file:

- Firebase credentials
- JWT settings
- API configuration
- CORS origins

See `.env.example` for all available options.

## 📱 Frontend Integration

This backend is designed to work with Flutter frontend applications using Firebase Authentication. The frontend handles user authentication, and this backend manages the notes data.