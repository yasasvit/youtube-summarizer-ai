import os
import subprocess
import openai
import json
import logging
from dotenv import load_dotenv
from markdown import markdown
from weasyprint import HTML

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Load API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
INPUT_LINKS = "input/youtube_links.txt"
MP3_DIR = "data/mp3"
TRANSCRIPTS_DIR = "data/transcripts"
SUMMARIES_DIR = "data/summaries"

os.makedirs(MP3_DIR, exist_ok=True)
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
os.makedirs(SUMMARIES_DIR, exist_ok=True)

def download_mp3(url: str) -> str:
    logging.info(f"Downloading: {url}")
    command = ["yt-dlp", "-x", "--audio-format", "mp3", "-P", MP3_DIR, url]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Download failed: {e}")
        return None

    # Try to find the most recent mp3 file added
    files = [f for f in os.listdir(MP3_DIR) if f.endswith(".mp3")]
    latest_file = max([os.path.join(MP3_DIR, f) for f in files], key=os.path.getctime)
    return latest_file

def transcribe_audio(mp3_path: str) -> str:
    base = os.path.splitext(os.path.basename(mp3_path))[0]
    transcript_path = os.path.join(TRANSCRIPTS_DIR, f"{base}.transcript.json")

    if os.path.exists(transcript_path):
        logging.info(f"Transcript exists: {transcript_path}")
        with open(transcript_path) as f:
            return json.load(f)['text']
    
    logging.info(f"Transcribing {mp3_path}")
    with open(mp3_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(file=audio_file, model="whisper-1")
        transcript_dict = transcript.to_dict()
    
    with open(transcript_path, "w") as f:
        json.dump(transcript_dict, f, indent=2)

    return transcript_dict['text']

def summarize_transcript(transcript_text: str, base_name: str):
    summary_path = os.path.join(SUMMARIES_DIR, f"{base_name}.summary.md")
    response_path = os.path.join(SUMMARIES_DIR, f"{base_name}.response.json")

    if os.path.exists(summary_path):
        logging.info(f"Summary already exists: {summary_path}")
        return summary_path

    system_prompt = "You are a helpful assistant that summarizes educational transcripts."
    user_prompt = (
        "Please summarize this transcript into a well-structured study guide. "
        "Use section titles, bullet points, and make it easy to read for students.\n\n"
        f"Transcript:\n{transcript_text}"
    )

    logging.info("Calling OpenAI to generate summary...")
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    response_dict = response.to_dict()
    summary_text = response.choices[0].message.content.strip()

    with open(response_path, "w") as f:
        json.dump(response_dict, f, indent=2)
    with open(summary_path, "w") as f:
        f.write(summary_text)
    
    return summary_path

def convert_md_to_pdf(md_path: str):
    base = os.path.splitext(os.path.basename(md_path))[0]
    pdf_path = os.path.join(SUMMARIES_DIR, f"{base}.pdf")
    with open(md_path) as f:
        md_text = f.read()
    
    html_body = markdown(md_text, extensions=["extra", "toc", "codehilite"])
    html = f"""
    <html><head><meta charset='utf-8'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown-light.min.css">
    <style>body{{max-width:800px;margin:2rem auto;padding:2rem;background:white;}}</style>
    </head><body class='markdown-body'>{html_body}</body></html>
    """
    HTML(string=html).write_pdf(pdf_path)
    logging.info(f"PDF saved: {pdf_path}")

def main():
    with open(INPUT_LINKS) as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        mp3_path = download_mp3(url)
        if not mp3_path:
            continue
        
        transcript_text = transcribe_audio(mp3_path)
        base_name = os.path.splitext(os.path.basename(mp3_path))[0]
        md_path = summarize_transcript(transcript_text, base_name)
        convert_md_to_pdf(md_path)

if __name__ == "__main__":
    main()
