from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import subprocess
import re
import os
from typing import Any

app = FastAPI(title="Video Downloader API")

# Add CORS middleware for Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoURL(BaseModel):
    url: str

def sanitize_filename(filename):
    """Remove emojis and special characters from filename"""
    # Remove emojis
    filename = re.sub(r'[^\x00-\x7F]+', '', filename)
    # Remove special characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename).strip()
    return filename if filename else 'video'

@app.get("/health")
async def health_check():
    """Health check endpoint for Flutter"""
    return {"status": "ok", "message": "API is running"}

@app.post("/download")
async def download_video(video: VideoURL):
    """Stream video directly to user without saving on server"""
    
    print(f"📥 Received URL: {video.url}")
    
    # Validate URL
    if not video.url.startswith(('http://', 'https://')):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    ydl_opts: dict[str, Any] = {
        'format': 'best[protocol^=http][ext=mp4]/best[protocol^=http]/best',  # Prioritize HTTP MP4
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'http_chunk_size': 10485760,  # 10MB chunks
        'concurrent_fragment_downloads': 8,  # Increase to 8 parallel downloads
        'buffersize': 32768,  # 32KB buffer (doubled)
        'retries': 10,
        'fragment_retries': 10,
        'socket_timeout': 30,
        'source_address': '0.0.0.0',  # Use all network interfaces
        'throttledratelimit': None,  # Remove rate limiting
        'extractor_args': {
            'youtube': {
                'player_client': ['android_creator'],  # Use Android creator client
                'skip': ['hls', 'dash'],  # Skip HLS/DASH formats
            }
        },
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
            info = ydl.extract_info(video.url, download=False)
            title = sanitize_filename(info.get('title', 'video'))
            ext = info.get('ext', 'mp4')
        
        print(f"🎬 Downloading: {title}")
        
        # Stream video using subprocess with maximum performance settings
        def generate():
            process = subprocess.Popen([
                'yt-dlp',
                '-f', 'best[protocol^=http][ext=mp4]/best[protocol^=http]/best',
                '--no-check-certificate',
                '--concurrent-fragments', '8',
                '--buffer-size', '32K',
                '--http-chunk-size', '10M',
                '--socket-timeout', '30',
                '--no-part',
                '--extractor-args', 'youtube:player_client=android_creator',
                '-o', '-',
                video.url
            ],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                bufsize=2097152
            )
            stdout = process.stdout
            if stdout is None:
                process.wait()
                return
            while True:
                chunk = stdout.read(131072)  # 128KB chunks (doubled again)
                if not chunk:
                    break
                yield chunk
        
        # Encode filename for HTTP header
        safe_filename = title.encode('ascii', 'ignore').decode('ascii')
        if not safe_filename:
            safe_filename = 'video'
        
        return StreamingResponse(
            generate(),
            media_type='video/mp4',
            headers={
                'Content-Disposition': f'attachment; filename="{safe_filename}.{ext}"'
            }
        )
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "Video Downloader API",
        "supported_platforms": [
            "YouTube",
            "Facebook", 
            "Instagram",
            "Twitter/X",
            "TikTok",
            "Vimeo",
            "Reddit",
            "1000+ more"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
