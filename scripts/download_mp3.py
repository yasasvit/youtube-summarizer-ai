import subprocess
import os

# Define input and output paths
input_file = "input/youtube_links.txt"
output_dir = "data/mp3"

os.makedirs(output_dir, exist_ok=True)

# Read YouTube links
with open(input_file, "r") as f:
    links = [line.strip() for line in f if line.strip()]

# Download each link as MP3
for url in links:
    print(f"Downloading: {url}")
    command = ["yt-dlp", "-x", "--audio-format", "mp3", "-P", output_dir, url]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}: {e}")
