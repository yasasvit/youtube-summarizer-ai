# youtube-summarizer-ai

This project automates the process of creating study guides from educational YouTube videos. It downloads an MP3 from a YouTube link, transcribes the audio using OpenAI Whisper, summarizes the transcript using GPT-4, and generates a clean, structured PDF study guide.



## Requirements

Install dependencies via:

```bash
pip install -r requirements.txt
```


## How to Use

1. Download MP3 via YouTube
```bash
yt-dlp -x --audio-format mp3 "<YOUTUBE_URL>"
```

2. Transcribe the MP3
```bash
python3 transcribe_audio.py --audio-path data/audio/audio-biology-v1.mp3 --output-path data/transcripts/audio-biology-v1.transcript.json
```

3. Download MP3 via YouTube
```bash
python3 summarize_transcript.py --transcript-path data/transcripts/audio-biology-v1.transcript.json --summary-path data/summaries/audio-biology-v1.summary.md --pdf-path data/summaries/audio-biology-v1.summary.pdf
```