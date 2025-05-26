import os
import openai
import json
import logging
from dotenv import load_dotenv
from markdown import markdown
from weasyprint import HTML

def convert_txt_to_pdf(md_path, pdf_path):
    with open(md_path, "r") as f:
        md_text = f.read()

    html_body = markdown(md_text, extensions=["extra", "toc", "codehilite"])

    html = f"""
    <html>
    <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown-light.min.css">
    <style>
        body {{
            max-width: 800px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
        }}
        .markdown-body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            font-size: 16px;
        }}
    </style>
    </head>
    <body class="markdown-body">
    {html_body}
    </body>
    </html>
    """

    HTML(string=html).write_pdf(pdf_path)
    print(f"PDF saved to: {pdf_path}")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Load env variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
logging.info("OpenAI API key loaded successfully")

# Load transcript
transcript_path = "data/transcripts/audio-biology-v1.transcript.json"
summary_path = "data/summaries/audio-biology-v1.summary.md"
response_json_path = "data/summaries/audio-biology-v1.response.json" 

# Check if summary already generated
if os.path.exists(summary_path):
    logging.info(f"Loading summary from: {summary_path}")
    with open(summary_path, "r") as f:
        summary_text = f.read()
else:
    # Load transcript
    with open(transcript_path, "r") as f:
        transcript_dict = json.load(f)

    # Generate summary via OpenAI GPT
    logging.info("Generating summary using OpenAI GPT...")
    system_prompt = "You are a helpful assistant that summarizes educational transcripts."
    user_prompt = (
        "Please summarize this transcript into a well-structured study guide. "
        "Based on the transcript length and content, decide how many sections are appropriate. "
        "Use clear section titles and write concise paragraphs, using bullet points where helpful. "
        "Make it easy to read and suitable as a study guide for students.\n\n"
        "Transcript:\n"
        + transcript_dict['text']
    )
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Save OpenAI response locally
    response_dict = response.to_dict()
    os.makedirs(os.path.dirname(response_json_path), exist_ok=True)
    with open(response_json_path, "w") as f_json:
        json.dump(response_dict, f_json, indent=2)
    logging.info(f"Full OpenAI response saved to: {response_json_path}")

    # Save sumamry locally
    summary_text = response.choices[0].message.content.strip()
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, "w") as f_summary:
        f_summary.write(summary_text)
    logging.info(f"Summary saved to: {summary_path}")

logging.info(f"Summary (first 300 chars): {summary_text[:300]}...")

# Convert md to pdf file
pdf_output_path = "data/summaries/audio-biology-v1.summary.pdf"
convert_txt_to_pdf(summary_path, pdf_output_path)