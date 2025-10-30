from database.config import client
from database.historySchema import NoteModel
from datetime import datetime
from bson.objectid import ObjectId

db = client.notesDB
notes_collection = db.get_collection("notes")

# Helper to convert MongoDB document to dict
def note_helper(note) -> dict:
    return {
        "id": str(note["_id"]),
        "user_id": note["user_id"],
        "title": note["title"],
        "type": note["type"],
        "summary": note["summary"],
        "chat_content": note.get("chat_content"),
        "embedding_reference": note.get("embedding_reference"),
        "source": note["source"],
        "created_at": note["created_at"]
    }

# CREATE note
def create_note(note: NoteModel):
    note_dict = note.dict()
    note_dict["created_at"] = datetime.utcnow()
    result = notes_collection.insert_one(note_dict)
    created_note = notes_collection.find_one({"_id": result.inserted_id})
    return note_helper(created_note)

# READ notes by user_id
def get_notes_by_user(user_id: str):
    notes = notes_collection.find({"user_id": user_id}).sort("created_at", -1)
    return [note_helper(note) for note in notes]
