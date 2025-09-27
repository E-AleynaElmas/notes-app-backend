from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class NoteModel:
    """Firestore document model for Note"""
    def __init__(
        self,
        id: Optional[str] = None,
        user_id: str = None,
        title: str = None,
        content: str = None,
        is_pinned: bool = False,
        tags: list = None,
        color: str = "#FFFFFF",
        created_at: datetime = None,
        updated_at: datetime = None,
        synced: bool = True
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.is_pinned = is_pinned
        self.tags = tags or []
        self.color = color or "#FFFFFF"
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.synced = synced

    def to_dict(self):
        """Convert model to Firestore document"""
        return {
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'is_pinned': self.is_pinned,
            'tags': self.tags,
            'color': self.color,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'synced': self.synced
        }

    @staticmethod
    def from_dict(doc_id: str, doc_dict: dict):
        """Create model from Firestore document"""
        return NoteModel(
            id=doc_id,
            user_id=doc_dict.get('user_id'),
            title=doc_dict.get('title'),
            content=doc_dict.get('content'),
            is_pinned=doc_dict.get('is_pinned', False),
            tags=doc_dict.get('tags', []),
            color=doc_dict.get('color', '#FFFFFF'),
            created_at=doc_dict.get('created_at'),
            updated_at=doc_dict.get('updated_at'),
            synced=doc_dict.get('synced', True)
        )