from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import subprocess
import re
import os
import random
from typing import Any

app = FastAPI(title="Video Downloader API")

# Rotating proxy list (use free proxies or premium service)
PROXY_LIST = [
    # Add your proxy list here - format: "http://user:pass@host:port"
    # Example: "http://proxy1.example.com:8080"
    # For production, use services like:
    # - Bright Data (https://brightdata.com) - $500/month residential
    # - Smartproxy (https://smartproxy.com) - $75/month
    # - ProxyMesh (https://proxymesh.com) - $9.95/month
    # Leave empty to use direct connection (will get blocked)
]

def get_random_proxy():
    """Get a random proxy from the list"""
    if PROXY_LIST:
        return random.choice(PROXY_LIST)
    return None

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
    
    # Get random proxy
    proxy = get_random_proxy()
    
    # Setup cookies - either from file or environment variable
    cookie_file = None
    if os.path.exists('cookies.txt'):
        cookie_file = 'cookies.txt'
        print("🍪 Using cookies from cookies.txt")
    elif os.getenv('COOKIES_CONTENT'):
        # Write cookies from environment variable to temp file
        cookie_file = '/tmp/cookies.txt'
        with open(cookie_file, 'w') as f:
            f.write(os.getenv('COOKIES_CONTENT', ''))
        print("🍪 Using cookies from environment variable")
    
    ydl_opts: dict[str, Any] = {
        'format': 'best[protocol^=http][ext=mp4]/best[protocol^=http]/best',
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'cookiefile': cookie_file,  # ✅ Use cookies for authentication
        'http_chunk_size': 10485760,
        'concurrent_fragment_downloads': 8,
        'buffersize': 32768,
        'retries': 10,
        'fragment_retries': 10,
        'socket_timeout': 30,
        'extractor_args': {
            'youtube': {
                'player_client': ['android_creator'],
                'skip': ['hls', 'dash'],
            }
        },
    }
    
    # Add proxy if available
    if proxy:
        ydl_opts['proxy'] = proxy
        print(f"🔐 Using proxy: {proxy.split('@')[1] if '@' in proxy else proxy}")
    else:
        print("⚠️ No proxy configured - may get blocked by platforms")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
            info = ydl.extract_info(video.url, download=False)
            title = sanitize_filename(info.get('title', 'video'))
            ext = info.get('ext', 'mp4')
        
        print(f"🎬 Downloading: {title}")
        
        # Build yt-dlp command with proxy and cookies
        cmd = [
            'yt-dlp',
            '-f', 'best[protocol^=http][ext=mp4]/best[protocol^=http]/best',
            '--no-check-certificate',
            '--concurrent-fragments', '8',
            '--buffer-size', '32K',
            '--http-chunk-size', '10M',
            '--socket-timeout', '30',
            '--no-part',
            '--extractor-args', 'youtube:player_client=android_creator',
        ]
        
        # Add cookies if available
        if cookie_file:
            cmd.extend(['--cookies', cookie_file])
        
        # Add proxy to command if available
        if proxy:
            cmd.extend(['--proxy', proxy])
        
        cmd.extend(['-o', '-', video.url])
        
        # Stream video using subprocess
        def generate():
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                bufsize=2097152
            )
            stdout = process.stdout
            if stdout is None:
                process.wait()
                return
            while True:
                chunk = stdout.read(131072)
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
