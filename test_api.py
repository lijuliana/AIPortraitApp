#!/usr/bin/env python3
"""
Test script for the AI Portrait Generator API
"""

import requests
import json
import os
from PIL import Image
import io

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_get_models():
    """Test the models endpoint"""
    print("\nTesting models endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/models")
        if response.status_code == 200:
            print("✅ Models endpoint passed")
            models = response.json()
            print(f"Available models: {list(models['models'].keys())}")
            print(f"Available styles: {models['styles']}")
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Models endpoint error: {e}")

def test_sdxl_generation():
    """Test SDXL portrait generation (no reference image needed)"""
    print("\nTesting SDXL portrait generation...")
    try:
        data = {
            "style": "professional",
            "prompt": "A stunning business portrait, professional lighting, sharp focus"
        }
        response = requests.post(f"{BASE_URL}/generate-portrait-sdxl", json=data)
        if response.status_code == 200:
            print("✅ SDXL generation passed")
            result = response.json()
            print(f"Generated image URL: {result['image_url']}")
            print(f"Model used: {result['model_used']}")
        else:
            print(f"❌ SDXL generation failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ SDXL generation error: {e}")

def create_test_image():
    """Create a simple test image for testing"""
    # Create a simple 100x100 test image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_instantid_generation():
    """Test InstantID portrait generation with a test image"""
    print("\nTesting InstantID portrait generation...")
    try:
        # Create a test image
        test_image = create_test_image()
        
        files = {'reference_image': ('test.jpg', test_image, 'image/jpeg')}
        data = {
            'style': 'realistic',
            'prompt': 'A high-quality portrait, professional photography'
        }
        
        response = requests.post(f"{BASE_URL}/generate-portrait", files=files, data=data)
        if response.status_code == 200:
            print("✅ InstantID generation passed")
            result = response.json()
            print(f"Generated image URL: {result['image_url']}")
            print(f"Model used: {result['model_used']}")
        else:
            print(f"❌ InstantID generation failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ InstantID generation error: {e}")

def test_ensemble_generation():
    """Test ensemble portrait generation"""
    print("\nTesting ensemble portrait generation...")
    try:
        # Create a test image
        test_image = create_test_image()
        
        files = {'reference_image': ('test.jpg', test_image, 'image/jpeg')}
        data = {
            'style': 'realistic',
            'prompt': 'A professional portrait photograph'
        }
        
        response = requests.post(f"{BASE_URL}/generate-portrait-ensemble", files=files, data=data)
        if response.status_code == 200:
            print("✅ Ensemble generation passed")
            result = response.json()
            print(f"Ensemble results: {list(result['ensemble_results'].keys())}")
        else:
            print(f"❌ Ensemble generation failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Ensemble generation error: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing AI Portrait Generator API")
    print("=" * 50)
    
    # Check if API is running
    try:
        requests.get(BASE_URL, timeout=5)
    except requests.exceptions.ConnectionError:
        print("❌ API is not running. Please start the server first:")
        print("   python main.py")
        return
    
    # Run tests
    test_health_check()
    test_get_models()
    test_sdxl_generation()
    test_instantid_generation()
    test_ensemble_generation()
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")

if __name__ == "__main__":
    main() 