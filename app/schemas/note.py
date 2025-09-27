from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=10000)
    is_pinned: bool = False
    tags: Optional[List[str]] = []
    color: Optional[str] = Field(default="#FFFFFF", regex="^#[0-9A-Fa-f]{6}$")

    @validator('title', 'content')
    def validate_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace')
        return v.strip()

    @validator('color')
    def validate_color(cls, v):
        if v is None:
            return "#FFFFFF"
        return v.upper()

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1, max_length=10000)
    is_pinned: Optional[bool] = None
    tags: Optional[List[str]] = None
    color: Optional[str] = Field(None, regex="^#[0-9A-Fa-f]{6}$")

    @validator('title', 'content')
    def validate_not_empty_if_provided(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Field cannot be empty or whitespace')
        return v.strip() if v else v

    @validator('color')
    def validate_color_if_provided(cls, v):
        if v is not None:
            return v.upper()
        return v

class NoteInDB(NoteBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    synced: bool = True

class NoteResponse(NoteBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class NotesListResponse(BaseModel):
    notes: List[NoteResponse]
    total: int
    page: int = 1
    page_size: int = 20