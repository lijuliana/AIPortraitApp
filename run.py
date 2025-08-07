#!/usr/bin/env python3
"""
Launcher script for AI Portrait Generator
"""

import os
import sys
import uvicorn
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        "main.py",
        "portrait_service.py", 
        "config.py",
        "static/index.html"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def check_env():
    """Check if environment is properly configured"""
    if not os.path.exists(".env"):
        print("⚠️  No .env file found. Please run setup.py first.")
        return False
    
    # Check if REPLICATE_API_TOKEN is set
    try:
        from dotenv import load_dotenv
        load_dotenv()
        token = os.getenv("REPLICATE_API_TOKEN")
        if not token or token == "your-replicate-api-token-here":
            print("⚠️  Please set your REPLICATE_API_TOKEN in the .env file")
            return False
    except ImportError:
        print("⚠️  python-dotenv not installed. Please run: pip install python-dotenv")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("🚀 AI Portrait Generator Launcher")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please ensure all required files are present.")
        sys.exit(1)
    
    # Check environment
    if not check_env():
        print("\n❌ Please configure your environment properly.")
        print("Run: python setup.py")
        sys.exit(1)
    
    print("✅ All checks passed!")
    print("\n🌐 Starting AI Portrait Generator...")
    print("📱 Frontend will be available at: http://localhost:8000")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 