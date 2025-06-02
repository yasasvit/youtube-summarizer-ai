import subprocess

# Read all YouTube links from input file
input_file = "inputs/youtube_links.txt"

with open(input_file, "r") as f:
    links = [line.strip() for line in f if line.strip()]

# Loop through each link and run yt-dlp command
for url in links:
    print(f"Downloading: {url}")
    command = ["yt-dlp", "-x", "--audio-format", "mp3", url]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}: {e}")
