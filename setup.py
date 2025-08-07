#!/usr/bin/env python3
"""
Setup script for AI Portrait Generator
"""

import os
import sys

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return
    
    print("📝 Creating .env file...")
    api_token = input("Enter your Replicate API token (get it from https://replicate.com/account/api-tokens): ").strip()
    
    if not api_token:
        print("❌ API token is required!")
        return
    
    with open(env_file, 'w') as f:
        f.write(f"REPLICATE_API_TOKEN={api_token}\n")
    
    print("✅ .env file created successfully!")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'replicate',
        'fastapi',
        'uvicorn',
        'python-multipart',
        'pillow',
        'requests',
        'python-dotenv',
        'pydantic',
        'aiofiles'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        os.system(f"pip install {' '.join(missing_packages)}")
    else:
        print("\n✅ All dependencies are installed!")

def main():
    """Main setup function"""
    print("🚀 AI Portrait Generator Setup")
    print("=" * 40)
    
    # Check dependencies
    check_dependencies()
    
    # Create .env file
    create_env_file()
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Make sure your .env file has the correct API token")
    print("2. Run the application: python main.py")
    print("3. Test the API: python test_api.py")
    print("4. Visit http://localhost:8000/docs for API documentation")

if __name__ == "__main__":
    main() 