# Project-Talk_With_YT_Video
A Streamlit app that lets users input a YouTube video URL, fetches and processes the video transcript, creates searchable embeddings, and enables users to ask questions about the video content using a retrieval-augmented language model.
# Youtube_Video_Chat

A Streamlit app to interactively chat with YouTube videos by fetching and processing their transcripts.

---

## Project Structure

- `app.py`  
  Main Streamlit app that takes a YouTube URL, fetches the transcript, creates embeddings, and answers user questions using a language model.

- `transcript.py`  
  Utility module to extract video ID from a URL and fetch video transcripts using the YouTube Transcript API.

- `try.ipynb`  
  Demo notebook for experimenting and testing the transcript fetching and processing workflow.

- `.env`  
  Stores sensitive API keys (e.g., `GROQ_API_KEY`). **Should be added to `.gitignore` to keep credentials safe.**
-'requirement.txt'
  Have all the dependecies

---

## Features

- Accepts YouTube video URL input (supports multiple URL formats).
- Supports transcript fetching in English and Hindi.
- Splits transcripts into manageable chunks for embedding.
- Creates semantic vector search with FAISS and HuggingFace embeddings.
- Uses ChatGroq LLM for retrieval-augmented Q&A on video content.
- Simple and interactive Streamlit user interface.

---

## Setup

1. Clone the repo:
   ```bash
   git clone <repo_url>
   cd Youtube_Video_Chat

2. Create and activate a virtual environment:

```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

4.Create a .env file and add your API key:
```bash
GROQ_API_KEY=your_api_key_here
```
5. Run the app
```bash
streamlit run app.py



