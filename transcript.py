import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    # Handle various formats
    parsed_url = urlparse(url)
    if "youtube" in parsed_url.netloc:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip('/')
    else:
        raise ValueError("Invalid YouTube URL")

def get_transcript_from_url(youtube_url, lang="en"):
    video_id = extract_video_id(youtube_url)
    if not video_id:
        raise ValueError("Could not extract video ID from URL.")
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        return transcript
    except Exception as e:
        print("Error fetching transcript:", e)
        return None
