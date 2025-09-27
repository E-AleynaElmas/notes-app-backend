from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from app.api.dependencies import get_current_user, get_firebase_service
from app.schemas.note import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    NotesListResponse
)
from app.models.note import NoteModel
from app.services.firebase_service import FirebaseService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/notes", response_model=NotesListResponse)
async def get_notes(
    search: Optional[str] = Query(None, description="Search query for title, content, or tags"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    current_user: dict = Depends(get_current_user),
    firebase: FirebaseService = Depends(get_firebase_service)
):
    """
    Get all notes for the authenticated user.

    - **search**: Optional search query to filter notes
    - **page**: Page number for pagination
    - **page_size**: Number of items per page
    """
    try:
        result = await firebase.get_user_notes(
            user_id=current_user["user_id"],
            search=search,
            page=page,
            page_size=page_size
        )

        # Convert to response model
        notes_response = []
        for note_data in result['notes']:
            notes_response.append(NoteResponse(
                id=note_data['id'],
                title=note_data['title'],
                content=note_data['content'],
                is_pinned=note_data.get('is_pinned', False),
                tags=note_data.get('tags', []),
                color=note_data.get('color', '#FFFFFF'),
                created_at=note_data['created_at'],
                updated_at=note_data['updated_at']
            ))

        return NotesListResponse(
            notes=notes_response,
            total=result['total'],
            page=result['page'],
            page_size=result['page_size']
        )

    except Exception as e:
        logger.error(f"Error fetching notes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch notes"
        )

@router.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    current_user: dict = Depends(get_current_user),
    firebase: FirebaseService = Depends(get_firebase_service)
):
    """
    Create a new note for the authenticated user.
    """
    try:
        # Create note model
        note_model = NoteModel(
            user_id=current_user["user_id"],
            title=note.title,
            content=note.content,
            is_pinned=note.is_pinned,
            tags=note.tags,
            color=note.color
        )

        # Save to Firestore
        note_id = await firebase.create_note(note_model)

        # Retrieve created note
        created_note = await firebase.get_note_by_id(note_id, current_user["user_id"])

        if not created_note:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created note"
            )

        return NoteResponse(
            id=created_note['id'],
            title=created_note['title'],
            content=created_note['content'],
            is_pinned=created_note.get('is_pinned', False),
            tags=created_note.get('tags', []),
            color=created_note.get('color', '#FFFFFF'),
            created_at=created_note['created_at'],
            updated_at=created_note['updated_at']
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating note: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create note"
        )

@router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    note_update: NoteUpdate,
    current_user: dict = Depends(get_current_user),
    firebase: FirebaseService = Depends(get_firebase_service)
):
    """
    Update an existing note.
    """
    try:
        # Prepare update data
        update_data = {}
        if note_update.title is not None:
            update_data['title'] = note_update.title
        if note_update.content is not None:
            update_data['content'] = note_update.content
        if note_update.is_pinned is not None:
            update_data['is_pinned'] = note_update.is_pinned
        if note_update.tags is not None:
            update_data['tags'] = note_update.tags
        if note_update.color is not None:
            update_data['color'] = note_update.color

        # Update note
        success = await firebase.update_note(
            note_id=note_id,
            user_id=current_user["user_id"],
            update_data=update_data
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found or you don't have permission to update it"
            )

        # Retrieve updated note
        updated_note = await firebase.get_note_by_id(note_id, current_user["user_id"])

        if not updated_note:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve updated note"
            )

        return NoteResponse(
            id=updated_note['id'],
            title=updated_note['title'],
            content=updated_note['content'],
            is_pinned=updated_note.get('is_pinned', False),
            tags=updated_note.get('tags', []),
            color=updated_note.get('color', '#FFFFFF'),
            created_at=updated_note['created_at'],
            updated_at=updated_note['updated_at']
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating note: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update note"
        )

@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    current_user: dict = Depends(get_current_user),
    firebase: FirebaseService = Depends(get_firebase_service)
):
    """
    Delete a note.
    """
    try:
        success = await firebase.delete_note(
            note_id=note_id,
            user_id=current_user["user_id"]
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found or you don't have permission to delete it"
            )

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting note: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete note"
        )