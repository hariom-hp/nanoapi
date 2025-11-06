import yt_dlp
from pathlib import Path

url = input("Enter video URL: ")

Path('downloads').mkdir(exist_ok=True)

ydl_opts = {
    'format': 'best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'nocheckcertificate': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("✅ Download complete!")
