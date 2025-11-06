# Real-Time Download Progress in Flutter

## 🎯 How It Works

The FastAPI backend streams video bytes, and Flutter's Dio automatically tracks progress through the `onReceiveProgress` callback.

---

## 📱 Complete Flutter Implementation

### 1. API Service with Progress Tracking

```dart
import 'package:dio/dio.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class VideoDownloader {
  final Dio _dio = Dio();
  final String baseUrl = 'http://10.84.3.92:8000';

  /// Download video with real-time progress updates
  Future<Map<String, dynamic>> downloadVideo(
    String videoUrl, {
    required Function(int received, int total) onProgress,
  }) async {
    try {
      print('🔍 Starting download for: $videoUrl');
      
      final tempDir = await getTemporaryDirectory();
      final fileName = 'video_${DateTime.now().millisecondsSinceEpoch}.mp4';
      final savePath = '${tempDir.path}/$fileName';

      // Download with progress tracking
      final response = await _dio.post(
        '$baseUrl/download',
        data: {'url': videoUrl},
        options: Options(
          headers: {'Content-Type': 'application/json'},
          responseType: ResponseType.bytes,
          receiveTimeout: const Duration(minutes: 5),
        ),
        onReceiveProgress: (received, total) {
          // This callback fires automatically as bytes are received
          onProgress(received, total);
        },
      );

      // Write to file
      final file = File(savePath);
      await file.writeAsBytes(response.data);

      return {
        'success': true,
        'filePath': savePath,
        'filename': fileName,
      };
      
    } catch (e) {
      return {
        'success': false,
        'error': e.toString(),
      };
    }
  }
}
```

---

### 2. UI with Progress Indicator

```dart
import 'package:flutter/material.dart';

class DownloadScreen extends StatefulWidget {
  @override
  _DownloadScreenState createState() => _DownloadScreenState();
}

class _DownloadScreenState extends State<DownloadScreen> {
  final VideoDownloader _downloader = VideoDownloader();
  final TextEditingController _urlController = TextEditingController();
  
  double _progress = 0.0;
  bool _isDownloading = false;
  String _status = 'Enter a video URL';
  int _receivedBytes = 0;
  int _totalBytes = 0;

  Future<void> _startDownload() async {
    if (_urlController.text.isEmpty) {
      setState(() => _status = '❌ Please enter a URL');
      return;
    }

    setState(() {
      _isDownloading = true;
      _progress = 0.0;
      _status = 'Initializing download...';
    });

    final result = await _downloader.downloadVideo(
      _urlController.text,
      onProgress: (received, total) {
        setState(() {
          _receivedBytes = received;
          _totalBytes = total;
          
          if (total != -1) {
            _progress = received / total;
            _status = 'Downloading... ${(received / 1024 / 1024).toStringAsFixed(1)} MB / ${(total / 1024 / 1024).toStringAsFixed(1)} MB';
          } else {
            _status = 'Downloading... ${(received / 1024 / 1024).toStringAsFixed(1)} MB';
          }
        });
      },
    );

    setState(() {
      _isDownloading = false;
      if (result['success']) {
        _progress = 1.0;
        _status = '✅ Download complete! Saved to: ${result['filename']}';
      } else {
        _progress = 0.0;
        _status = '❌ Error: ${result['error']}';
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Video Downloader')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            // URL Input
            TextField(
              controller: _urlController,
              decoration: InputDecoration(
                labelText: 'Video URL',
                hintText: 'https://youtube.com/shorts/...',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 20),
            
            // Download Button
            ElevatedButton(
              onPressed: _isDownloading ? null : _startDownload,
              child: Text(_isDownloading ? 'Downloading...' : 'Download Video'),
              style: ElevatedButton.styleFrom(
                minimumSize: Size(double.infinity, 50),
              ),
            ),
            SizedBox(height: 30),
            
            // Progress Indicator
            if (_isDownloading || _progress > 0)
              Column(
                children: [
                  // Linear Progress Bar
                  LinearProgressIndicator(
                    value: _progress,
                    backgroundColor: Colors.grey[300],
                    minHeight: 10,
                  ),
                  SizedBox(height: 10),
                  
                  // Percentage Text
                  Text(
                    '${(_progress * 100).toStringAsFixed(1)}%',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 10),
                  
                  // Status Text
                  Text(
                    _status,
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 14),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
```

---

### 3. Advanced: Circular Progress with Animation

```dart
class CircularProgressWidget extends StatelessWidget {
  final double progress;
  final String status;

  CircularProgressWidget({required this.progress, required this.status});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Stack(
          alignment: Alignment.center,
          children: [
            SizedBox(
              width: 150,
              height: 150,
              child: CircularProgressIndicator(
                value: progress,
                strokeWidth: 12,
                backgroundColor: Colors.grey[300],
              ),
            ),
            Text(
              '${(progress * 100).toInt()}%',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
        SizedBox(height: 20),
        Text(
          status,
          style: TextStyle(fontSize: 16),
        ),
      ],
    );
  }
}
```

---

### 4. Speed Calculation (Optional)

```dart
class DownloadStats {
  int _lastReceived = 0;
  DateTime _lastTime = DateTime.now();
  
  String calculateSpeed(int received) {
    final now = DateTime.now();
    final timeDiff = now.difference(_lastTime).inMilliseconds;
    
    if (timeDiff > 1000) { // Update every second
      final bytesDiff = received - _lastReceived;
      final speedMBps = (bytesDiff / timeDiff) * 1000 / 1024 / 1024;
      
      _lastReceived = received;
      _lastTime = now;
      
      return '${speedMBps.toStringAsFixed(2)} MB/s';
    }
    return '-- MB/s';
  }
}

// Usage in onProgress:
final stats = DownloadStats();

onProgress: (received, total) {
  final speed = stats.calculateSpeed(received);
  setState(() {
    _status = 'Downloading at $speed';
  });
}
```

---

## 🎨 UI Variations

### Material 3 Style
```dart
Card(
  child: Padding(
    padding: EdgeInsets.all(16),
    child: Column(
      children: [
        LinearProgressIndicator(value: _progress),
        SizedBox(height: 8),
        Text('${(_progress * 100).toInt()}% complete'),
      ],
    ),
  ),
)
```

### With Animation
```dart
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  width: MediaQuery.of(context).size.width * _progress,
  height: 50,
  color: Colors.blue,
  child: Center(
    child: Text(
      '${(_progress * 100).toInt()}%',
      style: TextStyle(color: Colors.white),
    ),
  ),
)
```

---

## 🔥 Key Points

1. **`onReceiveProgress` automatically tracks progress** - No backend changes needed!
2. **`received`** = bytes downloaded so far
3. **`total`** = total file size (may be -1 if unknown)
4. **Update UI in setState()** to reflect progress
5. **Progress fires frequently** - consider throttling updates for better performance

---

## 📊 Example Output

```
Initializing download...
Downloading... 2.5 MB / 15.3 MB (16.3%)
Downloading... 5.8 MB / 15.3 MB (37.9%)
Downloading... 10.2 MB / 15.3 MB (66.7%)
Downloading... 15.3 MB / 15.3 MB (100%)
✅ Download complete!
```

---

## ✅ Testing Tips

1. Test with small videos first (< 5MB)
2. Test with large videos to see progress tracking
3. Test network interruption handling
4. Add a cancel button (dio has `CancelToken`)

---

## 🚀 Your API Already Supports This!

The backend streams bytes efficiently. Just use the Flutter code above and you'll see real-time progress automatically! No backend changes needed.

**Server:** http://10.84.3.92:8000
**Ready to use!** 🎉
