# youtube-summarizer-ai

### Project Goal: 
Extract content from YouTube video and generate summarized notes in clean PDF using AI

### Steps:

Download audio of YT video
-> Transcribe the audio using OpenAI Whisper API
-> Send Transcripts to OpenAI API to get summary
-> Generate PDF for summary

yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=6v8djXa-IPQ&ab_channel=FreeAnimatedEducation"
