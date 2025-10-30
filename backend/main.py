from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils.youtube_transcript import get_transcripts
from services.YT_summarizer import summarize_long_transcript
from youtube_transcript_api._errors import IpBlocked, NoTranscriptFound
from database.historySchema import NoteModel
from database.crud import create_note, get_notes_by_user
from typing import List,Optional
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# creating a post request for summarize route with schema as url:string json object
class YouTubeRequest(BaseModel):
    url: str

class TranscriptItem(BaseModel):
    time: str
    text: str

class SummarizeRequest(BaseModel):
    url: Optional[str] = None
    transcript: Optional[List[TranscriptItem]] = None
    
        
# extracting transcript from the yt url 
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

@app.post("/summarize")
# async def summarize_youtube(req: YouTubeRequest):
#     url = req.url
#     try:
#         transcripts = get_transcripts(url)
#         summary=summarize_long_transcript(transcripts)
#         return {"summary":summary}
#     except Exception as e:
#          return {"err": str(e)}
async def summarize_youtube(req: SummarizeRequest):
    try:
        if req.transcript:
            transcripts = [item.dict() for item in req.transcript]
        elif req.url:
            transcripts = get_transcripts(req.url)
        else:
            return {"error": "Provide either a transcript or a URL"}

        summary = summarize_long_transcript(transcripts)
        return {"summary": summary}

    except Exception as e:
        return {"error": str(e)}