from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteModel(BaseModel):
    user_id: str
    title: str
    type: str  # youtube, pdf, media, chatbot
    summary: str
    source: str
    chat_content: Optional[str] = None
    embedding_reference: Optional[str] = None

class NoteResponseModel(NoteModel):
    id: str
    created_at: datetime
