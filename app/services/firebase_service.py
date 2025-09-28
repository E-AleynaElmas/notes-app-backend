import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
from google.cloud.firestore_v1 import FieldFilter
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.config import settings
from app.models.note import NoteModel
import logging

logger = logging.getLogger(__name__)

class FirebaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if not self.initialized:
            try:
                # Initialize Firebase Admin SDK
                cred = credentials.Certificate(settings.get_firebase_credentials())
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.initialized = True
                logger.info("Firebase initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase: {str(e)}")
                raise

    # Collection references
    def notes_collection(self):
        return self.db.collection('notes')

    def users_collection(self):
        return self.db.collection('users')

    # User operations
    async def verify_user(self, id_token: str) -> Optional[Dict[str, Any]]:
        """Verify Firebase ID token"""
        try:
            if not id_token or not id_token.strip():
                logger.error("Empty or None token provided")
                return None

            # Log first few chars for debugging (don't log full token for security)
            logger.info(f"Verifying token starting with: {id_token[:20]}...")

            decoded_token = firebase_auth.verify_id_token(id_token)
            logger.info(f"Token verified successfully for user: {decoded_token.get('uid')}")
            return decoded_token
        except Exception as e:
            logger.error(f"Error verifying token: {type(e).__name__}: {str(e)}")
            return None

    # Note operations
    async def create_note(self, note: NoteModel) -> str:
        """Create a new note in Firestore"""
        try:
            note.created_at = datetime.utcnow()
            note.updated_at = datetime.utcnow()

            doc_ref = self.notes_collection().add(note.to_dict())
            return doc_ref[1].id
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            raise

    async def get_user_notes(
        self,
        user_id: str,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """Get all notes for a user with optional search and pagination"""
        try:
            # Base query - no ordering to avoid composite index requirement
            query = self.notes_collection().where(
                filter=FieldFilter('user_id', '==', user_id)
            )

            # Get all documents for search/filtering (no ordering in Firestore)
            all_docs = query.stream()
            all_notes = []

            for doc in all_docs:
                note_data = doc.to_dict()
                note_data['id'] = doc.id

                # Apply search filter if provided
                if search:
                    search_lower = search.lower()
                    if (search_lower in note_data.get('title', '').lower() or
                        search_lower in note_data.get('content', '').lower() or
                        any(search_lower in tag.lower() for tag in note_data.get('tags', []))):
                        all_notes.append(note_data)
                else:
                    all_notes.append(note_data)

            # Sort by pinned status first, then by updated_at (in memory)
            all_notes.sort(key=lambda x: (
                not x.get('is_pinned', False),  # Pinned notes first (False sorts before True)
                -(x.get('updated_at').timestamp() if x.get('updated_at') else 0)  # Then by updated_at descending
            ))

            # Apply pagination
            total = len(all_notes)
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_notes = all_notes[start_idx:end_idx]

            return {
                'notes': paginated_notes,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }

        except Exception as e:
            logger.error(f"Error getting user notes: {str(e)}")
            raise

    async def get_note_by_id(self, note_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific note by ID"""
        try:
            doc = self.notes_collection().document(note_id).get()

            if not doc.exists:
                return None

            note_data = doc.to_dict()

            # Verify ownership
            if note_data.get('user_id') != user_id:
                return None

            note_data['id'] = doc.id
            return note_data

        except Exception as e:
            logger.error(f"Error getting note: {str(e)}")
            raise

    async def update_note(self, note_id: str, user_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a note"""
        try:
            # First verify ownership
            existing_note = await self.get_note_by_id(note_id, user_id)
            if not existing_note:
                return False

            # Add updated timestamp
            update_data['updated_at'] = datetime.utcnow()

            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}

            # Update the document
            self.notes_collection().document(note_id).update(update_data)
            return True

        except Exception as e:
            logger.error(f"Error updating note: {str(e)}")
            raise

    async def delete_note(self, note_id: str, user_id: str) -> bool:
        """Delete a note"""
        try:
            # First verify ownership
            existing_note = await self.get_note_by_id(note_id, user_id)
            if not existing_note:
                return False

            # Delete the document
            self.notes_collection().document(note_id).delete()
            return True

        except Exception as e:
            logger.error(f"Error deleting note: {str(e)}")
            raise

# Singleton instance
firebase_service = FirebaseService()