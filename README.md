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

### Prerequisites
- **Python 3.11** (strongly recommended for best compatibility)
- pip (latest version)

1. **Create virtual environment**
   ```bash
   # Recommended: Use Python 3.11 specifically
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Alternative: Use default Python 3 (ensure it's 3.11)
   python3 -m venv venv
   source venv/bin/activate
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
  "color": "#FFFFFF",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "synced": "boolean"
}
```

## 🛠️ Development

```bash
# Create and activate virtual environment (Python 3.11 recommended)
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload

# Run on specific port
uvicorn app.main:app --port 8080

# Run with both reload and custom port
uvicorn app.main:app --port 8080 --reload
```

## 🐛 Troubleshooting

### Python Version Compatibility
This project is **optimized for Python 3.11** and tested with this version. For best compatibility:

1. **Install Python 3.11**:
   ```bash
   # macOS with Homebrew
   brew install python@3.11

   # Ubuntu/Debian
   sudo apt update && sudo apt install python3.11 python3.11-venv

   # Verify installation
   python3.11 --version
   ```

2. **Create virtual environment with Python 3.11**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies with exact versions**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Always ensure virtual environment is activated** before running commands

### Common Issues
- **Port already in use**: Use `--port 8001` or kill existing process
- **Import errors**: Ensure virtual environment is activated
- **Firebase errors**: Check `.env` configuration

## 📋 Features

- ✅ CRUD operations for notes
- ✅ Search functionality
- ✅ Pagination support
- ✅ Note color customization (hex format)
- ✅ Firebase authentication integration
- ✅ Data validation with Pydantic
- ✅ Proper error handling
- ✅ CORS configuration
- ✅ Comprehensive logging
- ✅ Python 3.11 compatible

## 🔧 Configuration

Environment variables are managed through `.env` file:

- Firebase credentials
- JWT settings
- API configuration
- CORS origins

See `.env.example` for all available options.

## 📱 Frontend Integration

This backend is designed to work with Flutter frontend applications using Firebase Authentication. The frontend handles user authentication, and this backend manages the notes data.