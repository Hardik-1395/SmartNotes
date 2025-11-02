from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from youtube_transcript_api._errors import IpBlocked, NoTranscriptFound

from utils.youtube_transcript import get_transcripts
from services.YT_summarizer import summarize_long_transcript
from database.historySchema import NoteModel, NoteResponseModel
from database.crud import create_note, get_notes_by_user

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Schemas
class YouTubeRequest(BaseModel):
    url: str

class TranscriptItem(BaseModel):
    time: str
    text: str

class SummarizeRequest(BaseModel):
    user_id: str
    title: str
    type: str = "youtube"  
    url: Optional[str] = None
    transcript: Optional[List[TranscriptItem]] = None

# --------------------------
# YouTube Transcript API
# --------------------------
@app.get("/transcript/")
def transcript_api(url: str):
    try:
        transcripts = get_transcripts(url)
        return {"transcript": transcripts}
    except IpBlocked:
        return {"error": "Your IP is blocked by YouTube. Try again later or from a different network."}
    except NoTranscriptFound:
        return {"error": "Transcript not found for this video."}
    except Exception as e:
        return {"error": str(e)}

# --------------------------
# Summarize & Save Note
# --------------------------
@app.post("/summarize")
async def summarize_youtube_and_save(req: SummarizeRequest):
    try:
        if req.transcript:
            transcripts = [item.dict() for item in req.transcript]
        elif req.url:
            transcripts = get_transcripts(req.url)
        else:
            return {"error": "Provide either a transcript or a URL"}

        summary = summarize_long_transcript(transcripts)

        note_data = NoteModel(
            user_id=req.user_id,
            title=req.title,
            type=req.type,
            summary=summary,
            source=req.url or "uploaded transcript"
        )

        saved_note = create_note(note_data)

        return {"summary": summary, "note": saved_note}

    except Exception as e:
        return {"error": str(e)}

# --------------------------
# Get Notes by User
# --------------------------
@app.get("/notes/", response_model=List[NoteResponseModel])
def get_user_notes(user_id: str = Query(..., description="ID of the logged-in user")):
    """
    Fetch all saved notes for a specific user
    """
    try:
        notes = get_notes_by_user(user_id)  # returns list of dicts
        # Return as list of NoteResponseModel for FastAPI serialization
        response_notes = [
            NoteResponseModel(**note) for note in notes
        ]
        return response_notes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
