# FastAPI Video Downloader

API server for downloading videos from 1000+ platforms.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload
```

Server runs at: **http://127.0.0.1:8000**

## 📡 API Endpoints

### 1. **GET /** - API Info
```bash
curl http://127.0.0.1:8000/
```

### 2. **POST /download** - Download Video
```bash
curl -X POST http://127.0.0.1:8000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/shorts/9wKG_BHjMSI"}'
```

Response:
```json
{
  "status": "success",
  "message": "Download complete",
  "filename": "abc123.mp4",
  "title": "Video Title"
}
```

### 3. **GET /file/{filename}** - Download File
```bash
curl http://127.0.0.1:8000/file/abc123.mp4 --output video.mp4
```

## 🧪 Test Examples

### YouTube Short
```bash
curl -X POST http://127.0.0.1:8000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/shorts/9wKG_BHjMSI"}'
```

### Instagram Reel
```bash
curl -X POST http://127.0.0.1:8000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/reel/DJhkAQGNF-t/"}'
```

### TikTok Video
```bash
curl -X POST http://127.0.0.1:8000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.tiktok.com/@user/video/123456"}'
```

## 📚 Interactive Docs

Visit these URLs when server is running:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## ✅ Supported Platforms

- YouTube
- Facebook
- Instagram
- Twitter/X
- TikTok
- Vimeo
- Reddit
- 1000+ more

## 📁 Files

Downloads saved to `downloads/` folder with unique filenames.
