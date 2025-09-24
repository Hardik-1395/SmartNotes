from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from urllib.parse import urlparse, parse_qs
from deep_translator import GoogleTranslator

CHUNK_DURATION = 120

def merge_lines_into_chunks(lines, chunk_duration=CHUNK_DURATION):
    """Merge transcript lines into chunks of ~chunk_duration seconds."""
    chunks = []
    current_chunk = {"start": lines[0].start, "text": ""}
    current_duration = 0

    for line in lines:
        if current_duration + line.start - current_chunk["start"] >= chunk_duration:
            chunks.append(current_chunk)
            current_chunk = {"start": line.start, "text": line.text}
            current_duration = 0
        else:
            if current_chunk["text"]:
                current_chunk["text"] += " "
            current_chunk["text"] += line.text
            current_duration = line.start - current_chunk["start"]

    if current_chunk["text"]:
        chunks.append(current_chunk)
    return chunks

def format_time(seconds: float) -> str:
    """Convert seconds into MM:SS format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"

def extract_videoID(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc
    path = parsed_url.path

    if "youtube.com" in hostname and path == "/watch":
        return parse_qs(parsed_url.query).get("v", [""])[0]
    elif "youtube.com" in hostname and path.startswith("/live/"):
        return path.split("/")[2]
    elif "youtu.be" in hostname:
        return path.lstrip("/").split("/")[0]
    elif "youtube.com" in hostname and path.startswith("/embed/"):
        return path.split("/")[2]
    else:
        raise ValueError("Unsupported URL format")

def batch_translate(texts, target="en"):
    """Translate a list of texts in one request (faster)."""
    return GoogleTranslator(source="auto", target=target).translate_batch(texts)

def get_transcripts(url: str):
    """Return transcripts as a list of {time, text} dictionaries."""
    video_id = extract_videoID(url)
    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.fetch(video_id, languages=['en'])
        transcript_lang = 'en'
    except NoTranscriptFound:
        transcript_list = api.fetch(video_id, languages=['hi'])
        transcript_lang = 'hi'

    chunks = merge_lines_into_chunks(transcript_list)

    if transcript_lang != "en":
        # Batch translate all Hindi chunks into English
        hindi_texts = [chunk["text"] for chunk in chunks]
        english_texts = batch_translate(hindi_texts, "en")

        formatted_transcripts = [
            {"time": format_time(chunk["start"]), "text": translated}
            for chunk, translated in zip(chunks, english_texts)
        ]
    else:
        formatted_transcripts = [
            {"time": format_time(chunk["start"]), "text": chunk["text"]}
            for chunk in chunks
        ]

    return formatted_transcripts

# Example usage
if __name__ == "__main__":
    url = "https://youtu.be/ITkIdDyXeag?si=Lp5VKHgid4EZAYcG"
    transcripts = get_transcripts(url)

    for line in transcripts:
        print(line)
