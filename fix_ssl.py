#!/usr/bin/env python3
"""
SSL Certificate Fix for macOS
Run this script if you encounter SSL certificate errors
"""

import os
import sys
import ssl
import certifi

def fix_ssl_certificates():
    """Install SSL certificates for Python on macOS"""
    print("🔧 Fixing SSL certificates for macOS...\n")
    
    # Check if certifi is installed
    try:
        import certifi
        print(f"✅ certifi is installed: {certifi.where()}")
    except ImportError:
        print("❌ certifi is not installed")
        print("Installing certifi...")
        os.system(f"{sys.executable} -m pip install certifi")
        import certifi
        print(f"✅ certifi installed: {certifi.where()}")
    
    # Set SSL certificate environment variable
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    print(f"\n✅ SSL_CERT_FILE set to: {certifi.where()}")
    print(f"✅ REQUESTS_CA_BUNDLE set to: {certifi.where()}")
    
    # Check Python installation
    print(f"\n📍 Python executable: {sys.executable}")
    print(f"📍 Python version: {sys.version}")
    
    # Try to create SSL context
    try:
        ssl.create_default_context()
        print("\n✅ SSL context can be created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating SSL context: {e}")
    
    print("\n" + "="*60)
    print("🎉 SSL certificate fix completed!")
    print("="*60)
    print("\nNow you can run the video downloader:")
    print("  python video_downloader.py")
    print("\nOr use the alternative command:")
    print("  SSL_CERT_FILE=$(python -m certifi) python video_downloader.py")

if __name__ == "__main__":
    fix_ssl_certificates()
