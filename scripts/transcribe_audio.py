import os
import openai
import json
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Load env variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
logging.info("OpenAI API key loaded successfully")

# Load file
audio_path = "data/mp3/audio-biology-v1.mp3"
transcript_path = "data/transcripts/audio-biology-v1.transcript.json"

# Check if transcript file exists to avoid API call
if os.path.exists(transcript_path):
    logging.info(f"Loading transcript from: {transcript_path}")
    with open(transcript_path, "r") as f:
        transcript_dict = json.load(f)
else: 
    # If transcript not found, transcribe audio via OpenAI Whisper API
    logging.info(f"Transcribing audio file: {audio_path}")
    with open(audio_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1"
        )
        
        # Save transcription in local json file
        transcript_dict = transcript.to_dict()
        with open(transcript_path, "w") as f:
            json.dump(transcript_dict, f, indent=2)
        logging.info(f"Transcript saved to: {transcript_path}")

logging.info(f"Transcription (first 500 chars): {transcript_dict['text'][:500]}...")
