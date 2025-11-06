# Video Downloader API - Integration Guide

## 🎯 Base URL
```
http://10.84.3.92:8000
```

## 📡 API Endpoints

### 1. Health Check
**GET** `/health`

**Response:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

---

### 2. Download Video
**POST** `/download`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://youtube.com/shorts/VIDEO_ID"
}
```

**Response:**
- **Type:** Video file stream (bytes)
- **Content-Type:** `video/mp4`
- **Header:** `Content-Disposition: attachment; filename="video_title.mp4"`

**Status Codes:**
- `200 OK` - Video downloaded successfully
- `400 Bad Request` - Invalid URL or download failed

---

## 🔧 Flutter Integration Code

### Complete Working Example

```dart
import 'package:dio/dio.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class VideoDownloader {
  final Dio _dio = Dio();
  final String baseUrl = 'http://10.84.3.92:8000';

  /// Download video from URL
  Future<Map<String, dynamic>> downloadVideo(
    String videoUrl, {
    Function(double)? onProgress,
  }) async {
    try {
      // 1. Get device storage directory
      final Directory tempDir = await getTemporaryDirectory();
      final String fileName = 'video_${DateTime.now().millisecondsSinceEpoch}.mp4';
      final String savePath = '${tempDir.path}/$fileName';

      // 2. Make POST request to download endpoint
      final response = await _dio.post(
        '$baseUrl/download',
        data: {'url': videoUrl},
        options: Options(
          headers: {'Content-Type': 'application/json'},
          responseType: ResponseType.bytes, // IMPORTANT: Receive as bytes
          receiveTimeout: const Duration(minutes: 5),
          sendTimeout: const Duration(seconds: 30),
        ),
        onReceiveProgress: (received, total) {
          if (total != -1 && onProgress != null) {
            final progress = (received / total);
            onProgress(progress);
          }
        },
      );

      // 3. Write bytes to file
      final File file = File(savePath);
      await file.writeAsBytes(response.data);

      // 4. Return success with file path
      return {
        'success': true,
        'filePath': savePath,
        'filename': fileName,
      };
      
    } on DioException catch (e) {
      // Handle network errors
      return {
        'success': false,
        'error': _getErrorMessage(e),
      };
    } catch (e) {
      // Handle other errors
      return {
        'success': false,
        'error': e.toString(),
      };
    }
  }

  /// Check if API is available
  Future<bool> isApiAvailable() async {
    try {
      final response = await _dio.get(
        '$baseUrl/health',
        options: Options(receiveTimeout: const Duration(seconds: 5)),
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  String _getErrorMessage(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
        return 'Connection timeout';
      case DioExceptionType.receiveTimeout:
        return 'Download timeout';
      case DioExceptionType.badResponse:
        return 'Server error: ${e.response?.statusCode}';
      case DioExceptionType.connectionError:
        return 'Cannot connect to server';
      default:
        return 'Network error';
    }
  }
}
```

---

## 📱 Usage Example

```dart
// Initialize
final downloader = VideoDownloader();

// Check if API is available
bool isAvailable = await downloader.isApiAvailable();
if (!isAvailable) {
  print('❌ API is not available');
  return;
}

// Download video with progress
final result = await downloader.downloadVideo(
  'https://youtube.com/shorts/9wKG_BHjMSI',
  onProgress: (progress) {
    print('Download progress: ${(progress * 100).toStringAsFixed(0)}%');
  },
);

// Handle result
if (result['success']) {
  print('✅ Video saved at: ${result['filePath']}');
} else {
  print('❌ Error: ${result['error']}');
}
```

---

## 🌐 Supported Platforms

- ✅ YouTube (videos, shorts, playlists)
- ✅ Instagram (reels, posts, IGTV - public only)
- ✅ TikTok
- ✅ Twitter/X
- ✅ Facebook
- ✅ Vimeo
- ✅ Reddit
- ✅ 1000+ other platforms

---

## ⚙️ Configuration

### pubspec.yaml
```yaml
dependencies:
  dio: ^5.4.0
  path_provider: ^2.1.0
```

### Android Permissions (android/app/src/main/AndroidManifest.xml)
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
```

### iOS Permissions (ios/Runner/Info.plist)
```xml
<key>NSPhotoLibraryAddUsageDescription</key>
<string>We need access to save downloaded videos</string>
```

---

## 🐛 Troubleshooting

### Issue: Connection Error
**Solution:** Ensure device and server are on same network. Check IP address is correct.

### Issue: Timeout Error
**Solution:** Increase `receiveTimeout` duration. Large videos take longer.

### Issue: 400 Bad Request
**Solution:** Verify URL is valid and video is publicly accessible.

---

## 🔒 Important Notes

1. **responseType MUST be `ResponseType.bytes`** - This receives the video as binary data
2. **Use `writeAsBytes()`** - Writes the binary data to file
3. **Progress tracking works** - `onReceiveProgress` gives real-time updates
4. **No files stored on server** - Everything streams directly to user
5. **CORS is enabled** - Flutter apps can connect from any origin

---

## 🎬 Test URLs

```dart
// YouTube Short
'https://youtube.com/shorts/9wKG_BHjMSI'

// Instagram Reel
'https://www.instagram.com/reel/DJhkAQGNF-t/'

// TikTok Video
'https://www.tiktok.com/@user/video/123456'

// Twitter Video
'https://twitter.com/user/status/123456'
```

---

## ✅ Complete Integration Checklist

- [ ] Add dio and path_provider to pubspec.yaml
- [ ] Copy VideoDownloader class to your project
- [ ] Add Android permissions
- [ ] Add iOS permissions
- [ ] Update baseUrl if needed
- [ ] Test with health check endpoint
- [ ] Test download with sample URL
- [ ] Implement progress UI
- [ ] Handle success/error states
- [ ] Save to gallery (optional)

---

**API Status:** ✅ Running
**Server:** http://10.84.3.92:8000
**Documentation:** http://10.84.3.92:8000/docs
