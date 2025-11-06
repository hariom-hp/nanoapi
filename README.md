# 🎬 Multi-Platform Video Downloader

A powerful Python-based video downloader supporting 1000+ platforms including YouTube, Instagram, TikTok, Twitter, and many more!

## ✨ Features

- 📹 Download videos in the best quality available
- 🎵 Automatic audio and video merging
- 📊 Real-time download progress display
- 🌐 Support for 1000+ websites
- 💾 Automatic file organization
- 🎯 User-friendly interface

## ✅ Supported Platforms

- **YouTube** - All video types
- **Facebook** - Public videos
- **Instagram** - Reels, posts, IGTV (public only)
- **Twitter / X** - Video tweets
- **TikTok** - All public videos
- **Vimeo** - Public and unlisted videos
- **Reddit** - Video posts
- **Dailymotion**
- **Twitch** - Clips and VODs
- **And 1000+ more sites!**

## 🚀 Installation

1. **Clone or download this project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install directly:
   ```bash
   pip install yt-dlp
   ```

## 📖 Usage

### Basic Usage

Run the script:
```bash
python video_downloader.py
```

Then enter the video URL when prompted.

### Example URLs

```
YouTube: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Instagram: https://www.instagram.com/reel/ABC123/
TikTok: https://www.tiktok.com/@user/video/1234567890
Twitter: https://twitter.com/user/status/1234567890
```

## 📁 Output

All downloaded videos are saved to the `downloads/` folder with the format:
```
downloads/[Video Title].mp4
```

## ⚙️ Configuration

The downloader uses the following settings by default:

- **Format**: Best video + best audio merged
- **Output Format**: MP4
- **Output Template**: `downloads/%(title)s.%(ext)s`

To customize these settings, edit the `ydl_opts` dictionary in `video_downloader.py`.

## 🔧 Advanced Configuration Examples

### Download Audio Only (MP3)
```python
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s',
}
```

### Download Specific Quality
```python
ydl_opts = {
    'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
    'merge_output_format': 'mp4',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
}
```

### Download Playlist
The script automatically handles playlists. Just paste a playlist URL!

## 🛠️ Troubleshooting

### Issue: "Unable to extract video data"
- **Solution**: Make sure the video is public and accessible
- Try updating yt-dlp: `pip install --upgrade yt-dlp`

### Issue: "FFmpeg not found"
- **Solution**: Install FFmpeg for better video processing
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org)

### Issue: Downloads are slow
- Check your internet connection
- Try downloading at a different time
- Some platforms may rate-limit downloads

## 📋 Requirements

- Python 3.7 or higher
- yt-dlp
- FFmpeg (optional but recommended for best results)

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## ⚖️ Legal Notice

This tool is for personal use only. Please respect copyright laws and terms of service of the platforms you download from. Only download content you have permission to download.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Supports 1000+ websites thanks to the yt-dlp community

---

**Made with ❤️ for video enthusiasts**
